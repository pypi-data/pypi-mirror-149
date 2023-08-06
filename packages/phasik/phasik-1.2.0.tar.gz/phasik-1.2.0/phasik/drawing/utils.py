"""
General utility functions for plots
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import scipy.cluster.hierarchy as sch
import seaborn as sb
from matplotlib.colors import ListedColormap

__all__ = [
    "palette_20_ordered",
    "configure_sch_color_map",
    "display_name",
    "label_subplot_grid_with_shared_axes",
    "adjust_margin",
]


def palette_20_ordered(as_map=False):
    pal = sb.color_palette("tab20", n_colors=20)
    pal2_arr = np.append(pal[::2], pal[1::2], axis=0)
    pal2 = sb.color_palette(pal2_arr)
    if as_map:
        pal2 = ListedColormap(pal2)
    return pal2


def configure_sch_color_map(cmap):
    """Set SciPy's colour palette to use a particular colour map"""
    rgbs = cmap(np.linspace(0, 1, 10))
    sch.set_link_color_palette([mpl.colors.rgb2hex(rgb[:3]) for rgb in rgbs])


def display_name(key):
    """Get more user-friendly name for certain keywords"""
    names = {"maxclust": "Max # clusters", "distance": "Distance threshold"}
    return names[key] if key in names else key


def label_subplot_grid_with_shared_axes(
    rows, columns, total_subplots, xlabel, ylabel, fig, axes
):
    """Method to tidy up cases where we have a grid of plots with shared axes, by deleting unused subplots (if
    number of of subplots is not rectangular) and adding axes ticks

    Parameters
    ----------
    rows : int
        Number of rows in the grid of subplots
    columns : int
        Number of columns in the grid of subplots
    total_subplots : int
        Number of subplots in the grid; need not be a 'rectangular' number
    xlabel : str
        Label of the x-axis
    ylabel : str
        Label of the y-axis
    fig : matplotlib.Figure
        Figure that the subplots are a part of
    axes :list of matplotlib.Axes
        Axes containing the subplots

    Returns
    -------
    None
    """

    if rows > 1:
        axes_left = axes[:, 0]
    else:
        axes_left = [axes[0]]
    for ax in axes_left:
        ax.set_ylabel(ylabel)

    # Bottom row will potentially have fewer subplots than all other rows.
    size_of_extra_row = total_subplots % columns

    if size_of_extra_row != 0 and rows > 1:
        # Delete blank subplots and add x-axis ticks to subplots on penultimate row above blank subplots
        blank_axes = axes[-1, size_of_extra_row:]
        above_blank_axes = axes[-2, size_of_extra_row:]
        axes_on_extra_row = axes[-1, :size_of_extra_row]
        for ax in blank_axes:
            fig.delaxes(ax)
        for ax in above_blank_axes:
            ax.xaxis.set_tick_params(labelbottom=True)
            ax.set_xlabel(xlabel)
        for ax in axes_on_extra_row:
            ax.set_xlabel(xlabel)

    else:
        for ax in axes.flatten()[-columns:]:
            ax.set_xlabel(xlabel)


def adjust_margin(ax=None, top=0, bottom=0, left=0, right=0):
    """Extend the margin of a plot by a percentage of its original width/height

    Parameters
    ----------
    ax : matplotlib.Axes, optional
        Axes whose margins to adjust
    top : float, optional
        Percentage (as decimal) by which to increase top margin
    bottom : float, optional
        Percentage (as decimal) by which to increase bottom margin
    left : float, optional
        Percentage (as decimal) by which to increase left margin
    right : float, optional
        Percentage (as decimal) by which to increase right margin

    Returns
    -------
    None
    """

    if ax is None:
        ax = plt.gca()

    if top or bottom:
        y_limits = ax.get_ylim()
        difference = y_limits[-1] - y_limits[0]
        new_y_limits = [
            y_limits[0] - difference * bottom,
            y_limits[-1] + difference * top,
        ]
        ax.set_ylim(new_y_limits)

    if left or right:
        x_limits = ax.get_xlim()
        difference = x_limits[-1] - x_limits[0]
        new_x_limits = [
            x_limits[0] - difference * left,
            x_limits[-1] + difference * right,
        ]
        ax.set_xlim(new_x_limits)
