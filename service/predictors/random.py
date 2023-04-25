import random
from typing import Any, List, Tuple

from ..settings import ServiceConfig
from .base import BaseRecommender


class RandomRecommender(BaseRecommender):
    def __init__(self, global_cfg: ServiceConfig) -> None:
        super().__init__(global_cfg)
        self.load_model(global_cfg)

    def load_model(self, global_cfg: ServiceConfig) -> Any:
        random.seed(self.model_cfg["random"]["random_state"])

    def recommend(self, user_id: int) -> List:
        reco = random.sample(range(1000), self.k_recs)

        return reco

    def explain_reco(self, user_id: int, item_id: int) -> Tuple[float, List]:
        raise NotImplementedError()

    @property
    def users(self) -> List:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"""{type(self).__name__}(model={self.model_cfg["random"]["model_filename"]}"""


def get_random_predictor(global_cfg: ServiceConfig) -> Any:
    return RandomRecommender(global_cfg)
