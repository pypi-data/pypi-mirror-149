import json
import uuid
import collections
import os
import shutil
import logging
import yaml

from pathlib import Path
from git import Repo
from aoa.cli.train_model import TrainModel
from aoa.cli.evaluate_model import EvaluateModel
from aoa.cli.score_model import ScoreModel


class RepoManager(object):

    def __init__(self, base_path: str, repo_template_catalog: str = None):
        self.base_path = base_path
        self.dir_path, _ = os.path.split(__file__)
        self.template_catalog = os.path.join(self.dir_path, 'model_templates/')
        self.repo_template_catalog = repo_template_catalog
        self.model = collections.OrderedDict()
        self.model_catalog_path = os.path.join(base_path, '')
        self.model_template = "empty"
        self.logger = logging.getLogger(__name__)

    def add_model(self, model_name: str, model_desc: str, lang: str,
                  template: str, base_path: str = None):

        base_path = self.model_catalog_path if base_path is None else os.path.join(base_path, '')
        model_path = os.path.join(base_path + 'model_definitions/', '')

        if not os.path.isdir(model_path):
            raise ValueError("model directory {0} does not exist".format(model_path))

        self.model["id"] = str(uuid.uuid4())
        self.model["name"] = model_name
        self.model["description"] = model_desc
        self.model["language"] = lang

        self.model_template = template

        self.__create_model_structure(model_path)

    @staticmethod
    def clone_repository(url, path, branch: str = 'master'):
        repo = Repo.clone_from(url, path)
        repo.git.checkout(branch)

    def init_model_directory(self, path: str = None):
        logging.info('Creating model directory')
        if path is None:
            path = os.path.join(os.path.abspath(os.getcwd()), '')

        self.logger.info('Creating model definitions')

        src = os.path.join(os.path.split(__file__)[0], '') + 'metadata_files'
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if os.path.isfile(full_file_name) and not os.path.exists(os.path.join(path, file_name)):
                shutil.copy(full_file_name, path)

        Path(path + "model_definitions/").mkdir(parents=True, exist_ok=True)
        Path(path + "model_templates/").mkdir(parents=True, exist_ok=True)

        self.logger.info("model directory initialized at {0}".format(path))

    def __create_model_structure(self, model_path):
        # check if model template exists in templates catalog passed and use that as override if it does. if not, use
        # defaut version in the package template
        model_template_path = os.path.join(self.repo_template_catalog, '') \
                                   + self.model["language"] + "/" + self.model_template

        if os.path.exists(model_template_path):
            template_dir = model_template_path
        else:
            template_dir = self.template_catalog + self.model["language"] + "/" + self.model_template

        model_dir = model_path + self.model["id"]
        shutil.copytree(template_dir, model_dir)

        Path(model_dir + "/notebooks").mkdir(exist_ok=True)

        with open(model_dir + "/model.json", 'w') as f:
            json.dump(self.model, f, indent=4)

    def get_all_template_catalog(self):
        cat, custom_cat = {}, {}

        if self.repo_template_catalog is not None and os.path.exists(self.repo_template_catalog):
            custom_cat = self.__get_template_catalog(self.repo_template_catalog)

        cat = self.__get_template_catalog(self.template_catalog)

        return cat, custom_cat

    def __get_template_catalog(self, model_template_path):
        catalog = {}

        sub_folders = [f for f in os.listdir(model_template_path)
                       if os.path.isdir(os.path.join(model_template_path, f))
                       & (f[0] != '.') & (f.lower() != 'readme.md')]

        for language in sub_folders:
            language_dir = os.path.join(model_template_path, language)
            catalog[language] = []
            for template_type in os.listdir(language_dir):
                if template_type[0] != '.' and template_type.lower() != 'readme.md':
                    catalog[language].append(template_type)
        return catalog

    def read_repo_config(self):
        path = os.path.join(self.base_path, ".aoa/config.yaml")
        if os.path.exists(path):
            with open(path, "r") as handle:
                return yaml.safe_load(handle)

        self.logger.warning("Aoa repo config doesn't exist")
        return None

    def write_repo_config(self, config, path=None):
        path = path if path else self.base_path
        config_dir = os.path.join(path, ".aoa")
        Path(config_dir).mkdir(parents=True, exist_ok=True)
        config_file = "{}/config.yaml".format(config_dir)

        with open(config_file, 'w+') as f:
            yaml.dump(config, f, default_flow_style=False)

    def repo_config_exists(self, repo_path=None):
        path = repo_path if repo_path else self.base_path
        return Path(os.path.join(path, ".aoa")).is_file()

    def train(self, model_id: str, data_conf: dict):
        trainer = TrainModel(self)
        trainer.train_model_local(model_id=model_id, rendered_dataset=data_conf)

    def evaluate(self, model_id: str, data_conf: dict):
        evaluator = EvaluateModel(self)
        evaluator.evaluate_model_local(model_id=model_id, rendered_dataset=data_conf)

    def batch_score_model_local(self, model_id: str, data_conf: dict):
        scorer = ScoreModel(self)
        scorer.batch_score_model_local(model_id=model_id, rendered_dataset=data_conf)
