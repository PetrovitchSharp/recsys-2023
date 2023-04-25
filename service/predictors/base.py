# mypy: disable-error-code="misc"
# pylint: disable=no-method-argument
from abc import ABC, abstractmethod
from typing import Any, List, Tuple

from ..settings import ServiceConfig
from .utils import get_predictors_config


class BaseRecommender(ABC):
    def __init__(self, global_cfg: ServiceConfig) -> None:
        super().__init__()
        self.k_recs = global_cfg.k_recs
        self.model_cfg = get_predictors_config(global_cfg)
        self._users = []

    @abstractmethod
    def load_model(self, global_cfg: ServiceConfig) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def recommend(self, user_id: int) -> List:
        raise NotImplementedError()

    @abstractmethod
    def explain_reco(self, user_id: int, item_id: int) -> Tuple[float, List]:
        raise NotImplementedError()

    @property
    def users(self) -> List:
        raise NotImplementedError()
