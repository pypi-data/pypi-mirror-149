"""
Base class for time series data
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal

from phasik.utils.xppcall import xpprun

# from labellines import labelLines


__all__ = ["TemporalData"]

comparators = {"minima": np.less, "maxima": np.greater}


class TemporalData:
    """Class representing any sort of temporal data for a specified list of variables

    Since teneto's TemporalNetwork class requires all times to start at zero, we again have the concept of 'true' times
    as well as times offset to start at zero.
    """

    def __init__(self, temporal_data, variables, times, true_times):
        """
        Parameters
        ----------
        temporal_data : ndarray
            2D array whose columns are the variables we're interested in and whose rows are the
            temporal data for these variables
        variables : list of str
            List (not a numpy array) of variable names
        times : ndarray
            1D array based on true_times but with values shifted to start at zero
        true_times ndarray
             1D array of time points
        """

        self.temporal_data = temporal_data
        self.variables = variables
        self.times = times
        self.true_times = true_times

    # This method requires xppaut to be installed. Uncomment if xppaut is installed.
    #    @classmethod
    #    def from_ODEs(class_, filepath, start_time=None, end_time=None, xpp_alias='xppaut', uppercase_vars=False):
    #        """Create a TemporalData object by solving a system of ODEs

    #        Uses the solver XPP. XPP must be installed and executable on your PATH under the name xpp_alias

    #        Parameters
    #        ----------
    #        filepath : str
    #            Path to the file specifying the system of ODEs to solve
    #        start_time : int or float, optional
    #            Start of time period from which to take temporal data; set to None (default) to start at beginning. If
    #            given, should
    # be inclusive.
    #        end_time : int of float, optional
    #            End of time period from which to take temporal data; set to None (default) to end at the end. If given,
    #            should be exclusive.
    #        xpp_alias : str
    #            Name of the XPP executable on your PATH.
    #        """

    #        times_and_series, variables = xpprun(filepath, xppname=xpp_alias, clean_after=True)
    #
    #        if uppercase_vars :
    #            variables = [var.upper() for var in variables]

    #        # Since our temporal network has had times shifted to start at zero, do the same here.
    #        # If given, start time should be inclusive and end_time should be exclusive.
    #        true_times = times_and_series[start_time:end_time, 0]
    #        times = true_times if not start_time else true_times - start_time
    #        temporal_data = times_and_series[start_time:end_time, 1:]
    #        return class_(temporal_data, variables, times, true_times)

    @classmethod
    def from_dict(class_, dict_, times, true_times, i_tend=None):
        """Create a TemporalData from a dict with variables as keys and time series as values"""

        variables = list(dict_.keys())
        temporal_data = np.array(list(dict_.values()))
        if i_tend is not None:
            temporal_data = temporal_data[:, 0:i_tend]
            times = times[0:i_tend]
            true_times = true_times[0:i_tend]
        return class_(temporal_data.T, variables, times, true_times)

    @classmethod
    def from_df(class_, df, times, true_times, i_tend=None):
        """Create a TemporalData from a DataFrame with variables as columns and timepoints as rows"""

        variables = df.columns.tolist()
        temporal_data = df.to_numpy()
        if i_tend is not None:
            temporal_data = temporal_data[0:i_tend, :]
            times = times[0:i_tend]
            true_times = true_times[0:i_tend]
        return class_(temporal_data, variables, times, true_times)

    def downsample(self, skip):
        """Return a downsampled copy of the TemporalData object, by skipping ever 'skip' elements"""
        return TemporalData(
            self.temporal_data[::skip, :],
            self.variables,
            self.times[::skip],
            self.true_times[::skip],
        )

    def series(self, variable):
        """Get temporal data for a particular variable"""
        return self.temporal_data[:, self.variables.index(variable)]

    def to_dict(self):
        """Convert temporal data to dict format, with variables as keys and time series as values"""
        return {variable: self.series(variable) for variable in self.variables}

    def to_df(self):
        """Convert temporal data to pandas.DataFrame format, with variables as rows and time points as columns"""
        # was
        return pd.DataFrame.from_dict(self.to_dict()).transpose()
        # but time index was range() by default, not working for downsampling
        # now, indices set as times (maybe need to change to time indices in future)
        # return pd.DataFrame(self.temporal_data.T, index=self.variables, columns=self.times)

    def save_to_csv(self, filepath, index=False):
        """Save temporal data to .csv file, with variables as rows and time points as columns"""
        df = self.to_df().transpose()
        df.to_csv(filepath, index=index)

    def normalise(self):
        """Return new TemporalData where each time series is normalised by its maximum"""

        temporal_data_normalised = self.temporal_data / np.max(
            self.temporal_data, axis=0
        )

        return TemporalData(
            temporal_data_normalised, self.variables, self.times, self.true_times
        )

    def relative_optima(self, variable, optima_type):
        """Get relative optima for a particular variable

        Parameters
        ----------
        variable : str
            Name of the variable whose optima we want
        optima_type : {'minima', 'maxima'}
            Type of optima to look for

        Returns
        -------
        optima : list_like
            Value of the variable at its optima
        optima_times : list_like
            Times at which these optima occur
        """

        series = self.series(variable)
        optima_times = scipy.signal.argrelextrema(series, comparators[optima_type])
        optima = series[optima_times]
        return optima, optima_times

    def plot_relative_optima(
        self, variable, optima_type, ax=None, use_true_times=True, plot_var=True
    ):
        """Plot relative optima for a prticular variable

        Parameters
        ----------
        variable : str
            The name of the variable whose optima we want to plot
        optima_type : {'minima', 'maxima'}
        ax : matplotlib.Axes, optional
            Axes on which to plot
        use_true_times : bool, optional
            Whether to use the 'actual' times or offset the times so that they start at zero

        Returns
        -------
        None
        """

        if ax is None:
            ax = plt.gca()

        times = self.true_times if use_true_times else self.times
        if plot_var:
            ax.plot(times, self.series(variable), "o-")
        mass_minima, mass_minima_times = self.relative_optima(variable, optima_type)
        ax.plot(times[mass_minima_times], mass_minima, "ro")

    def plot_series(
        self,
        variables=None,
        ax=None,
        norm=False,
        add_labels=True,
        labels_xvals=None,
        use_true_times=True,
    ):
        """Plot particular variables' values over time

        Parameters
        ----------
        variables : list of str
            Names of the variable whose values we want to plot
        ax : matplotlib.Axes, optional
            Axes on which to plot
        norm : bool, optional
            Whether or not to normalise the time series by dividing through by the max (default False)
        add_labels : bool, optional
            Whether to label the variables when plotting (default True)
        labels_xvals : list of float, optional
            The positions along the x-axis at which to place the variables' labels (if using). If set to
            None (default), labels will be placed at regular intervals along x-axis.
        use_true_times : bool, optional
            Whether to use the 'actual' times or offset the times so that they start at zero (default True)

        Returns
        -------
        None
        """

        if ax is None:
            ax = plt.gca()
        if variables is None:
            variables = self.variables
        times = self.true_times if use_true_times else self.times

        for variable in variables:
            y = normed(self.series(variable)) if norm else self.series(variable)
            ax.plot(times, y, label=variable)

        if add_labels:
            if not labels_xvals:
                # Add evenly-spaced labels
                labels_interval = len(times) // (len(variables) + 1)
                labels_xvals = [
                    times[labels_interval * (i + 1)] for i in range(len(variables))
                ]


#            labelLines(ax.get_lines(), zorder=2.5, xvals=labels_xvals)


def normed(x):
    return x / np.max(x)
