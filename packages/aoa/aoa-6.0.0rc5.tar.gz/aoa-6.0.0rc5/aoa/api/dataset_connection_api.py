from __future__ import absolute_import
from typing import Dict

from aoa.api.iterator_base_api import IteratorBaseApi


class DatasetConnectionApi(IteratorBaseApi):
    path = "/api/datasetConnections/"
    type = "DATASET_CONNECTION"

    def find_by_archived(self, archived: bool = False, projection: str = None, page: int = None, size: int = None, sort: str = None):
        raise NotImplemented("Archiving not supported for DatasetConnections")

    def _get_header_params(self):
        header_vars = ['AOA-Project-ID', 'Content-Type', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            'application/json',
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]

        return self.generate_params(header_vars, header_vals)

    def render_vars(self, dataset_connection_id: str):
        """
        returns dictionary with the env vars for a given dataset connection of a project

        Parameters:
           dataset_connection_id (str): dataset connection id(uuid) to find

        Returns:
            (dict): dataset connection envs
        """
        return self.aoa_client.get_request(
            path=self.path + dataset_connection_id + "/renderVars",
            header_params=self._get_header_params(),
            query_params={})

    def save(self, dataset_connection: Dict[str, str]):
        """
        register a dataset connection

        Parameters:
           dataset connection (dict): dataset connection to register

        Returns:
            (dict): dataset template
        """
        self.required_params(['name', 'description', 'type', 'metadata', 'credentials'], dataset_connection)

        query_params = {}

        return self.aoa_client.post_request(
            path=self.path,
            header_params=self._get_header_params(),
            query_params=query_params,
            body=dataset_connection)
