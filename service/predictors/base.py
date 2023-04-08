from abc import ABC, abstractmethod
from typing import Any, List

from ..settings import get_config

app_config = get_config()


class BaseRecommender(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.predictors_path = app_config.predictors_path
        self.k_recs = app_config.k_recs

    @abstractmethod
    def load_model(self) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def recommend(self, model) -> List:
        raise NotImplementedError()
