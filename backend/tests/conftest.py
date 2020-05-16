# -*- coding: utf-8 -*-
import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture()
def test_app():
    with TestClient(app) as client:
        yield client
