import pandas as pd
from pandas.plotting import PlotAccessor
from terality._terality.patch_libs.plot.patch_hist import patch_plot_hist

THRESHOLD_COMPUTATION_CLIENT_SIDE_BYTES = 100_000_000


class TeralityPlotAccessor:
    def __init__(self, obj):
        self._obj = obj  # DataFrame or Series

    def _pandas_hist(self, *args, **kwargs):
        """
        Convert the terality object to a pandas object and performs the plot.hist client side.
        Improve performances on small data as `plot.hist` calls several terality methods, including 2 partitioned jobs
        which are not efficient on small data.
        """

        return self._obj.to_pandas().plot.hist(*args, **kwargs)

    def hist(self, *args, **kwargs):
        # avoid circular import
        from terality._terality.terality_structures.dataframe import DataFrame

        memory_obj = (
            self._obj.memory_usage().sum()
            if isinstance(self._obj, DataFrame)
            else self._obj.memory_usage()
        )
        if memory_obj <= THRESHOLD_COMPUTATION_CLIENT_SIDE_BYTES:
            return self._pandas_hist(*args, **kwargs)

        with patch_plot_hist():
            plot = pd.plotting.PlotAccessor(self._obj)
            return plot.hist(*args, **kwargs)

    def __getattr__(self, item: str):
        """
        Allow any plot method to run client side on small data.
        Above a given threshold, the plotting method is not supported.
        """

        # avoid circular import
        from terality._terality.terality_structures.dataframe import DataFrame

        try:
            getattr(PlotAccessor, item)  # check pandas API
        except AttributeError:
            raise AttributeError(  # pylint: disable=raise-missing-from
                f"`{item}` is not a plotting method."
            )

        memory_obj = (
            self._obj.memory_usage().sum()
            if isinstance(self._obj, DataFrame)
            else self._obj.memory_usage()
        )

        if memory_obj <= THRESHOLD_COMPUTATION_CLIENT_SIDE_BYTES:
            return getattr(self._obj.to_pandas().plot, item)

        threshold_mb = f"{THRESHOLD_COMPUTATION_CLIENT_SIDE_BYTES // 1_000_000:g}"
        raise NotImplementedError(
            f"Terality does not support plot.{item} on objects bigger than {threshold_mb}MB."
        )
