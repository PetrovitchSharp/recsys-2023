from abc import ABC, abstractmethod
from typing import Any, List

from ..settings import ServiceConfig
from .utils import get_predictors_config


class BaseRecommender(ABC):
    def __init__(self, global_cfg: ServiceConfig) -> None:
        super().__init__()
        self.k_recs = global_cfg.k_recs
        self.model_cfg = get_predictors_config(global_cfg)

    @abstractmethod
    def load_model(self, global_cfg: ServiceConfig) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def recommend(self, user_id) -> List:
        raise NotImplementedError()
