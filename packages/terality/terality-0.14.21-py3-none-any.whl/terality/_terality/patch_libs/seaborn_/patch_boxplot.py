import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from typing import Optional, Any

import numpy as np
import pandas as pd

from terality._terality.patch_libs.patch_pandas_and_numpy import (
    patch_external_packages,
)
from terality._terality.httptransport import HTTP_CONNECTION_POOL_SIZE

# Previous versions require a pandas version < 1.2.5.
from terality._terality.utils import logger

SUPPORTED_SEABORN_VERSION = ["0.9.0", "0.9.1", "0.10.0", "0.10.1", "0.11.0", "0.11.1", "0.11.2"]


def _try_get_group(groupby, key):
    try:
        return groupby.get_group(key)
    except KeyError:
        return np.array([])


def _group_longform(self, vals, grouper, order):  # pylint: disable=unused-argument
    """Monkey patch of seaborn.categorical._BoxPlotter._group_longform.

    Performs a groupby, and then calls `get_group` for every key (that were previously computed).
    With many categories, calling sequentially `get_group` for every key can have poor performance,
    even if we reuse partitions over different calls. Thus, we parallelize get_group calls
    in order to gain performance.

    """

    # Ensure that the groupby will work
    if not isinstance(vals, pd.Series):
        if isinstance(grouper, pd.Series):
            index = grouper.index
        else:
            index = None
        vals = pd.Series(vals, index=index)

    # Get the vals axis label
    label = vals.name

    # Group the val data
    groupby = vals.groupby(grouper)
    first_group_and_empty_groups = []
    keys = list(order)

    # Do the first get_group that computes groupby partitioned and mutates the groupby object server side.
    # We do this computation before using the ThreadPool to avoid concurrency issues.
    keys_to_parallelize = list(keys)
    for key in keys:
        try:
            g_vals = groupby.get_group(key)
            keys_to_parallelize.remove(key)
            first_group_and_empty_groups.append(g_vals)
            break
        except KeyError:
            g_vals = np.array([])
            first_group_and_empty_groups.append(g_vals)
    else:
        # Only empty groups, should not happen
        return first_group_and_empty_groups, label

    # Then we can parallelize the other calls as we know they won't mutate the groupby object server side.
    with ThreadPoolExecutor(max_workers=HTTP_CONNECTION_POOL_SIZE) as pool:
        out = pool.map(
            _try_get_group,
            [groupby] * len(keys_to_parallelize),
            keys_to_parallelize,
            timeout=100,
        )
    out_data = first_group_and_empty_groups + list(out)

    return out_data, label


def _draw_single_box_without_hue(i, group_data, vert, width, axe, kws) -> Optional[Any]:
    from seaborn.utils import remove_na

    # if i == 1:
    #     time.sleep(1)
    # Handle case where there is data at this level
    if group_data.size == 0:
        return None

    # Draw a single box or a set of boxes
    # with a single level of grouping
    no_na = remove_na(group_data)
    box_data = np.asarray(no_na)

    # Handle case where there is no non-null data
    if box_data.size == 0:
        return None

    # Order of the call of this method determines the order of lines within Axes object,
    # but it does not impact boxes order as we force the positions here.
    artist_dict = axe.boxplot(
        box_data, vert=vert, patch_artist=True, positions=[i], widths=width, **kws
    )
    return artist_dict


def _draw_boxplot(self, lib, kws):
    """Monkey patch of seaborn.categorical._BoxPlotter._group_longform.

    Use a ThreadPoolExecutor to parallelize computations instead of having a sequential loop
    that has poor performance when computing stats for each category.
    """

    if self.plot_hues is not None:
        raise NotImplementedError("Terality does not support seaborn.boxplot `hue` parameter.")

    vert = self.orient == "v"
    props = {}
    for obj in ["box", "whisker", "cap", "median", "flier"]:
        props[obj] = kws.pop(obj + "props", {})

    with ThreadPoolExecutor(max_workers=HTTP_CONNECTION_POOL_SIZE) as pool:
        nb_groups = len(self.plot_data)
        out = pool.map(
            _draw_single_box_without_hue,
            list(range(nb_groups)),
            self.plot_data,
            [vert] * nb_groups,
            [self.width] * nb_groups,
            [lib] * nb_groups,
            [kws] * nb_groups,
            timeout=100,
        )

    for i, artist_dict in enumerate(list(out)):  # note colors
        if artist_dict is None:
            continue
        self.restyle_boxplot(artist_dict, self.colors[i], props)


@contextmanager
def patch_seaborn_boxplot():
    """Enable the use of terality structures within seaborn boxplot.

    This context manager should be used over `patch_external_packages` for `seaborn.boxplot`,
    as it benefits from specific performance boost.
    It is recommended to import seaborn within the context manager, as it may prevent
    of some symbols imported by seaborn not to be patched.

    Example:
    with patch_external_packages():
        import seaborn as sb
        sb.boxplot(df_terality)

    """

    try:
        import seaborn as sb
    except ImportError as e:
        raise ImportError(
            "The 'seaborn' package is not installed, can't patch it to make it compatible with Terality."
        ) from e

    if sb.__version__ not in SUPPORTED_SEABORN_VERSION:
        raise ImportError(
            f"Seaborn version {sb.__version__} is installed, but Terality only supports following versions: {SUPPORTED_SEABORN_VERSION}"
        )

    with patch_external_packages():
        previous_log_level = logger.level
        logger.setLevel(logging.ERROR)

        original_draw_boxplot = sb.categorical._BoxPlotter.draw_boxplot
        sb.categorical._BoxPlotter.draw_boxplot = _draw_boxplot

        original_group_longform = sb.categorical._BoxPlotter._group_longform
        sb.categorical._BoxPlotter._group_longform = _group_longform

        try:
            yield
        finally:
            logger.setLevel(previous_log_level)
            sb.categorical._BoxPlotter.draw_boxplot = original_draw_boxplot
            sb.categorical._BoxPlotter._group_longform = original_group_longform
