import itertools
import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from numbers import Number
from threading import Event

import numpy as np
import pandas as pd
import terality
from numpy import ndarray
from pandas.core.dtypes.generic import ABCSeries
from pandas.io.formats.printing import pprint_thing
from terality._terality.httptransport import HTTP_CONNECTION_POOL_SIZE

from terality._terality.patch_libs.patch_pandas_and_numpy import (
    patch_external_packages,
)

# Previous versions require a pandas version < 1.2.5.
from terality._terality.utils import logger

# TODO To check compatibility of un-released versions, we would compare hashes of patched methods code between
#  future and currently supported versions.

PANDAS_SUPPORTED_VERSIONS = (
    [f"1.2.{i}" for i in range(3, 6)]
    + [f"1.3.{i}" for i in range(6)]
    + [
        f"1.4.{i}" for i in range(10)
    ]  # Support un-released 1.4.x versions at it is very likely to work
)

# Below versions require more numpy API to support and decorator check_figures_equal seems buggy
MATPLOTLIB_SUPPORTED_VERSIONS = (
    [f"3.3.{i}" for i in range(5)]
    + [f"3.4.{i}" for i in range(3)]
    + [
        f"3.5.{i}" for i in range(10)
    ]  # Support un-released 3.5.x versions at it is very likely to work
)


def hist(  # pylint: disable=C0103,W0622,C0103,R0912,R0913,R0914,R0915,R1704,R1705
    self,
    x,
    bins=None,
    range=None,
    density=False,
    weights=None,
    cumulative=False,
    bottom=None,
    histtype="bar",
    align="mid",
    orientation="vertical",
    rwidth=None,
    log=False,
    color=None,
    label=None,
    stacked=False,
    **kwargs,
):
    """
    Monkey patch `hist` so `col_num` and `events_draw_finished` kwargs are used to draw histograms respecting column order.
    It avoid having a probabilistic column order drawing, that might lead to bugs / probabilistic plots.
    """
    import matplotlib.lines as mlines
    import matplotlib.colors as mcolors
    from matplotlib import cbook, rcParams, _api

    # PATCH CODE: additional parameters added to draw according histograms respecting column order
    col_num = kwargs.pop("col_num")
    events_draw_finished = kwargs.pop("events_draw_finished")
    # END PATCH CODE

    # Avoid shadowing the builtin.
    bin_range = range
    from builtins import range

    if np.isscalar(x):
        x = [x]

    if bins is None:
        bins = rcParams["hist.bins"]

    # Validate string inputs here to avoid cluttering subsequent code.
    _api.check_in_list(["bar", "barstacked", "step", "stepfilled"], histtype=histtype)
    _api.check_in_list(["left", "mid", "right"], align=align)
    _api.check_in_list(["horizontal", "vertical"], orientation=orientation)

    if histtype == "barstacked" and not stacked:
        stacked = True

    # Massage 'x' for processing.
    x = cbook._reshape_2D(x, "x")
    nx = len(x)  # number of datasets

    # Process unit information.  _process_unit_info sets the unit and
    # converts the first dataset; then we convert each following dataset
    # one at a time.
    if orientation == "vertical":
        convert_units = self.convert_xunits
        x = [*self._process_unit_info([("x", x[0])], kwargs), *map(convert_units, x[1:])]
    else:  # horizontal
        convert_units = self.convert_yunits
        x = [*self._process_unit_info([("y", x[0])], kwargs), *map(convert_units, x[1:])]

    if bin_range is not None:
        bin_range = convert_units(bin_range)

    if not cbook.is_scalar_or_string(bins):
        bins = convert_units(bins)

    # We need to do to 'weights' what was done to 'x'
    if weights is not None:
        w = cbook._reshape_2D(weights, "weights")
    else:
        w = [None] * nx

    if len(w) != nx:
        raise ValueError("weights should have the same shape as x")

    input_empty = True
    for xi, wi in zip(x, w):
        len_xi = len(xi)
        if wi is not None and len(wi) != len_xi:
            raise ValueError("weights should have the same shape as x")
        if len_xi:
            input_empty = False

    if color is None:
        color = [self._get_lines.get_next_color() for i in range(nx)]
    else:
        color = mcolors.to_rgba_array(color)
        if len(color) != nx:
            raise ValueError(
                f"The 'color' keyword argument must have one "
                f"color per dataset, but {nx} datasets and "
                f"{len(color)} colors were provided"
            )

    hist_kwargs = dict()

    # if the bin_range is not given, compute without nan numpy
    # does not do this for us when guessing the range (but will
    # happily ignore nans when computing the histogram).
    if bin_range is None:
        xmin = np.inf
        xmax = -np.inf
        for xi in x:
            if len(xi):
                # python's min/max ignore nan,
                # np.minnan returns nan for all nan input
                xmin = min(xmin, np.nanmin(xi))
                xmax = max(xmax, np.nanmax(xi))
        if xmin <= xmax:  # Only happens if we have seen a finite value.
            bin_range = (xmin, xmax)

    # If bins are not specified either explicitly or via range,
    # we need to figure out the range required for all datasets,
    # and supply that to np.histogram.
    if not input_empty and len(x) > 1:
        if weights is not None:
            _w = np.concatenate(w)
        else:
            _w = None
        bins = np.histogram_bin_edges(np.concatenate(x), bins, bin_range, _w)
    else:
        hist_kwargs["range"] = bin_range

    density = bool(density)
    if density and not stacked:
        hist_kwargs["density"] = density

    # List to store all the top coordinates of the histograms
    tops = []  # Will have shape (n_datasets, n_bins).
    # Loop through datasets
    for i in range(nx):
        # this will automatically overwrite bins,
        # so that each histogram uses the same bins
        m, bins = np.histogram(x[i], bins, weights=w[i], **hist_kwargs)
        tops.append(m)

    # PATCH CODE: Terality computations just finished, now wait until all previous column threads finish to draw
    # their histogram before drawing the current histogram within the `Axes` object (self).
    for event_draw_finished in events_draw_finished[0:col_num]:
        event_draw_finished.wait()

    tops = np.array(tops, float)  # causes problems later if it's an int
    if stacked:
        tops = tops.cumsum(axis=0)
        # If a stacked density plot, normalize so the area of all the
        # stacked histograms together is 1
        if density:
            tops = (tops / np.diff(bins)) / tops[-1].sum()
    if cumulative:
        slc = slice(None)
        if isinstance(cumulative, Number) and cumulative < 0:
            slc = slice(None, None, -1)
        if density:
            tops = (tops * np.diff(bins))[:, slc].cumsum(axis=1)[:, slc]
        else:
            tops = tops[:, slc].cumsum(axis=1)[:, slc]

    patches = []

    if histtype.startswith("bar"):

        totwidth = np.diff(bins)

        if rwidth is not None:
            dr = np.clip(rwidth, 0, 1)
        elif len(tops) > 1 and ((not stacked) or rcParams["_internal.classic_mode"]):
            dr = 0.8
        else:
            dr = 1.0

        if histtype == "bar" and not stacked:
            width = dr * totwidth / nx
            dw = width
            boffset = -0.5 * dr * totwidth * (1 - 1 / nx)
        elif histtype == "barstacked" or stacked:
            width = dr * totwidth
            boffset, dw = 0.0, 0.0

        if align == "mid":
            boffset += 0.5 * totwidth
        elif align == "right":
            boffset += totwidth

        if orientation == "horizontal":
            _barfunc = self.barh
            bottom_kwarg = "left"
        else:  # orientation == 'vertical'
            _barfunc = self.bar
            bottom_kwarg = "bottom"

        for m, c in zip(tops, color):
            if bottom is None:
                bottom = np.zeros(len(m))
            if stacked:
                height = m - bottom
            else:
                height = m
            bars = _barfunc(
                bins[:-1] + boffset,
                height,
                width,
                align="center",
                log=log,
                color=c,
                **{bottom_kwarg: bottom},
            )
            patches.append(bars)
            if stacked:
                bottom = m
            boffset += dw
        # Remove stickies from all bars but the lowest ones, as otherwise
        # margin expansion would be unable to cross the stickies in the
        # middle of the bars.
        for bars in patches[1:]:
            for patch in bars:
                patch.sticky_edges.x[:] = patch.sticky_edges.y[:] = []

    elif histtype.startswith("step"):
        # these define the perimeter of the polygon
        x = np.zeros(4 * len(bins) - 3)
        y = np.zeros(4 * len(bins) - 3)

        x[0 : 2 * len(bins) - 1 : 2], x[1 : 2 * len(bins) - 1 : 2] = bins, bins[:-1]
        x[2 * len(bins) - 1 :] = x[1 : 2 * len(bins) - 1][::-1]

        if bottom is None:
            bottom = 0

        y[1 : 2 * len(bins) - 1 : 2] = y[2 : 2 * len(bins) : 2] = bottom
        y[2 * len(bins) - 1 :] = y[1 : 2 * len(bins) - 1][::-1]

        if log:
            if orientation == "horizontal":
                self.set_xscale("log", nonpositive="clip")
            else:  # orientation == 'vertical'
                self.set_yscale("log", nonpositive="clip")

        if align == "left":
            x -= 0.5 * (bins[1] - bins[0])
        elif align == "right":
            x += 0.5 * (bins[1] - bins[0])

        # If fill kwarg is set, it will be passed to the patch collection,
        # overriding this
        fill = histtype == "stepfilled"

        xvals, yvals = [], []
        for m in tops:
            if stacked:
                # top of the previous polygon becomes the bottom
                y[2 * len(bins) - 1 :] = y[1 : 2 * len(bins) - 1][::-1]
            # set the top of this polygon
            y[1 : 2 * len(bins) - 1 : 2] = y[2 : 2 * len(bins) : 2] = m + bottom

            # The starting point of the polygon has not yet been
            # updated. So far only the endpoint was adjusted. This
            # assignment closes the polygon. The redundant endpoint is
            # later discarded (for step and stepfilled).
            y[0] = y[-1]

            if orientation == "horizontal":
                xvals.append(y.copy())
                yvals.append(x.copy())
            else:
                xvals.append(x.copy())
                yvals.append(y.copy())

        # stepfill is closed, step is not
        split = -1 if fill else 2 * len(bins)
        # add patches in reverse order so that when stacking,
        # items lower in the stack are plotted on top of
        # items higher in the stack
        for x, y, c in reversed(list(zip(xvals, yvals, color))):
            patches.append(
                self.fill(
                    x[:split],
                    y[:split],
                    closed=True if fill else None,
                    facecolor=c,
                    edgecolor=None if fill else c,
                    fill=fill if fill else None,
                    zorder=None if fill else mlines.Line2D.zorder,
                )
            )
        for patch_list in patches:
            for patch in patch_list:
                if orientation == "vertical":
                    patch.sticky_edges.y.append(0)
                elif orientation == "horizontal":
                    patch.sticky_edges.x.append(0)

        # we return patches, so put it back in the expected order
        patches.reverse()

    # If None, make all labels None (via zip_longest below); otherwise,
    # cast each element to str, but keep a single str as it.
    labels = [] if label is None else np.atleast_1d(np.asarray(label, str))
    for patch, lbl in itertools.zip_longest(patches, labels):
        if patch:
            p = patch[0]
            p.update(kwargs)
            if lbl is not None:
                p.set_label(lbl)
            for p in patch[1:]:
                p.update(kwargs)
                p.set_label("_nolegend_")

    if nx == 1:
        return tops[0], bins, patches[0]
    else:
        patch_type = "BarContainer" if histtype.startswith("bar") else "list[Polygon]"
        return tops, bins, cbook.silent_list(patch_type, patches)


def getdata(a, subok=True):  # pylint: disable=invalid-name
    """
    Early return if the input array is terality NDArray
    Requires a monkey patch as we do not support np.array(copy=False).
    """

    # START PATCH CODE
    if isinstance(a, terality.NDArray):
        return a
    # END PATCH CODE

    try:
        data = a._data
    except AttributeError:
        data = np.array(a, copy=False, subok=subok)
    if not subok:
        return data.view(ndarray)
    return data


def _convert_dx(self, dx, x0, xconv, convert):  # pylint: disable=invalid-name, unused-argument
    """
    Monkey patch replacing "type(xconv) is np.ndarray" by "isinstance(xconv, np.ndarray)" so our instancecheck patching works.
    """

    # START PATCH CODE
    from matplotlib import cbook  # import here to not break client not having matplotlib installed

    assert isinstance(xconv, np.ndarray)
    # END PATCH CODE

    if xconv.size == 0:
        # xconv has already been converted, but maybe empty...
        return convert(dx)

    try:
        # attempt to add the width to x0; this works for
        # datetime+timedelta, for instance

        # only use the first element of x and x0.  This saves
        # having to be sure addition works across the whole
        # vector.  This is particularly an issue if
        # x0 and dx are lists so x0 + dx just concatenates the lists.
        # We can't just cast x0 and dx to numpy arrays because that
        # removes the units from unit packages like `pint` that
        # wrap numpy arrays.
        try:
            x0 = cbook.safe_first_element(x0)
        except (TypeError, IndexError, KeyError):
            pass

        try:
            x = cbook.safe_first_element(xconv)  # pylint: disable=invalid-name
        except (TypeError, IndexError, KeyError):
            x = xconv  # pylint: disable=invalid-name

        delist = False
        if not np.iterable(dx):
            dx = [dx]
            delist = True
        dx = [convert(x0 + ddx) - x for ddx in dx]
        if delist:
            dx = dx[0]
    except (ValueError, TypeError, AttributeError):
        # if the above fails (for any reason) just fallback to what
        # we do by default and convert dx by itself.
        dx = convert(dx)
    return dx


def _compute_plot_data(self):
    """
    Monkey patch modifying the last line changes as terality does not support `apply(axis=0)`.
    """

    data = self.data

    if isinstance(data, ABCSeries):
        label = self.label
        if label is None and data.name is None:
            label = "None"
        data = data.to_frame(name=label)

    # GH16953, _convert is needed as fallback, for ``Series``
    # with ``dtype == object``
    data = data._convert(datetime=True, timedelta=True)
    include_type = [np.number, "datetime", "datetimetz", "timedelta"]

    # GH23719, allow plotting boolean
    if self.include_bool is True:
        include_type.append(np.bool_)

    # GH22799, exclude datetime-like type for boxplot
    exclude_type = None
    if self._kind == "box":
        include_type = [np.number]
        exclude_type = ["timedelta"]

    # GH 18755, include object and category type for scatter plot
    if self._kind == "scatter":
        include_type.extend(["object", "category"])

    numeric_data = data.select_dtypes(include=include_type, exclude=exclude_type)

    try:
        is_empty = numeric_data.columns.empty
    except AttributeError:
        is_empty = len(numeric_data) == 0

    # no non-numeric frames or series allowed
    if is_empty:
        raise TypeError("no numeric data to plot")

    # START PATCH CODE
    # TODO _convert_to_ndarray is used to convert pandas dtypes to numpy dtypes (like nullable ints to floats)
    # self.data = numeric_data.apply(self._convert_to_ndarray)
    self.data = numeric_data
    # END PATCH CODE


def _make_single_plot(
    self, y, label, col_num, colors, stacking_id, events_draw_finished
):  # pylint: disable=invalid-name
    """
    Draw a single plot for a 1D input (Series), this function is meant to be called by different threads
    simultaneously.
    `events_draw_finished` is an additional parameter specific to the monkey patch, that allows histogram to be drawn
     respecting column orders.
    """

    ax = self._get_ax(col_num)  # pylint: disable=invalid-name

    kwds = self.kwds.copy()

    label = pprint_thing(label)
    kwds["label"] = label

    style, kwds = self._apply_style_colors(colors, kwds, col_num, label)
    if style is not None:
        kwds["style"] = style

    kwds = self._make_plot_keywords(kwds, y)

    # We allow weights to be a multi-dimensional array, e.g. a (10, 2) array,
    # and each sub-array (10,) will be called in each iteration. If users only
    # provide 1D array, we assume the same weights is used for all iterations
    weights = kwds.get("weights", None)
    if weights is not None and np.ndim(weights) != 1:
        kwds["weights"] = weights[:, col_num]

    # PATCH CODE: `col_num` and `events` are additional parameters not used within the `_plot` method,
    # they are directly propagated to `Axes.hist` method within kwargs.
    kwds["col_num"] = col_num
    kwds["events_draw_finished"] = events_draw_finished

    artists = self._plot(
        ax,
        y,
        column_num=col_num,
        stacking_id=stacking_id,
        **kwds,
    )
    self._add_legend_handle(artists[0], label, index=col_num)

    # PATCH CODE: Notify other threads that the drawing part of the current thread is finished.
    events_draw_finished[col_num].set()


def _make_plot(self):
    """
    Monkey patch to parallelize computations over columns.
    The fact that each thread calls ax.hist in a probabilistic way leads to several issues:
    - legends order is probabilistic
    - which bars are in foreground/background is probabilistic
    - stacked=True does not work
    """

    colors = self._get_colors()
    stacking_id = self._get_stacking_id()

    with ThreadPoolExecutor(max_workers=HTTP_CONNECTION_POOL_SIZE) as pool:
        labels_and_values = list(self._iter_data())
        labels = [item[0] for item in labels_and_values]
        values = [item[1] for item in labels_and_values]
        nb_cols = len(labels_and_values)
        events_draw_finished = [Event() for _ in range(nb_cols)]

        out = pool.map(
            _make_single_plot,
            [self] * nb_cols,
            values,
            labels,
            list(range(nb_cols)),
            [colors] * nb_cols,
            [stacking_id] * nb_cols,
            [events_draw_finished] * nb_cols,
            timeout=100,
        )
        _ = list(out)  # triggers the threads ? useless ?


@contextmanager
def patch_plot_hist():  # pylint: disable=too-many-statements
    """
    To be used before calling the pandas method PlotAccessor.plot.hist.
    It enables patching top level pandas/numpy methods and uses some specific monkey patches.
    Note that monkey patches to implement are trickier than for an external lib, because
    we need to patch internal pandas methods (that rely on low level pandas features like block manager).
    """

    try:
        import matplotlib as mpl
    except ImportError as e:
        raise ImportError(
            "The 'matplotlib' package is not installed, can't patch it to make it compatible with Terality."
        ) from e

    if mpl.__version__ not in MATPLOTLIB_SUPPORTED_VERSIONS:
        raise ImportError(
            f"Matplotlib version {mpl.__version__} is installed, but Terality only supports following versions: {MATPLOTLIB_SUPPORTED_VERSIONS}"
        )

    if pd.__version__ not in PANDAS_SUPPORTED_VERSIONS:
        raise ImportError(
            f"Pandas version {pd.__version__} is installed, but plot.hist only supports following versions: {PANDAS_SUPPORTED_VERSIONS}"
        )

    with patch_external_packages():
        # import here to not break client not having matplotlib installed
        from pandas.plotting._matplotlib import HistPlot
        from pandas.plotting._matplotlib.core import MPLPlot
        from matplotlib.axes import Axes
        from matplotlib import _preprocess_data

        previous_log_level = logger.level
        logger.setLevel(logging.ERROR)

        # `_convert` and `_get_numeric_data` private method are called by pandas `PlotAccessor` code,
        # but these methods are not supported by Terality as they are pandas private API. Thus, we have to patch them.
        # TODO _convert should infer better dtypes like str -> datetimes.
        terality.DataFrame._convert = lambda df, *args, **kwargs: df
        terality.Series._convert = lambda series, *args, **kwargs: series

        # TODO Test pandas behavior on datetimes and handle it
        terality.DataFrame._get_numeric_data = lambda df: df.select_dtypes("number")
        terality.Series._get_numeric_data = lambda series: series

        # Required as we do not support `apply(axis=0)`
        old_compute_plot_data = MPLPlot._compute_plot_data
        MPLPlot._compute_plot_data = _compute_plot_data

        # Required as the module imports the symbol directly, like `from pandas import isna`
        old_isna = pd.plotting._matplotlib.hist.isna
        pd.plotting._matplotlib.hist.isna = pd.isna

        try:
            # Only in pandas 1.4 (maybe 1.3 too)
            old_notna = pd.core.dtypes.missing.notna
            pd.core.dtypes.missing.notna = pd.notna
        except AttributeError:
            pass

        # Required to replace a type check by a isinstance check so our instancecheck patching works
        old_convert_dx = Axes._convert_dx
        Axes._convert_dx = _convert_dx

        # Required as we do not support `copy=False`
        old_getdata = np.ma.getdata
        np.ma.getdata = getdata

        # Required to parallelize hist computation over columns
        # Unnused for now as the probabilistic calls to ax.hist leads to several issues.
        old_make_plot = HistPlot._make_plot
        HistPlot._make_plot = _make_plot

        # Required to pass additional parameters in order to draw histograms respecting column order.
        old_axes_hist = Axes.hist
        Axes.hist = _preprocess_data(hist, replace_names=["x", "weights"], label_namer="x")

        # Required to pass isinstance checks on internal pandas types (like ABCDataFrame)
        terality.Index._typ = "index"
        terality.Series._typ = "series"
        terality.DataFrame._typ = "dataframe"

        try:
            yield
        finally:
            logger.setLevel(previous_log_level)

            MPLPlot._compute_plot_data = old_compute_plot_data
            pd.plotting._matplotlib.hist.isna = old_isna

            try:
                # Only in pandas 1.4 (maybe 1.3 too)
                pd.core.dtypes.missing.notna = old_notna
            except AttributeError:
                pass

            Axes._convert_dx = staticmethod(old_convert_dx)
            Axes.hist = old_axes_hist
            np.ma.getdata = old_getdata
            HistPlot._make_plot = old_make_plot

            terality.DataFrame._convert = None
            terality.DataFrame._get_numeric_data = None

            terality.Index._typ = None
            terality.Series._typ = None
            terality.DataFrame._typ = None
