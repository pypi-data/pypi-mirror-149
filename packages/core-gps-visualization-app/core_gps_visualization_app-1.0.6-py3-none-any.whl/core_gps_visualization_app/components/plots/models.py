"""
Plots models
"""

from django_mongoengine import fields, Document
from core_gps_visualization_app.utils import parser


class Configurations(Document):
    """ Data Structure to handle Plots configurations

    """
    x_parameter = fields.StringField(blank=True)
    y_parameter = fields.StringField(blank=True)
    data_sources = fields.ListField(blank=True)

    @staticmethod
    def create_configurations(x_parameter, y_parameter, data_sources):
        """
        Returns:

        """
        return Configurations.objects.create(x_parameter=x_parameter, y_parameter=y_parameter, data_sources=data_sources)

    def update_configurations(self, x_parameter, y_parameter, data_sources):
        """

        Returns:

        """
        self.x_parameter = x_parameter
        self.y_parameter = y_parameter
        self.data_sources = data_sources
        self.save()

    @staticmethod
    def get_configurations():
        """ Unique object configuration
        Returns:

        """
        return Configurations.objects.all()[0]


class Plots(Document):
    """ Data Structure to optimize Plots interactions

    """
    plots_data = fields.ListField(blank=True)
    # [{'x_parameter': x}, {'y_parameter': y}, {'data_sources': [data_sources]}]
    config = fields.ListField(blank=True)
    part = fields.IntField(blank=True)

    def get_plots_data(self):
        """

        Returns: plots list

        """
        return self.plots_data

    @staticmethod
    def create_plots(list_of_charts, config):
        """

        Args:
            list_of_charts:
            config:

        Returns:

        """
        part = 1
        # Slice bigger documents in chunks that we add in the DB
        if parser.get_size(list_of_charts) > 1000000:
            sub_list_of_charts = []
            for i in range(0, len(list_of_charts)):
                if parser.get_size(sub_list_of_charts + [list_of_charts[i]]) < 1000000:
                    sub_list_of_charts.append(list_of_charts[i])
                    i += 1
                else:
                    # len is 0 means one dict elt of the list of charts is beyond the limit
                    if len(sub_list_of_charts) == 0:
                        dict_chart = list_of_charts[i]
                        data = dict_chart['data']
                        data_part = []
                        for elt in data:
                            if parser.get_size(data_part + [elt]) < 1000000:
                                data_part.append(elt)
                            else:
                                sub_list_of_charts = [{'x': dict_chart['x'], 'y': dict_chart['y'],
                                                       'ids': dict_chart['ids'], 'data': data_part
                                                       }]
                                Plots.objects.create(plots_data=sub_list_of_charts, config=config,
                                                     part=part)
                                part += 1
                                data_part = [elt]
                    else:
                        Plots.objects.create(plots_data=sub_list_of_charts, config=config, part=part)
                        part += 1
                        sub_list_of_charts = [list_of_charts[i]]

        else:
            return Plots.objects.create(plots_data=list_of_charts, config=config)

    @staticmethod
    def get_plots(config):
        return Plots.objects.filter(config=config)

