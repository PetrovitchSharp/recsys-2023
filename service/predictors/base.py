from abc import ABC, abstractmethod
from typing import Any, List

from ..settings import ServiceConfig
from .utils import get_predictors_config


class BaseRecommender(ABC):
    def __init__(self, cfg: ServiceConfig) -> None:
        super().__init__()
        self.predictors_path = cfg.predictors_path
        self.k_recs = cfg.k_recs
        self.model_cfg = get_predictors_config(cfg)

    @abstractmethod
    def load_model(self) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def recommend(self, user_id) -> List:
        raise NotImplementedError()
