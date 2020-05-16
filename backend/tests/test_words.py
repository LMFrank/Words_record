# -*- coding: utf-8 -*-
import json
import pytest

from app.api.api_1_0 import crud
from app.configs import API_PREFIX


def test_create_word(test_app, monkeypatch):
    test_request_payload = {"words_num": 10}
    test_response_payload = {
        "id": 1,
        "words_num": test_request_payload["words_num"],
        "create_time": "2020-01-01 12:00:00",
    }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post(API_PREFIX + "/word", data=json.dumps(test_request_payload))
    assert response.status_code == 201
    assert all([k in response.json() for k in test_response_payload.keys()])

def test_create_word_invalid_json(test_app):
    response = test_app.post(API_PREFIX + "/word", data=json.dumps({"words_num": "aa"}))
    assert response.status_code == 422

def test_get_word_by_id(test_app, monkeypatch):
    test_data = {
        "create_time": "2020-01-01T12:00:00",
        "id": 1,
        "update_time": "2020-01-01T12:00:00",
        "words_num": 10,
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(API_PREFIX + "/word/1")

    assert response.status_code == 200
    assert response.json() == test_data

def test_get_word_by_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get(API_PREFIX + "/word/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "words_num not found"

    response = test_app.get(API_PREFIX + "/word/0")
    assert response.status_code == 422

def test_get_all_words(test_app, monkeypatch):
    test_data = [
        {
            "create_time": "2020-01-01T12:00:00",
            "id": 1,
            "update_time": "2020-01-01T12:00:00",
            "words_num": 10,
        },
        {
            "create_time": "2020-01-03T12:00:00",
            "id": 2,
            "update_time": "2020-01-03T12:00:00",
            "words_num": 20,
        },
        {
            "create_time": "2020-01-05T12:00:00",
            "id": 3,
            "update_time": "2020-01-05T12:00:00",
            "words_num": 30,
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get(API_PREFIX + "/word")
    assert response.status_code == 200
    assert response.json() == test_data

@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {"words_num": 20, "create_time": "2020-01-01T12:00:00"}, 200],
        [2, {"words_num": 30}, 200]
    ]
)
def test_update_word(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put(API_PREFIX + f"/word/{id}", data=json.dumps(payload))
    assert response.status_code == 200

@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [99999, {"words_num": 10, "create_time": "2020-01-03T12:00:00"}, 404],
        [0, {"words_num": 20, "create_time": "2020-01-03T12:00:00"}, 422]
    ]
)
def test_update_word_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(API_PREFIX + f"/word/{id}", data=json.dumps(payload))
    assert response.status_code == status_code

def test_remove_word(test_app, monkeypatch):
    test_data = {"id": 1, "words_num": 10}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete(API_PREFIX + "/word/1")
    assert response.status_code == 200
    assert response.json() == test_data

@pytest.mark.parametrize(
    "id, status_code",
    [
        [99999, 404],
        [0, 422],
    ]
)
def test_remove_word_incorrect_id(test_app, monkeypatch, id, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete(API_PREFIX + f"/word/{id}")
    assert response.status_code == status_code