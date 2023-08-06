"""GPS Visualization user views"""

from core_main_app.utils.rendering import render
from core_gps_visualization_app.views.user import forms
from core_gps_visualization_app.utils import data_utils as utils
from core_gps_visualization_app.components.plots import api
from core_gps_visualization_app.components.data import api as data_api

from core_main_app.components.data.models import Data
from core_main_app.system import api as sysapi
from core_main_app.settings import DATA_SORTING_FIELDS
import json


def index(request):
    """ GPS Visualization homepage

    Args:
        request:

    Returns:

    """
    variable = utils.get_variable()
    parameters = utils.get_parameters()
    x_parameters = variable + parameters
    y_parameters = parameters
    data_sources = data_api.get_data_sources()
    
    select_x_parameter = forms.SelectXParameterDropDown(x_parameters)
    select_y_parameter = forms.SelectYParameterDropDown(y_parameters)
    select_data_source = forms.SelectDataSourceCheckBox(data_sources)

    # Default configurations
    api.update_configurations(x_parameters[0][0], y_parameters[0][0], data_sources)

    context = {
        'x_parameter': select_x_parameter,
        'y_parameter': select_y_parameter,
        'data_source': select_data_source
    }

    assets = {
        "css": ["core_gps_visualization_app/user/css/main.css"],
        "img": ["core_gps_visualization_app/user/img/loading.gif"],
        "js": [
            {
                "path": 'core_gps_visualization_app/user/js/load_initial_plots.js',
                "is_raw": False
            },
            {
                "path": 'core_gps_visualization_app/user/js/select_chart_form.js',
                "is_raw": False
            },
            {
                "path": 'core_gps_visualization_app/user/js/update_chart.js',
                "is_raw": False
            }
        ]
    }

    return render(request, "core_gps_visualization_app/user/gps_visualization.html",
                  assets=assets,
                  context=context)
