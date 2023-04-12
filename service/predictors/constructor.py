from typing import Any, Dict

from ..settings import ServiceConfig
from .als import get_als_predictor
from .random import get_random_predictor


def get_predictors(config: ServiceConfig) -> Dict[str, Any]:
    predictors = {
        "random": get_random_predictor(config),
        "als": get_als_predictor(config),
    }

    return predictors
