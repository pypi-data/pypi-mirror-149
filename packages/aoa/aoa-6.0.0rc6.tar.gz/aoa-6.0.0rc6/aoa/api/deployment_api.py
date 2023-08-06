from __future__ import absolute_import

from aoa.api.iterator_base_api import IteratorBaseApi


class DeploymentApi(IteratorBaseApi):
    path = "/api/deployments/"
    type = "DEPLOYMENT"

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

        return self.generate_params(header_vars, header_vals)

    def find_by_archived(self, archived: bool = False, projection: str = None, page: int = None, size: int = None, sort: str = None):
        raise NotImplemented("Archiving not supported for Deployments")

    def find_active_by_trained_model_and_engine_type(self, trained_model_id: str, engine_type: str, projection: str = None):
        """
        returns deployments by trained model and engine type

        Parameters:
           trained_model_id (str): trained model id(string) to find
           engine_type (str): engine type(string) to find
           projection (str): projection type

        Returns:
            (dict): deployments
        """
        query_vars = ['trainedModelId', 'engineType', 'projection']
        query_vals = [trained_model_id, engine_type, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            path=self.path + "search/findActiveByTrainedModelIdAndEngineType",
            header_params=self._get_header_params(),
            query_params=query_params)

    def find_by_status(self, status: str, projection: str = None):
        """
        returns deployments by status
        Parameters:
           status (str): status(string) to find
           projection (str): projection type
        Returns:
            (dict): deployments
        """
        query_vars = ['status', 'projection']
        query_vals = [status, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            path=self.path + "search/findByStatus",
            header_params=self._get_header_params(),
            query_params=query_params)

    def find_active(self, projection: str = None):
        """
        returns active deployments
        Parameters:
           projection (str): projection type
        Returns:
            (dict): deployments
        """
        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            path=self.path + "search/findActive",
            header_params=self._get_header_params(),
            query_params=query_params)
