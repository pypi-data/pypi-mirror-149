from __future__ import absolute_import
from typing import List
from aoa.api.base_api import BaseApi

import requests
import uuid
import os


class TrainedModelArtefactsApi(BaseApi):

    def _get_header_params(self):
        header_vars = ['AOA-Project-ID', 'Content-Type', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            'application/json',
            'application/json']

        return self.generate_params(header_vars, header_vals)

    def list_artefacts(self, trained_model_id: uuid):
        """
        returns all trained models

        Parameters:
           trained_model_id (uuid): Trained Model Id

        Returns:
            (list): all trained model artefacts
        """

        return self.aoa_client.get_request(
            path="/api/trainedModels/{}/artefacts/listObjects".format(trained_model_id),
            header_params=self._get_header_params(),
            query_params={})["objects"]

    def get_signed_download_url(self, trained_model_id: uuid, artefact: str):
        """
        returns a signed url for the artefact

        Parameters:
           trained_model_id (uuid): Trained Model Id
           artefact (str): The artefact to generate the signed url for

        Returns:
            (str): the signed url
        """
        query_params = self.generate_params(['objectKey'], [artefact])

        response = self.aoa_client.get_request(
            path="/api/trainedModels/{}/artefacts/signedDownloadUrl".format(trained_model_id),
            header_params=self._get_header_params(),
            query_params=query_params)

        return response["endpoint"]

    def get_signed_upload_url(self, trained_model_id: uuid, artefact: str):
        """
        returns a signed url for the artefact

        Parameters:
           trained_model_id (uuid): Trained Model Id
           artefact (str): The artefact to generate the signed url for

        Returns:
            (str): the signed url
        """
        query_params = self.generate_params(['objectKey'], [artefact])

        response = self.aoa_client.get_request(
            path="/api/trainedModels/{}/artefacts/signedUploadUrl".format(trained_model_id),
            header_params=self._get_header_params(),
            query_params=query_params)

        return response["url"]

    def download_artefacts(self, trained_model_id: uuid, path: str = "."):
        """
        downloads all artefacts for the given trained model

        Parameters:
           trained_model_id (uuid): Trained Model Id
           path (str): the path to download the artefacts to (default cwd)

        Returns:
            None
        """

        for artefact in self.list_artefacts(trained_model_id):
            response = self.aoa_client.session.get(self.get_signed_download_url(trained_model_id, artefact))

            output_file = "{}/{}".format(path, artefact)
            if not os.path.exists(os.path.dirname(output_file)):
                os.makedirs(os.path.dirname(output_file))

            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    f.write(chunk)

    def upload_artefacts(self, import_id: uuid, artefacts: List = None, artefacts_folder: str = None):
        """
        uploads artefacts for the given trained model

        Parameters:
           import_id (uuid): Trained Model Id
           artefacts (List): The artefact paths to upload (must specify this or artefacts_folder)
           artefacts_folder (str): The artefact folder (must specify this or artefacts list)
        Returns:
            None
        """

        if artefacts is None and artefacts_folder is None:
            raise ValueError("Either artefacts or artefacts_folder argument must be specified")

        if artefacts is not None:
            for artefact in artefacts:
                object_key = os.path.basename(artefact)
                self.__upload_artefact(artefact, object_key, import_id)

        else:
            for root, d, files in os.walk(artefacts_folder):
                for file in files:
                    object_key = os.path.relpath(os.path.join(root, file), artefacts_folder)
                    self.__upload_artefact(os.path.join(root, file), object_key, import_id)

    def __upload_artefact(self, artefact, object_key, import_id):
        query_params = {
            'objectKey': object_key
        }
        header_params = {
            'AOA-Project-ID': "{}".format(self.aoa_client.project_id)
        }
        signed_url = self.aoa_client.get_request("/api/trainedModels/{}/artefacts/signedUploadUrl"
                                                 .format(import_id), header_params, query_params)
        upload_resp = requests.put(signed_url['endpoint'], data=open(artefact, 'rb'))
        upload_resp.raise_for_status()
