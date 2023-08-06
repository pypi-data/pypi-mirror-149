from __future__ import absolute_import

from aoa.api.iterator_base_api import IteratorBaseApi


class JobApi(IteratorBaseApi):
    path = "/api/jobs/"
    type = "JOB"

    def find_by_archived(self, archived: bool = False, projection: str = None, page: int = None, size: int = None, sort: str = None):
        raise NotImplemented("Archiving not supported for Jobs")

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

    def find_job_events(self, job_id: str, projection: str = None):
        """
        returns events of a job

        Parameters:
           job_id (str): job id(uuid) to find events
           projection (str): projection type

        Returns:
            (dict): job events
        """
        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            path=self.path + job_id + '/events',
            header_params=self._get_header_params(),
            query_params=query_params)

    def find_by_job_event_id(self, job_id: str, job_event_id: str, projection: str = None):
        """
        returns job event

        Parameters:
           job_id (str): job id(uuid)
           job_event_id (str): job event id(uuid)
           projection (str): projection type

        Returns:
            (dict): job event
        """
        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            path=self.path + job_id + '/events/' + job_event_id,
            header_params=self._get_header_params(),
            query_params=query_params)

    def find_job_between_intervals(self, start_time: str, end_time: str,
                                   projection: str = None):
        """
        returns job events within the timestamp range

        Parameters:
           start_time (str): start time e.g: 2020-03-18T09:05:03.569Z
           end_time (str): end time e.g: 2020-03-24T09:05:03.569Z
           projection (str): projection type

        Returns:
            (dict): job events
        """
        query_vars = ['startAt', 'endAt', 'projection']
        query_vals = [start_time, end_time, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            path=self.path + "search/findByCreatedAtBetween",
            header_params=self._get_header_params(),
            query_params=query_params)

    def find_by_status(self, status: str, projection: str = None, page: int = None, size: int = None,
                       sort: str = None):
        """
        returns job by status

        Parameters:
           status (str): job status
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): job events
        """
        query_vars = ['status', 'projection', 'page', 'sort', 'size']
        query_vals = [status, projection, page, sort, size]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            path=self.path + 'search/findByStatusIn',
            header_params=self._get_header_params(),
            query_params=query_params)

    def wait(self, job_id: str, timeout_sec: int = 60):
        import time

        start_time_sec = int(time.time())

        while True:
            job = self.find_by_id(id=job_id, projection="expandJob")
            status = job["status"]

            if status == 'COMPLETED':
                return
            elif not status or status in ["ERROR", "CANCELLED"]:
                raise Exception("Job failed with status: {}".format(status))

            if int(start_time_sec) - start_time_sec > timeout_sec:
                raise Exception("Timeout waiting for job to complete. Current status: {}".format(status))

            time.sleep(5)
