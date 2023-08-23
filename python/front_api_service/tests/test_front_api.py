from typing import Any, Generator
import pytest
from starlette.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
import sys
import json
sys.path.append('../front_api_service')
from front_api import app



@pytest.fixture(autouse=True)
def _init_cache() -> Generator[Any, Any, None]:  # pyright: ignore[reportUnusedFunction]
    FastAPICache.init(InMemoryBackend())
    yield
    FastAPICache.reset()


def test_read_item():
    with TestClient(app) as client:
        response = client.get("/?limit=20")
        assert response.status_code == 200
        counter = response.text.count("null")
        assert counter == 20
        response = client.get("/")
        counter = response.text.count("null")
        assert counter == 10
        
def test_wrong_limit_0():
    with TestClient(app) as client:
        response = client.get("/?limit=0")
        assert response.status_code == 422

def test_wrong_limit_negative():
    with TestClient(app) as client:
        response = client.get("/?limit=-11")
        assert response.status_code == 422

def test_cache():
    with TestClient(app) as client:
        response = client.get("/cache")
        response_2 = client.get("/cache")
        assert response.text == response_2.text