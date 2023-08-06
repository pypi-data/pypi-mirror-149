from typing import List, Dict
import os


class DatasetInfo(object):

    def __init__(self, sql: str = None,
                 entity_key: str = None,
                 feature_names: List = None,
                 target_names: List = None,
                 feature_metadata: Dict = None,
                 predictions: Dict = None,
                 legacy_data_conf: Dict = None,
                 **kwargs):
        self.sql = sql
        self.entity_key = entity_key
        self.feature_names = feature_names
        self.target_names = target_names
        self.legacy_data_conf = legacy_data_conf

        if feature_metadata:
            self.feature_metadata_database = feature_metadata.get("database")
            self.feature_metadata_table = feature_metadata.get("table")
            self.feature_metadata_monitoring_group = feature_metadata.get("monitoringGroup")

        if predictions:
            self.predictions_database = predictions.get("database")
            self.predictions_table = predictions.get("table")

    @classmethod
    def from_dict(cls, rendered_dataset: Dict):
        if "type" in rendered_dataset and rendered_dataset["type"] == "CatalogBody":
            return cls(sql=rendered_dataset.get("sql"),
                       entity_key=rendered_dataset.get("entityKey"),
                       feature_names=rendered_dataset.get("featureNames"),
                       feature_metadata=rendered_dataset.get("featureMetadata"),
                       predictions=rendered_dataset.get("predictions"),
                       target_names=rendered_dataset.get("targetNames"))
        else:
            # set dict and legacy
            return cls(feature_metadata=rendered_dataset.get("featureMetadata"),
                       legacy_data_conf=rendered_dataset)

    def get_feature_metadata_fqtn(self):
        return f"{self.feature_metadata_database}.{self.feature_metadata_table}"

    def get_predictions_metadata_fqtn(self):
        return f"{self.predictions_database}.{self.predictions_table}"

    def is_legacy(self):
        return self.legacy_data_conf is not None


class ModelContext(object):

    def __init__(self, hyperparams: Dict,
                 dataset_info: DatasetInfo,
                 artefact_output_path: str = None,
                 artefact_input_path: str = None,
                 **kwargs):

        self.hyperparams = hyperparams
        self.artefact_output_path = artefact_output_path
        self.artefact_input_path = artefact_input_path
        self.dataset_info = dataset_info

        valid_var_keys = {"project_id", "model_id", "model_version", "job_id", "model_table"}
        for key in kwargs:
            if key in valid_var_keys:
                setattr(self, key, kwargs.get(key))

    @property
    def artefact_output_path(self):
        return self.__artefact_output_path

    @artefact_output_path.setter
    def artefact_output_path(self, artefact_output_path):
        if artefact_output_path and not os.path.isdir(artefact_output_path):
            raise ValueError(f"artefact_output_path ({artefact_output_path}) does not exist")

        self.__artefact_output_path = artefact_output_path

    @property
    def artefact_input_path(self):
        return self.__artefact_input_path

    @artefact_input_path.setter
    def artefact_input_path(self, artefact_input_path):
        if artefact_input_path and not os.path.isdir(artefact_input_path):
            raise ValueError(f"artefact_input_path ({artefact_input_path}) does not exist")

        self.__artefact_input_path = artefact_input_path

