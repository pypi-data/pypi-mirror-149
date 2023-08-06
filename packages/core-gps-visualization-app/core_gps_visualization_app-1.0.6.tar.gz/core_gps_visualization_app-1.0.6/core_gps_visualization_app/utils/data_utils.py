""" Data Utils """ 

from datetime import datetime
from core_gps_visualization_app import data_config
from core_main_app.system import api as system_api
import time
import julian


def get_all_data():
    """ Get all data as is from the DB under JSON format (data follow the structure defined by a schema)

    Returns: dict

    """
    templates = system_api.get_all_templates()

    # Each data in the list contains a XML file content accessible through its dict_content attribute
    all_data = system_api.get_all_by_list_template(templates)

    return all_data

  
def query_data(path):
    """ Query a specific path, and put the results in a list

    Args:
        path:

    Returns:

    """
    #field = 'dict_content.data.parameterIds.satelliteID'
    field = 'dict_content.' + path
    query = {field: {'$exists': True}}
    results = []

    test = system_api.execute_query_with_projection(query, field)
    for data_object in test:
        result = get_value_by_path(data_object.dict_content, path)
        if result not in results:
            results.append(result)

    return results

  
def is_total_documents_changed(data_sources_documents):
    """ Compare the number of documents currently in the DB to the number of documents used by out Data source object

    Args:
        data_sources_documents:

    Returns:

    """
    all_data = get_all_data()
    current_documents = len(all_data)
    return current_documents != data_sources_documents

  
###TODO
def update_data_part(all_data, x_or_y_dict, part):
    # for data that are split in different files,
    # Make a list:  [part1, part2, etc] that is inside all_x_data
    # where part x_dict is part off all_x_data
    # and partX = {x_dict, part: X}
    return 0

  
###TODO
def combine_parts(all_data):
    # temp structure in function above must be transformed to be like
    # any other x/y dict
    return 0


def build_groups(x_ids, y_ids):
    ids = []
    for key in x_ids:
        if key in y_ids:
            if x_ids[key] == y_ids[key]:
                ids.append(x_ids[key])
        else:
            ids.append(x_ids[key])
    for key in y_ids:
        if key not in x_ids:
            ids.append(y_ids)

    return ids


def is_same_group(x_dict, y_dict):
    """ If x and y ids share same keys and values are different, then
    they're not from the same group

    """
    # Union all but two similar keys with different values
    same_group = True
    x_ids = x_dict['ids']
    y_ids = y_dict['ids']

    for x_ids_dict in x_ids:
        for y_ids_dict in y_ids:
            if x_ids_dict.keys() == y_ids_dict.keys():
                if x_ids_dict != y_ids_dict:
                    same_group = False

    return same_group


def build_chart(x_dict, y_dict):
    x_data = x_dict['data']
    y_data = y_dict['data']
    ids = build_groups(x_dict['ids'], y_dict['ids'])

    temp_data = zip(x_data, y_data)
    data = []
    for xy in temp_data:
        if None not in xy:
            data.append(xy)

    chart_dict = {
        'x': x_dict['x'],
        'y': y_dict['y'],
        'ids': ids,
        'data': data
    }

    return chart_dict


def parse_data(data):
    parsed = []
    # In Case we only have 1 data point
    if not isinstance(data, list):
        data = [data]
    for elt in data:
        parsed_elt = parse_number(elt)
        if not parsed_elt:
            parsed_elt = parse_date(elt)
            if not parsed_elt:
                parsed_elt = None
        if elt == 0:
            parsed_elt = None
        parsed.append(parsed_elt)

    return parsed


def parse_date(date_string):
    """

    Args:
        date_string: YYYY-mm-ddTHH:MM:SS

    Returns: datetime

    """
    try:
        year = date_string[:4]
        month = date_string[5:7]
        day = date_string[8:10]
        hours = date_string[11:13]
        mins = date_string[14:16]
        secs = date_string[17:19]
        parsed_date = datetime(int(year), int(month), int(day), int(hours), int(mins), int(secs))
        mjd_time = julian.to_jd(parsed_date) - 2400000.5 

    except ValueError:
        mjd_time = False
    except TypeError:
        mjd_time = False

    return mjd_time


def parse_number(value):
    """ Check if value is a number

    Args:
        value:

    Returns:

    """
    try:
        return float(value)
    except ValueError:
        return False
    except TypeError:
        return False


def get_value_by_path(dict_content, path):
    """ Recursive method to get a value inside a dict from a path.
    '.' defines a layer in the dict and '/' defines start of a list

    Args:
        dict_content:
        path:

    Returns:

    """
    path_list = path.split('.')

    if dict_content:
        if len(path_list) == 1 and path in dict_content:
            return dict_content[path]
        else:
            substr_length = len(path_list[0]) + 1  # +1 to substring the point
            if path_list[0] not in dict_content:
                return None
            else:
                get_value_by_path(dict_content[path_list[0]], path[substr_length:])
    return get_value_by_path(dict_content[path_list[0]], path[substr_length:])


def get_parameter_ids(dict_content, ids_parameters):
    ids = []
    for id_parameter in ids_parameters:
        id_value = get_value_by_path(dict_content, id_parameter['idPath'])
        id_name = id_parameter['idName']
        if id_value:
            ids.append({id_name: id_value})
    return ids


def is_legend_id_in_document(dict_content, id_legend_path):
    """

    Args:
        dict_content:
        id_legend_path:

    Returns:

    """
    id_legend_value = get_value_by_path(dict_content, id_legend_path)
    if id_legend_value is None:
        return False
    return True


def get_parameter_data(dict_content, list_parameters, parameter_name):
    found = False
    i = 0
    while not found:
        if list_parameters[i]['parameterName'] == parameter_name:
            found = True
            path = list_parameters[i]['valuesPath']
        i += 1
    value = get_value_by_path(dict_content, path)

    return value


def get_display_name(name, list_parameters):
    found = False
    i = 0
    while not found and i < len(list_parameters):
        if list_parameters[i]['parameterName'] == name:
            return list_parameters[i]['displayName']
        i += 1
    return None


def get_chart_data(dict_content, info_parameters):
    variable_path = info_parameters['variablePath']
    value_path = info_parameters['valuePath']

    values = parse_data(get_value_by_path(dict_content, value_path))
    variables = parse_data(get_value_by_path(dict_content, variable_path))

    data = list(zip(variables, values))

    for data_tuple in data:
        if None in data_tuple:
            data.remove(data_tuple)

    return data


def get_variable():
    variable = data_config.variable
    variable_tuple = (variable, variable)
    return [variable_tuple]


def get_parameters():
    result = []
    parameters = data_config.list_parameters
    for parameter_dict in parameters:
        result.append((parameter_dict['parameterName'], parameter_dict['displayName']))

    return result
