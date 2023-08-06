__version__="6.0.0rc5"

# import client
from aoa.api_client import AoaClient

# import APIs into api package
from aoa.api.dataset_api import DatasetApi
from aoa.api.dataset_template_api import DatasetTemplateApi
from aoa.api.dataset_connection_api import DatasetConnectionApi
from aoa.api.model_api import ModelApi
from aoa.api.project_api import ProjectApi
from aoa.api.trained_model_api import TrainedModelApi
from aoa.api.trained_model_event_api import TrainedModelEventApi
from aoa.api.trained_model_artefacts_api import TrainedModelArtefactsApi
from aoa.api.job_api import JobApi
from aoa.api.job_event_api import JobEventApi
from aoa.api.deployment_api import DeploymentApi
from aoa.api.api_iterator import ApiIterator
from aoa.api.message_api import MessageApi

# import repo into api package
from aoa.cli.repo_manager import RepoManager
from aoa.cli.evaluate_model import EvaluateModel
from aoa.cli.score_model import ScoreModel
from aoa.cli.train_model import TrainModel
from aoa.cli.base_model import BaseModel

from aoa.context.model_context import *
from aoa.util import *
from aoa.stats.stats import *
from aoa.stats.store import *
