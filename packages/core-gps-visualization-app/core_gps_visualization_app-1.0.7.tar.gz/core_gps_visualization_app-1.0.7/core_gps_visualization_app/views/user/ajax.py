from django.http import HttpResponseBadRequest, HttpResponse
import json

from core_gps_visualization_app.components.plots import api as plots_api
from bokeh.embed import server_document


def load_initial_plots(request):
    """ load layout plots into the visualization page

    Args:
        request:

    Returns:
    """
    try:
        script = server_document(request.build_absolute_uri())

        # Re-initialize dropdown buttons
        # plots_types = SelectPlotDropDown().fields['plots'].choices
        # time_ranges = SelectTimeRangeDropDown().fields['time_ranges'].choices
        # initial_plot_selected = plots_types[0][0]
        # initial_time_range_selected = time_ranges[0][0]
        # plots_api.update_plot_selected(plots_object, initial_plot_selected)
        # plots_api.update_time_range_selected(plots_object, initial_time_range_selected)

        return HttpResponse(json.dumps({'script': script}), content_type='application/json')

    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type='application/javascript')


def update_configurations(request):
    """ Update chart on validate click

    Args:
        request:

    Returns:
    """
    try:
        x_parameter = request.POST.get('x_parameter', None)
        y_parameter = request.POST.get('y_parameter', None)
        data_sources = request.POST.getlist('data_sources[]', None)

        # update configurations
        plots_api.update_configurations(x_parameter, y_parameter, data_sources)

        print(x_parameter)
        print(y_parameter)
        print(data_sources)

        return HttpResponse(json.dumps({}), content_type='application/json')

    except Exception as e:
        return HttpResponseBadRequest(str(e), content_type='application/javascript')


def update_chart(request):
    """

    Args:
        request:

    Returns:

    """
    script = server_document(request.build_absolute_uri())

    return HttpResponse(json.dumps({'script': script}), content_type='application/json')