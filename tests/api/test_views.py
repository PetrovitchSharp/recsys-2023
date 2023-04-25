from http import HTTPStatus

from starlette.testclient import TestClient

from service.settings import ServiceConfig

GET_RECO_PATH = "/reco/{model_name}/{user_id}"
GET_EXPLANATION_PATH = "/explain/{model_name}/{user_id}/{item_id}"


def test_health(
    client: TestClient,
) -> None:
    with client:
        response = client.get("/health")
    assert response.status_code == HTTPStatus.OK


def test_get_reco_success(
    client: TestClient,
    service_config: ServiceConfig,
) -> None:
    user_id = 123
    path = GET_RECO_PATH.format(model_name="random", user_id=user_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["user_id"] == user_id
    assert len(response_json["items"]) == service_config.k_recs
    assert all(isinstance(item_id, int) for item_id in response_json["items"])


def test_get_reco_for_unknown_user(
    client: TestClient,
) -> None:
    user_id = 10**10
    path = GET_RECO_PATH.format(model_name="random", user_id=user_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "user_not_found"


def test_get_explanation_for_als_success(client: TestClient) -> None:
    user_id = 699317  # user_id from mock data
    item_id = 12173  # item_id from mock data
    path = GET_EXPLANATION_PATH.format(model_name="als", user_id=user_id, item_id=item_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert isinstance(response_json["p"], float)
    assert isinstance(response_json["explanation"], str)
    assert response_json["explanation"] != ""


def test_get_explanation_for_unknown_model(client: TestClient) -> None:
    user_id = 0
    item_id = 0
    path = GET_EXPLANATION_PATH.format(model_name="unknown", user_id=user_id, item_id=item_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "model_not_found"


def test_get_explanation_for_unknown_user(client: TestClient) -> None:
    user_id = 10**10
    item_id = 0
    path = GET_EXPLANATION_PATH.format(model_name="als", user_id=user_id, item_id=item_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "user_not_found"


def test_get_explanation_for_unknown_item(client: TestClient) -> None:
    user_id = 0
    item_id = 10**10
    path = GET_EXPLANATION_PATH.format(model_name="als", user_id=user_id, item_id=item_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "item_not_found"
