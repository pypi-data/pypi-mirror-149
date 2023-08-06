from aoa.cli.base_model import BaseModel
from aoa.context.model_context import ModelContext, DatasetInfo
import json
import os
import importlib
import logging
import shutil
import sys


class ScoreModel(BaseModel):

    def __init__(self, repo_manager):
        super().__init__(repo_manager)
        self.logger = logging.getLogger(__name__)

    def batch_score_model_local(self,
                                model_id: str = None,
                                base_path: str = None,
                                rendered_dataset: dict = None):
        base_path = self.repo_manager.model_catalog_path if base_path is None else os.path.join(base_path, '')
        model_definitions_path = base_path + 'model_definitions/'

        if not os.path.exists(model_definitions_path):
            raise ValueError("model directory {0} does not exist".format(model_definitions_path))

        model_artefacts_path = ".artefacts/{}".format(model_id)

        if not os.path.exists("{}/output".format(model_artefacts_path)):
            raise ValueError("You must run training before trying to run scoring.")

        try:
            self.__cleanup()

            os.makedirs("./artifacts")

            os.symlink("../{}/output/".format(model_artefacts_path), "./artifacts/input", target_is_directory=True)

            # legacy models folder
            if not os.path.exists("./models"):
                os.symlink("{}/output".format(model_artefacts_path), "./models", target_is_directory=True)

            model_dir = model_definitions_path + BaseModel.get_model_folder(model_definitions_path, model_id)

            with open(model_dir + "/model.json", 'r') as f:
                model_definition = json.load(f)

            with open(model_dir + "/config.json", 'r') as f:
                model_conf = json.load(f)

            self.logger.info("Loading and executing model code")

            cli_model_kargs = {
                "model_id": model_id,
                "model_version": "cli",
                "model_table": "AOA_MODELS_cli",
                "project_id": self._BaseModel__get_project_id()
            }

            context = ModelContext(dataset_info=DatasetInfo.from_dict(rendered_dataset),
                                   hyperparams=model_conf["hyperParameters"],
                                   artefact_input_path="artifacts/input",
                                   **cli_model_kargs)

            engine = self._BaseModel__get_engine(model_definition, "deployment")
            if engine == "python" or engine == "pyspark":
                sys.path.append(model_dir)
                scoring = importlib.import_module(".scoring", package="model_modules")

                scoring.score(context=context,
                              data_conf=rendered_dataset,
                              model_conf=model_conf,
                              **cli_model_kargs)

            elif engine == "sql":
                raise Exception("not supported")

            elif engine == "R":
                self._BaseModel__run_r_model(model_id, base_path, rendered_dataset, "score.batch")

            else:
                raise Exception("Unsupported language: {}".format(model_definition["language"]))

            self.__cleanup()
        except ModuleNotFoundError:
            model_dir = model_definitions_path + BaseModel.get_model_folder(model_definitions_path, model_id)
            self.__cleanup()
            self.logger.error("Missing required python module, try running following command first:")
            self.logger.error("pip install -r {}/model_modules/requirements.txt".format(model_dir))
            raise
        except:
            self.__cleanup()
            self.logger.exception("Exception running model code")
            raise

    def __cleanup(self):
        if os.path.exists("./artifacts"):
            shutil.rmtree("./artifacts")
        try:
            os.remove("./models")
        except FileNotFoundError:
            self.logger.debug("Nothing to remove, folder './models' does not exists.")
