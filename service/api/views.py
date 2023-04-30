from __future__ import annotations

from typing import Union

from fastapi import APIRouter, FastAPI, Request

from service.api.exceptions import ItemNotFoundError, UserNotFoundError
from service.log import app_logger

from ..models import ExplainResponse, HealthResponse, HTTPValidationError, NotFoundError, RecoResponse
from ..predictors.constructor import get_predictor
from ..predictors.explainer import get_all_users, get_items_rating

router = APIRouter()


@router.get(path="/health", tags=["Health"], response_model=HealthResponse)
async def health() -> HealthResponse:
    """
    Check health
    """
    return HealthResponse(health="I am alive. Everything is OK!")


@router.get(
    path="/explain/{model_name}/{user_id}/{item_id}",
    tags=["Explanations"],
    responses={"200": {"model": ExplainResponse}, "404": {"model": NotFoundError}},
)
async def explain(request: Request, model_name: str, user_id: int, item_id: int) -> ExplainResponse:
    """
    Explain recommendation
    """
    p = 0.0
    explanation = ""

    model = get_predictor(model_name)
    model_warm_users = model.users

    all_users = get_all_users()
    items_rating = get_items_rating()

    # If the user is not in the database at all, we throw an error
    if user_id not in all_users:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    # Similarly for items
    if item_id not in items_rating.index:
        raise ItemNotFoundError(error_message=f"Item {item_id} not found")

    # If the model has never seen the user,
    # we give him/her an explanation based on the global top seen
    if user_id not in model_warm_users:
        # Get the values needed for the explanation
        # from the dataset with the rating
        p = round(items_rating.at[item_id,"relevancy"] * 100, 4)
        views_count = items_rating.at[item_id,"views"]
        item_rank = items_rating.at[item_id,"rank"]
        item_title = items_rating.at[item_id,"title"]

        # Forming an explanation
        explanation = (
            rf"Фильм\сериал {item_title!r} может вам понравиться т.к. "
            + rf"его уже посмотрели {views_count} пользователей сервиса, что составляет "
            + rf"{p}% от всех просмотров и занимает {item_rank} место в нашем топе"
        )
    # Otherwise we try to explain by the model itself
    else:
        # Get the values needed for the explanation from model itself
        item_score, top_contributor = model.explain_reco(user_id, item_id)
        p = round(item_score * 100, 4)
        item_title = items_rating.at[item_id,"title"]
        top_contributor_title = items_rating.at[top_contributor,"title"]

        # Forming an explanation
        explanation = (
            rf"Фильм\сериал {item_title!r} может вам {'' if p > 0 else 'не'} "
            + rf"с вероятностью {abs(p)}% т.к. вы посмотрели {top_contributor_title!r}"
        )

    return ExplainResponse(p=p, explanation=explanation)


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

    model = get_predictor(model_name)

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    reco = model.recommend(user_id)

    return RecoResponse(user_id=user_id, items=reco)


def add_views(app: FastAPI) -> None:
    app.include_router(router)
