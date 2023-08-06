from __future__ import absolute_import
from typing import Dict

from aoa.api.iterator_base_api import IteratorBaseApi


class ProjectApi(IteratorBaseApi):

    path = "/api/projects/"
    type = "PROJECT"

    def _get_header_params(self):
        # The header for project id is required for the archive/unarchive method from base_api
        header_vars = ['AOA-Project-ID', 'Content-Type', 'Accept']
        header_vals = [self.aoa_client.project_id, 'application/json', 'application/json']

        return self.generate_params(header_vars, header_vals)

    def save(self, project: Dict[str, str]):
        """
        create a project

        Parameters:
           project (dict): project to create

        Returns:
            (dict): project
        """
        header_vars = ['Accept']
        header_vals = ['application/json']
        header_params = self.generate_params(header_vars, header_vals)

        query_params = {}

        self.required_params(['description', 'gitRepositoryUrl', 'groupId', 'name'], project)

        return self.aoa_client.post_request(
            self.path,
            header_params,
            query_params,
            project)

    def update(self, project: Dict[str, str]):
        """
        update a project

        Parameters:
           project (dict): project to update

        Returns:
            (dict): project
        """
        header_vars = ['Accept']
        header_vals = ['application/json']
        header_params = self.generate_params(header_vars, header_vals)

        query_params = {}

        self.required_params(['description', 'gitRepositoryUrl', 'groupId', 'name'], project)

        return self.aoa_client.put_request(
            self.path + self.aoa_client.project_id,
            header_params,
            query_params,
            project)

    def is_archived(self, project_id: str):
        """
        returns the archived status of a project
        Parameters:
           project_id (str): project id to check archived status
        Returns:
            (bool)
        """
        project = self.find_by_id(project_id)

        return project["archived"]
