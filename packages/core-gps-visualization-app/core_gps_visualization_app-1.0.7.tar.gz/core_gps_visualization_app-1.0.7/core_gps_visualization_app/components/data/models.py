"""
Data models
"""

from django_mongoengine import fields, Document
from core_gps_visualization_app import data_config
from core_gps_visualization_app.utils import data_utils as utils


class DataSources(Document):
    """ Data Structure to fill Django Form. Object is used to optimize loading time

    """
    data_sources = fields.ListField(blank=False)
    total_documents = fields.IntField(blank=False)

    @staticmethod
    def create_data_sources():
        """
        Returns: data source is a list of tuples

        """
        data_source_path = data_config.info_data_source['dataSourcePath']
        data_sources = utils.query_data(data_source_path)

        all_data = utils.get_all_data()
        total_documents = len(all_data)

        return DataSources.objects.create(data_sources=data_sources, total_documents=total_documents)

    @staticmethod
    def update_data_sources():
        """

        Returns:

        """
        DataSources.objects.all().delete()
        return DataSources.create_data_sources()

    @staticmethod
    def get_data_sources():
        """
        Returns:

        """
        if len(DataSources.objects.all()) == 0:
            DataSources.create_data_sources()
        data_sources_object = DataSources.objects.all()[0]
        return data_sources_object.data_sources
