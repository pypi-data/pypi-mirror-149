import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def make_cycle_plot(
    follicle_data: pd.DataFrame,
    x_axis: str,
    y_axis: str,
    style_key: bool = None,
    plot_type: str = 'strip',
    hue: str = 'side',
    rotate_xlabel: bool = False,
    figsize: tuple = (20, 9),
    fontsize: int = 12,
):
    """plotting function which includes strip, line, scatter, box plots

    Parameters
    ----------
    follicle_data: pandas Dataframe
        The data needed to be plotted
    yaxis: str
        the name of column which include the values that are going to be used.
    xaxis: str
        variable of x axis such as relative day or day from peak
    style_key: str
        the style option.
    plot_type: str
        the plot type such as line, scatter, strip or box
    hue: str
        the way to separate data, such as side
    figsize: tuple
        the size of figure

    Returns
    -------
    f: Figure
        the plot
    axs: axes.Axes or array of Axes
        ax can be either a single Axes object or an array of Axes objects if more than one subplot was created.

    """
    f, axs = plt.subplots(1, 2, sharey=True, figsize=figsize)

    base_kwargs = {'x': x_axis, 'y': y_axis, 'hue': hue}
    if style_key is not None:
        base_kwargs.update({'style': style_key})

    z1_data = follicle_data.loc[follicle_data['cycle'] == 'z1']
    z1_kwargs = base_kwargs
    z1_kwargs.update({'data': z1_data, 'ax': axs[0]})
    if plot_type == 'strip':
        sns.stripplot(**z1_kwargs)
    elif plot_type == 'line':
        z1_kwargs.update({'legend': 'brief'})
        sns.lineplot(**z1_kwargs)
    elif plot_type == 'scatter':
        z1_kwargs.update({'alpha': 1})
        sns.scatterplot(**z1_kwargs)
    elif plot_type == 'box_strip':
        sns.stripplot(x=x_axis, y=y_axis, data=z1_data, ax=axs[0], color='.25')
        z1_kwargs.update({'palette': "Set3"})
        sns.boxplot(**z1_kwargs)
    elif plot_type == 'box':
        z1_kwargs.update({'palette': "Set3"})
        sns.boxplot(**z1_kwargs)

    z2_data = follicle_data.loc[follicle_data['cycle'] == 'z2']
    z2_kwargs = base_kwargs
    z2_kwargs.update({'data': z2_data, 'ax': axs[1]})
    if plot_type == 'strip':
        sns.stripplot(**z2_kwargs)
    elif plot_type == 'line':
        z1_kwargs.update({'legend': 'brief'})
        sns.lineplot(**z2_kwargs)
    elif plot_type == 'scatter':
        z2_kwargs.update({'alpha': 1})
        sns.scatterplot(**z2_kwargs)
    elif plot_type == 'box_strip':
        sns.stripplot(x=x_axis, y=y_axis, data=z2_data, ax=axs[1], color='.25')
        z2_kwargs.update({'palette': "Set3"})
        sns.boxplot(**z2_kwargs)
    elif plot_type == 'box':
        z2_kwargs.update({'palette': "Set3"})
        sns.boxplot(**z2_kwargs)

    # remove the right legend
    right_legend = axs[1].legend()
    right_legend.remove()

    # add cycle titles
    axs[0].set_xlabel('cycle 1', fontsize=fontsize)
    axs[1].set_xlabel('cycle 2', fontsize=fontsize)

    if rotate_xlabel:
        # rotate label
        axs[0].set_xticklabels(
            axs[0].get_xticklabels(),
            rotation=40,
            ha="right",
            fontsize=fontsize,
        )
        axs[1].set_xticklabels(
            axs[1].get_xticklabels(),
            rotation=40,
            ha="right",
            fontsize=fontsize,
        )

    # hide the vertical axis on the right plot
    axs[1].get_yaxis().set_visible(False)

    # remove the box
    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)

    axs[1].spines['left'].set_visible(False)
    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)

    f.tight_layout()

    return f, axs
