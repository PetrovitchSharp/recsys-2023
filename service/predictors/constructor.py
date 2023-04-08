from typing import Any, Dict

from .als import get_als_predictor
from .random import get_random_predictor


def get_predictors() -> Dict[str, Any]:
    predictors = {
        "random": get_random_predictor(),
        "als": get_als_predictor(),
    }

    return predictors
