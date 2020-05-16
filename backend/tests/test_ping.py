# -*- coding: utf-8 -*-
from app.configs import API_PREFIX


def test_ping(test_app):
    response = test_app.get(API_PREFIX + "/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}