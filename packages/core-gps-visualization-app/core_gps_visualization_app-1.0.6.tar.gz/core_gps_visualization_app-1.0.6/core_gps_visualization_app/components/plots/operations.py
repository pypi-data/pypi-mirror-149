import holoviews as hv
from core_main_app.commons import exceptions
from core_gps_visualization_app.utils.parser import stringify, unit_stringify
from core_gps_visualization_app.utils import parser as utils
from datashader.colors import Sets1to3
import holoviews.operation.datashader as hd
import datashader as ds
import numpy as np

count = 1


def plot_layout(plots_type, plots_data, vlines):
    """

    Args:
        plots_type:
        plots_data:
        vlines:

    Returns:

    """
    hv.extension('bokeh')

    if plots_type == 'Scatter':
        layout = plot_scatter(plots_data, vlines)
    if plots_type == 'Line':
        layout = plot_line(plots_data, vlines)

    try:
        return layout
    except Exception:
        raise exceptions.DoesNotExist("No plots type found!")


def plot_layout_by_time_range(plots_data, plots_type, time_range):
    """

    Args:
        plots_data:
        plots_type:
        time_range:

    Returns:

    """
    vlines = []
    for dict_data in plots_data:
        if dict_data['x'][0] == "Time (UTC)":
            min = int(dict_data['data'][0][0])
            max = int(dict_data['data'][-1][0])
            for i in range(min, max + 1):
                vlines.append(i)
            if time_range != "Seconds":
                dict_data['data'] = utils.parse_time_range_data(dict_data['data'], time_range)
    return plot_layout(plots_type, plots_data, vlines)


def plot_scatter(plots_data, vlines):
    """

    Args:
        plots_data:
        vlines:

    Returns:

    """
    plots = {}
    groups = []

    # All plots share same x and y so we can take the first one
    y_tuple = plots_data[0]['y']
    x_tuple = plots_data[0]['x']

    count = 0
    for plot in plots_data:
        count += 1
        # Define chart label
        label = ''
        if plot['ids'] is not None:
            for id_dict in plot['ids']:
                label += stringify(next(iter(id_dict.keys()))) + ': ' + stringify(next(iter(id_dict.values())))
                label += ' - '
            label = label[:-3]

        # List of labels to Identify groups
        groups.append(label)

        # define x and y labels
        x_unit_label = unit_stringify(plot['x'][1])
        y_unit_label = unit_stringify(plot['y'][1])

        # Create plot
        scatter_plot = hv.Scatter(np.array(plot['data']), stringify(plot['x'][0]) + x_unit_label,
                                  stringify(plot['y'][0]) + y_unit_label, label=label)

        #scatter_plot = hv.Points(np.array(plot['data']))

        # Add to list of plots
        plots[str(count)] = scatter_plot

    # len(Sets1to3) is 22, might be too small in some occurrences
    colors_list = Sets1to3 + ['#a3d0e4', '#89003e', '#38b29f', '#9c4578', '#3e1515', '#8f329f', '#f0535a',
                              '#a3b0e4', '#ff5393', '#d57aa8', '#ee846d', '#96858f']

    # Overlay all plots in a single chart
    overlaid_chart = hd.spread(hd.datashade(hv.NdOverlay(plots, kdims='k'), aggregator=ds.by('k', ds.count()), color_key=colors_list), px=4)

    # Datashader removes groups so we add artificial ones (cf. holoviews documentation)
    # len(Sets1to3) is 22, might be too small in some occurrences, now support up to 34 groups
    print('groups')
    print(groups)
    print('colors list')
    print(colors_list)
    color_key = [(group, color) for group, color in zip(groups, colors_list)]  # Attribute a group to a color
    color_points = hv.NdOverlay({k: hv.Points([0, 0], label=str(k)).opts(color=v, size=0) for k, v in color_key})

    #return overlaid_chart.opts(hv.opts.RGB(
    #    height=500,
    #    width=750,
   #     show_grid=True,
     #   title="Scatter: " + stringify(y_tuple[0]) + " against " + stringify(x_tuple[0])))  # * color_points)

    legend_chart = (overlaid_chart * color_points).opts(hv.opts.RGB(height=500, width=750, show_grid=True, title="Scatter: " + stringify(y_tuple[0]) + " against " + stringify(x_tuple[0])))

    if len(vlines) > 0:
        vline_chart = hv.VLine(vlines[0]).opts(color='black')
        for vline in vlines:
            vline_chart = vline_chart * hv.VLine(vline).opts(color='black')

        return legend_chart * vline_chart
    else:
        return legend_chart

def plot_line(plots_data, vlines):
    """

    Args:
        plots_data:
        vlines:

    Returns:

    """
    plots = {}
    groups = []

    # All plots share same x and y so we can take the first one
    y_tuple = plots_data[0]['y']
    x_tuple = plots_data[0]['x']

    for plot in plots_data:
        # Define chart label
        label = ''
        if plot['ids'] is not None:
            for id_dict in plot['ids']:
                label += stringify(next(iter(id_dict.keys()))) + ': ' + stringify(next(iter(id_dict.values())))
                label += ' - '
            label = label[:-3]

        # List of labels to Identify groups
        groups.append(label)

        # define x and y labels
        x_unit_label = unit_stringify(plot['x'][1])
        y_unit_label = unit_stringify(plot['y'][1])

        # Create plots
        line_plot = hv.Curve(np.array(plot['data']), stringify(plot['x'][0]) + x_unit_label,
                             stringify(plot['y'][0]) + y_unit_label, label=label)

        # Add to list of plots
        plots[label] = line_plot

    # Overlay all plots in a single chart
    overlaid_chart = hd.spread(hd.datashade(hv.NdOverlay(plots, kdims='k'), aggregator=ds.by('k', ds.count())), px=4)

    # Datashader removes groups so we add artificial ones (cf. holoviews documentation)
    # len(Sets1to3) is 22, might be too small in some occurrences
    colors_list = Sets1to3 + ['#a3d0e4', '#89003e', '#38b29f', '#9c4578', '#3e1515', '#8f329f', '#f0535a',
                              '#a3b0e4', '#ff5393', '#d57aa8', '#ee846d', '#96858f']
    color_key = [(group, color) for group, color in zip(groups, colors_list)]  # Attribute a group to a color
    color_points = hv.NdOverlay({k: hv.Points([0, 0], label=str(k)).opts(color=v, size=0) for k, v in color_key})

    legend_chart = (overlaid_chart.opts(hv.opts.RGB(height=500, width=750, show_grid=True,
                                           title="Line: " + str(y_tuple[0]) + " against " + str(x_tuple[0]))) * color_points)

    if len(vlines) > 0:
        vline_chart = hv.VLine(vlines[0]).opts(color='black')
        for vline in vlines:
            vline_chart = vline_chart * hv.VLine(vline).opts(color='black')
        return legend_chart * vline_chart
    else:
        return legend_chart


def plot_box(plots_data):
    """

    Args:
        plots_data:

    Returns:

    """
    box_plots = []
    for box_data_dict in plots_data:
        x_unit_label = unit_stringify(box_data_dict['x'][1])
        y_unit_label = unit_stringify(box_data_dict['y'][1])
        box_plot = hv.BoxWhisker(box_data_dict['data'], stringify(box_data_dict['x'][0])
                                 + x_unit_label,  stringify(box_data_dict['y'][0])
                                 + y_unit_label)
        box_plots.append(box_plot)
    layout = hv.Layout(box_plots).cols(1)
    layout.opts(hv.opts.BoxWhisker(width=1400, height=700))

    return layout




