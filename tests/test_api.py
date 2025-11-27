"""
Tests for api.py.
Uses Flask test client.
"""

import pytest
from unittest.mock import patch
from src.api import app


@pytest.fixture
def client():
    """Create Flask test client."""
    with app.test_client() as client:
        yield client


@patch("src.model.predict")
def test_predict_endpoint(mock_predict, client):
    """Test /predict API endpoint."""
    mock_predict.return_value = [0]

    response = client.post("/predict", json={"url": "https://example.com"})

    assert response.status_code == 200
    assert response.json == {"prediction": [0]}
