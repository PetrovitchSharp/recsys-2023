from abc import ABC, abstractmethod
from typing import Any, List

from ..settings import get_config

model_cfg = get_config()


class BaseRecommender(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.k_recs = model_cfg.k_recs

    @abstractmethod
    def load_model(self) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def recommend(self, user_id) -> List:
        raise NotImplementedError()
