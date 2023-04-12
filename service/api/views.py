from __future__ import annotations

from typing import Union

from fastapi import APIRouter, FastAPI, Request

from service.api.exceptions import ModelNotFoundError, UserNotFoundError
from service.log import app_logger
from service.settings import ServiceConfig

from ..models import HealthResponse, HTTPValidationError, NotFoundError, RecoResponse
from ..predictors.constructor import get_predictors


def add_views(app: FastAPI, config: ServiceConfig) -> None:
    predictors = get_predictors(config)

    router = APIRouter()

    @router.get(path="/health", tags=["Health"], response_model=HealthResponse)
    async def health() -> HealthResponse:
        """
        Check health
        """
        return HealthResponse(health="I am alive. Everything is OK!")

    @router.get(
        path="/reco/{model_name}/{user_id}",
        tags=["Recommendations"],
        response_model=RecoResponse,
        responses={
            "200": {"model": RecoResponse},
            "404": {"model": NotFoundError},
            "422": {"model": HTTPValidationError},
        },
    )
    async def get_reco(
        request: Request,
        model_name: str,
        user_id: int,
    ) -> Union[RecoResponse, NotFoundError, HTTPValidationError]:
        """
        Get recommendations for user
        """
        app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

        try:
            model = predictors[model_name]
        except KeyError as err:
            raise ModelNotFoundError(error_message=f"Model {model_name} not found") from err

        if user_id > 10**9:
            raise UserNotFoundError(error_message=f"User {user_id} not found")

        reco = model.recommend(user_id)

        return RecoResponse(user_id=user_id, items=reco)

    app.include_router(router)
