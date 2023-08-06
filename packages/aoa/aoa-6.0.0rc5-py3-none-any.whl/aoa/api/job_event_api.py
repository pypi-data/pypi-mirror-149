from __future__ import absolute_import

from aoa.api.iterator_base_api import IteratorBaseApi


class JobEventApi(IteratorBaseApi):

    path = "/api/jobEvents/"
    type = "JOB_EVENT"

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

    def find_all(self, projection: str = None, page: int = None, size: int = None, sort: str = None):
        """
        returns all job events

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all job events
        """
        query_vars = ['projection', 'page', 'sort', 'size', 'sort']
        query_vals = [projection, page, sort, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            path=self.path,
            header_params=self._get_header_params(),
            query_params=query_params)

    def find_by_id(self, job_event_id: str, projection: str = None):
        """
        returns a job event

        Parameters:
           job_event_id (str): job event id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): job event
        """
        query_vars = ['id', 'projection']
        query_vals = [job_event_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            path=self.path + "search/findById",
            header_params=self._get_header_params(),
            query_params=query_params)

    def find_by_job_id(self, job_id: str, projection: str = None, page: int = None, size: int = None,
                       sort: str = None):
        """
        returns events of a job

        Parameters:
           job_id (str): job id(uuid) to find events
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): job events
        """
        query_vars = ['jobId', 'projection', 'page', 'sort', 'size', 'sort']
        query_vals = [job_id, projection, page, sort, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            path=self.path + 'search/findByJobId',
            header_params=self._get_header_params(),
            query_params=query_params)
