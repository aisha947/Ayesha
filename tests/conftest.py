# tests/conftest.py
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from app import app
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
