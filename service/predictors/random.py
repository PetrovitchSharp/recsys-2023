import random
from typing import Any, List

from ..settings import ServiceConfig
from .base import BaseRecommender


class RandomRecommender(BaseRecommender):
    def __init__(self, cfg: ServiceConfig):
        super().__init__(cfg)

    def load_model(self) -> Any:
        random.seed(self.model_cfg["random"]["random_state"])

    def recommend(self, user_id: int) -> List:
        reco = random.sample(range(1000), self.k_recs)

        return reco

    def __repr__(self) -> str:
        return f"""{type(self).__name__}(model={self.model_cfg["random"]["model_filename"]}"""


def get_random_predictor(cfg: ServiceConfig) -> Any:
    return RandomRecommender(cfg)
