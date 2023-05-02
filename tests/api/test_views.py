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


def test_get_explanation_for_als_for_warm_user_success(client: TestClient) -> None:
    user_id = 555088  # warm user's user_id from mock data
    item_id = 12173  # item_id from mock data
    path = GET_EXPLANATION_PATH.format(model_name="als", user_id=user_id, item_id=item_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert isinstance(response_json["p"], int)
    assert isinstance(response_json["explanation"], str)
    assert response_json["p"] == 0
    assert response_json["explanation"] == ("Фильм/сериал 'Мстители: Финал' скорее всего вам не понравится")


def test_get_explanation_for_als_for_previously_seen_success(client: TestClient) -> None:
    user_id = 555088  # warm user's user_id from mock data
    item_id = 598  # item_id from mock data that has been seen by user
    path = GET_EXPLANATION_PATH.format(model_name="als", user_id=user_id, item_id=item_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert isinstance(response_json["p"], int)
    assert isinstance(response_json["explanation"], str)
    assert response_json["p"] == 100
    assert response_json["explanation"] == (
        "Фильм/сериал 'Мы будем первыми!' может вам понравиться, т.к. вы его уже посмотрели"
    )


def test_get_explanation_for_als_for_cold_user_success(client: TestClient) -> None:
    user_id = 6  # cold user's user_id from mock data
    item_id = 15297  # item_id from mock data
    path = GET_EXPLANATION_PATH.format(model_name="als", user_id=user_id, item_id=item_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert isinstance(response_json["p"], int)
    assert isinstance(response_json["explanation"], str)
    assert response_json["p"] == 95
    assert response_json["explanation"] == (
        "Фильм/сериал 'Клиника счастья' может вам понравиться с вероятностью 95%"
        + " т.к. его уже посмотрели 193123 пользователей сервиса и"
        + " он занимает 2 место в нашем топе"
    )


def test_get_explanation_for_unknown_model(client: TestClient) -> None:
    user_id = 555088  # user_id from mock data
    item_id = 12173  # item_id from mock data
    path = GET_EXPLANATION_PATH.format(model_name="unknown", user_id=user_id, item_id=item_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "model_not_found"


def test_get_explanation_for_unknown_user(client: TestClient) -> None:
    user_id = 10**10
    item_id = 12173  # item_id from mock data
    path = GET_EXPLANATION_PATH.format(model_name="als", user_id=user_id, item_id=item_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "user_not_found"


def test_get_explanation_for_unknown_item(client: TestClient) -> None:
    user_id = 555088  # user_id from mock data
    item_id = 10**10
    path = GET_EXPLANATION_PATH.format(model_name="als", user_id=user_id, item_id=item_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "item_not_found"
