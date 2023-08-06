from core_gps_visualization_app.components.plots.models import Plots, Configurations


def configurations_exist():
    """

    Returns:

    """
    if len(Configurations.objects.all()) == 0:
        return False
    return True


def create_configurations(x_parameter, y_parameter, data_sources):
    """

    Args:
        x_parameter:
        y_parameter:
        data_sources:

    Returns:

    """
    return Configurations.create_configurations(x_parameter, y_parameter, data_sources)


def update_configurations(x_parameter, y_parameter, data_sources):
    """

    Args:
        x_parameter:
        y_parameter:
        data_sources:

    Returns:

    """
    if configurations_exist():
        configurations = get_configurations()
        return configurations.update_configurations(x_parameter, y_parameter, data_sources)
    else:
        return create_configurations(x_parameter, y_parameter, data_sources)


def get_configurations():
    return Configurations.get_configurations()


def get_x_parameter():
    configurations = get_configurations()
    return configurations.x_parameter


def get_y_parameter():
    configurations = get_configurations()
    return configurations.y_parameter


def get_data_sources():
    configurations = get_configurations()
    return configurations.data_sources


def create_plots(list_of_charts, x_parameter, y_parameter, data_sources):
    """

    Args:
        list_of_charts:
        x_parameter:
        y_parameter:
        data_sources:

    Returns:

    """
    config = [{'x_parameter': x_parameter}, {'y_parameter': y_parameter}, {'data_sources': data_sources}]
    return Plots.create_plots(list_of_charts, config)


def get_plots_data(x_parameter, y_parameter, data_sources):
    """

    Returns:

    """
    data = []  # list of chart dicts
    config = [{'x_parameter': x_parameter}, {'y_parameter': y_parameter}, {'data_sources': data_sources}]
    plots_objects = get_plots(config=config)

    # if more than a document, we have to merge them
    if len(plots_objects) > 1:
        ids = []
        for plots_object in plots_objects:
            plots_data_list = Plots.get_plots_data(plots_object)
            for plots_data_dict in plots_data_list:
                # Plots data sharing same ids had to be split in several docs
                if plots_data_dict['ids'] in ids:
                    for data_dict in data:
                        if data_dict['ids'] == plots_data_dict['ids']:
                            data_dict['data'] += plots_data_dict['data']
                # plots data sharing only config had to be split in several docs
                else:
                    data.append(plots_data_dict)
                    ids.append(plots_data_dict['ids'])

    else:
        data = Plots.get_plots_data(plots_objects[0])
    return data


def get_plots(config):
    """

    Returns: list of plots objects

    """
    return Plots.get_plots(config)


def plots_exist(x_parameter, y_parameter, data_sources):
    """

    Args:
        x_parameter:
        y_parameter:
        data_sources:

    Returns:

    """
    config = [{'x_parameter': x_parameter}, {'y_parameter': y_parameter}, {'data_sources': data_sources}]
    if len(Plots.objects.filter(config=config)) == 0:
        return False
    return True

