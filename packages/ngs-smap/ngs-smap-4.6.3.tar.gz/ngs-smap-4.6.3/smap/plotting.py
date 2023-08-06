from dataclasses import dataclass, field
from itertools import cycle

import matplotlib
import numpy as np
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt

matplotlib.use('Pdf')


@dataclass(frozen=True, order=True, repr=False)
class PlotLevel:
    compare_value: int = field(init=False, repr=False, compare=True)
    string_representation: str = field(repr=True, init=True, compare=False)

    def __post_init__(self):
        mapping = {'all': 10, 'summary': 5, 'nothing': 0}
        try:
            object.__setattr__(self, 'compare_value', mapping[self.string_representation])
        except KeyError:
            raise ValueError(f"'{self.string_representation}' is not a correct plot level, "
                             f" should be a value from {', '.join(mapping.keys())}")

    def __str__(self) -> str:
        return self.string_representation

    def __repr__(self) -> str:
        return self.string_representation


PLOT_ALL = PlotLevel('all')
PLOT_SUMMARY = PlotLevel('summary')
PLOT_NOTHING = PlotLevel('nothing')


def histogram(values,
              name,
              title,
              xlab,
              ylab,
              color,
              xmin,
              xmax,
              binwidth,
              plot_type,
              xaxisticks=None,
              thresholds=None,
              ylog_scale=False):
    """
    General function to create a histogram for the given values.
    """
    assert xmin <= xmax
    plt.figure(figsize=(10, 10))
    plt.hist(values, alpha=0.5, color=color, bins=np.arange(xmin, xmax+2)-binwidth/2)
    if ylog_scale:
        plt.yscale('log')
        axes = plt.gca()
        axes.yaxis.set_major_formatter(ScalarFormatter())
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    xaxisticks = xaxisticks if xaxisticks else 1
    xlabs = [i for i in np.arange(xmin, xmax+1) if i % xaxisticks == 0]
    if not xlabs or not xlabs[0] == xmin:
        xlabs.insert(0, xmin)
    if not xlabs or not xlabs[-1] == xmax:
        xlabs.append(xmax)
        # Check if second to last xlabel is too close to last xlabel
        if xlabs[-2] >= xmax - xaxisticks/2:
            xlabs.pop(-2)
    plt.xticks(xlabs)
    plt.xlim([xmin-1, xmax+1])
    if thresholds:
        thresholds = list(thresholds)
        plt.axvline(x=thresholds.pop(0), color='gold')
        styling = cycle([{'color': 'darkorange', 'ls': 'dotted'},
                         {'color': 'chocolate', 'ls': 'solid'}])
        offset = cycle([0.2, -0.2])
        while thresholds:
            options = next(styling)
            plt.axvline(x=thresholds.pop()+next(offset), **options)
    plt.tight_layout()
    plt.savefig(name + f'.histogram.{plot_type}', format=plot_type)
    plt.close()


def barplot(x_values,
            height,
            name,
            title,
            xlab,
            ylab,
            color,
            plot_type,
            xaxisticks=None,
            hide_xlabels=False):
    plt.figure(figsize=(10, 10))
    plt.bar(x_values, height, align='center', alpha=0.5, color=color)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    xaxisticks = xaxisticks if xaxisticks else 1
    xlabs = [i for n, i in enumerate(x_values) if n % xaxisticks == 0 or n == 0]
    plt.xticks(xlabs, xlabs)
    if hide_xlabels:
        plt.gca().get_xaxis().set_visible(not hide_xlabels)
    plt.tight_layout()
    plt.savefig(name + f'.barplot.{plot_type}', format=plot_type)
    plt.close()


def scatterplot(x_values,
                y_values,
                name,
                title,
                xlab,
                ylab,
                color,
                plot_type,
                rotate_xlabels=False,
                marker='o'):
    plt.figure(figsize=(10, 10))
    plt.scatter(x_values, y_values, alpha=0.5, color=color, marker=marker)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.ylim(ymin=0)
    plt.xlim(xmin=0)
    if rotate_xlabels:
        plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(name + f'.scatter.{plot_type}', format=plot_type)
    plt.close()


def heatmap(data, row_label=None, col_label=None, xticklabels=None, yticklabels=None,
            title=None, ax=None, cbarlabel="", xmin=0, ymin=0, annotate=False, **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.
    """

    if not ax:
        ax = plt.gca()

    # Set the xlimits
    # Although the blocks in the heatmap are 1 unit wide,
    # The axis system works continuously, so we need to adjust with 0.5 (half a block witdth)
    numrows, numcols = data.shape
    xlim = (xmin-0.5, numcols-0.5)
    ylim = (numrows-0.5, ymin-0.5)  # Reverse y-axis
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # Make sure we only get integers as axis ticks
    ax.xaxis.get_major_locator().set_params(integer=True)
    # Customize ticks to always include min and max
    if xticklabels is None:
        new_ticks = format_ticks(ax.get_xticks(), xmin, numcols-0.5)
        ax.set_xticks(new_ticks)
    else:
        ax.set_xticks(range(0, len(xticklabels)), xticklabels)

    ax.yaxis.get_major_locator().set_params(integer=True)
    if yticklabels is None:
        new_ticks = format_ticks(ax.get_yticks(), ymin, numrows-0.5)
        ax.set_yticks(new_ticks)
    else:
        ax.set_yticks(range(0, len(yticklabels)), yticklabels)

    # Plot the heatmap
    im = ax.imshow(data, interpolation=None, **kwargs)

    # Set the colorbar limits to the visable data
    visible_data = data[xmin:numrows, ymin:numcols]
    cmin, cmax = np.nanmin(visible_data), np.nanmax(visible_data)
    im.set_clim(cmin, cmax)

    # Add text annotations for each squars
    if annotate:
        for i in range(numrows):
            for j in range(numcols):
                ax.text(j, i, data[i, j], ha="center", va="center", color="w")

    # Use minor ticks as grid
    ax.set_xticks(np.arange(*xlim, 1), minor=True)
    ax.set_yticks(np.arange(ymin-0.5, numrows-0.5, 1), minor=True)
    ax.grid(which='minor', color='lightgray', linestyle='-', linewidth=0.5)
    ax.tick_params(which='minor',
                   bottom=False,
                   top=False,
                   labelbottom=False,
                   right=False,
                   left=False,
                   labelleft=False)

    # Change the font size of the tick labels
    ax.tick_params(which='both', labelsize='medium')

    # Create colorbar
    im_ratio = numrows/numcols
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046*im_ratio, pad=0.04)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom", fontsize="large")
    cbar.ax.tick_params(which='both', labelsize='medium')

    if title:
        ax.set_title(title)
    if row_label:
        ax.set_xlabel(row_label, multialignment='center', size='large')
    if col_label:
        ax.set_ylabel(col_label, multialignment='center', size='large')
    return im, cbar


def format_ticks(ticks, axis_min, axis_max):
    while ticks[0] < axis_min:
        ticks = np.delete(ticks, 0, axis=0)
    if ticks[0] != axis_min:
        ticks = np.insert(ticks, 0, axis_min, axis=0)

    while ticks[-1] > axis_max:
        ticks = np.delete(ticks, -1, axis=0)
    return ticks
