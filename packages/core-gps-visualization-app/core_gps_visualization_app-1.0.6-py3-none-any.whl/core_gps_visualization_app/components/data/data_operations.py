"""Visualization Data Operations"""

from core_gps_visualization_app import data_config as data_config
from core_gps_visualization_app.utils import data_utils as utils
from core_gps_visualization_app.data_config import info_id_legend

import logging

logger = logging.getLogger(__name__)


def parse_data(all_data, x_parameter, y_parameter, data_sources, legend_ids):
    """ Parse data from the DB that match the configuration
    into a list of charts that are ready to be plotted (and overlaid)

    Args:
        data_sources: data sources selected on UI configurations
        legend_ids: legend elements selected on UI configurations
        y_parameter: y selected on UI configurations
        x_parameter: x selected on UI configurations
        all_data: List of all XML documents (under JSON format)

    Returns: List of dicts that each represent one plot (check tests for more details)

    """
    # Instantiate list to return
    logger.info("Periodic task: START parsing data")

    list_of_charts = []

    # data config instantiate
    info_parameters = data_config.info_parameters
    list_parameters = data_config.list_parameters
    ids_parameters = data_config.ids_parameters

    # If x is time (so x is already in every document along with y)
    # x of the document = x selected in configurations = variable from config file
    if x_parameter == data_config.variable:
        charts_to_overlay = []
        x_display_name = x_parameter
        for xml_file in all_data:
            dict_content = xml_file['dict_content']
            data_source = utils.get_value_by_path(dict_content, data_config.info_data_source['dataSourcePath'])
            legend_id = utils.get_value_by_path(dict_content, data_config.info_id_legend['legendPath'])
            legend_id_name = info_id_legend['legendName'] + ': ' + str(legend_id)

            # If legend path in this document, it has to contain a legend id from legend ids
            if (not utils.is_legend_id_in_document(dict_content, data_config.info_id_legend['legendPath'])) or (legend_id_name in legend_ids):
                # Only check documents that come from a selected data source
                if data_source in data_sources:
                    parameter_name = utils.get_value_by_path(dict_content, info_parameters['parameterNamePath'])

                    # 1 file = 1 group = 1 chart
                    if parameter_name == y_parameter:
                        y_display_name = utils.get_display_name(y_parameter, list_parameters)
                        y_unit = utils.get_value_by_path(dict_content, info_parameters['parameterUnitPath'])
                        data = utils.get_chart_data(dict_content, data_config.info_parameters)
                        ids = utils.get_parameter_ids(dict_content, ids_parameters)
                        part = utils.get_value_by_path(dict_content, info_parameters['parameterPartPath'])
                        if part is None:
                            part = 0

                        chart_dict = {
                            'x': (x_display_name, None),
                            'y': (y_display_name, y_unit),
                            'ids': ids,
                            'data': data,
                            'part': part
                        }

                        charts_to_overlay.append(chart_dict)

        # Sort charts to overlay by part
        sorted(charts_to_overlay, key=lambda i: i['part'])

        # if not split file detected
        if [chart['part'] == 0 for chart in charts_to_overlay]:
            for chart in charts_to_overlay:
                list_of_charts.append(chart)

        # Several Parts (total data would make xml file > 16GB so it is split in parts)
        else:
            chart_dict_temp = {}

            # Sort charts by ids
            for chart in charts_to_overlay:
                if (tuple(sorted(chart['ids']))) in chart_dict_temp:
                    chart_dict_temp[tuple(sorted(chart['ids']))].append(chart)
                else:
                    chart_dict_temp[tuple(sorted(chart['ids']))] = [chart]

            # Merge parts
            for chart_ids_tuples in chart_dict_temp:
                data = []
                for chart_part in sorted(chart_dict_temp[chart_ids_tuples], key=lambda l: l['part']):
                    data += chart_part['data']

                list_of_charts.append({
                    'x': chart_part['x'],
                    'y': chart_part['y'],
                    'ids': list(chart_ids_tuples),
                    'data': data
                })

    # For now we do not support split files (parts) if x is not the Variable
    # Every chart that hasn't time (or Variable) as x:
    else:
        all_x_dicts = []
        all_y_dicts = []
        # Check all files
        # For every file, if x/y then all its data are added to all_x_dicts/all_y_dicts
        for xml_file in all_data:
            dict_content = xml_file['dict_content']
            data_source = utils.get_value_by_path(dict_content, data_config.info_data_source['dataSourcePath'])
            legend_id = utils.get_value_by_path(dict_content, data_config.info_id_legend['legendPath'])
            legend_id_name = info_id_legend['legendName'] + ': ' + str(legend_id)

            # If legend path in this document, it has to contain a legend id from legend ids
            if (not utils.is_legend_id_in_document(dict_content, data_config.info_id_legend['legendPath'])) or (legend_id_name in legend_ids):

                # Only check documents that come from a selected data source
                if data_source in data_sources:
                    parameter_name = utils.get_value_by_path(dict_content, info_parameters['parameterNamePath'])

                    # 1 file for 1 group for 1 chart
                    if parameter_name == x_parameter:
                        x_display_name = utils.get_display_name(x_parameter, list_parameters)
                        x_unit = utils.get_value_by_path(dict_content, info_parameters['parameterUnitPath'])
                        x_data = dict(utils.get_chart_data(dict_content, data_config.info_parameters))
                        x_ids = utils.get_parameter_ids(dict_content, ids_parameters)
                        part = utils.get_value_by_path(dict_content, info_parameters['parameterPartPath'])
                        if part is None:
                            part = 0

                        x_dict = {
                            'x': (x_display_name, x_unit),
                            'ids': x_ids,
                            'data': x_data,  # [{var1: x1}, {var2: x2}, etc]
                            'part': part
                        }

                        all_x_dicts.append(x_dict)

                    # 1 file for 1 group for 1 chart
                    if parameter_name == y_parameter:
                        y_display_name = utils.get_display_name(y_parameter, list_parameters)
                        y_unit = utils.get_value_by_path(dict_content, info_parameters['parameterUnitPath'])
                        y_data = dict(utils.get_chart_data(dict_content, data_config.info_parameters))
                        y_ids = utils.get_parameter_ids(dict_content, ids_parameters)
                        part = utils.get_value_by_path(dict_content, info_parameters['parameterPartPath'])
                        if part is None:
                            part = 0

                        y_dict = {
                            'y': (y_display_name, y_unit),
                            'ids': y_ids,
                            'data': y_data,
                            'part': part
                        }

                        all_y_dicts.append(y_dict)

        # Merge x and y
        for x_dict in all_x_dicts:
            for y_dict in all_y_dicts:
                # 1 chart per group
                if utils.is_same_group(x_dict, y_dict) and x_dict['part'] == y_dict['part']:
                    data = []
                    for k in sorted(x_dict['data']):
                        if k in y_dict['data']:
                            data.append((x_dict['data'][k], y_dict['data'][k]))
                    ids = x_dict['ids']
                    for id_elt in y_dict['ids']:
                        if id_elt not in ids:
                            ids.append(id_elt)

                    chart_dict = {
                        'x': (x_dict['x'][0], x_dict['x'][1]),
                        'y': (y_dict['y'][0], y_dict['y'][1]),
                        'ids': ids,
                        'data': data
                    }

                    list_of_charts.append(chart_dict)
                    
    logger.info("Periodic task: FINISH parsing data")
    return list_of_charts

