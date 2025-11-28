"""
Tests for api.py.
Uses pytest-flask or manual client.
"""

import pytest
from src.api import app
from src.model import predict


@pytest.fixture
def client():
	with app.test_client() as client:
		yield client
