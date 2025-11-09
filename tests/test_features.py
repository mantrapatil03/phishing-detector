"""
Tests for features.py.
"""

import pytest
from unittest.mock import patch
from src.features import extract_url_features, extract_html_features, extract_features
from src.utils import validate_url


def test_extract_url_features():
    """Test URL features."""
    url = "https://example.com"
    features = extract_url_features(url)
    assert len(features) == 5
    assert features[0] == len(url)  # Length
    assert features[3] == 1  # HTTPS


def test_extract_html_features():
    """Test HTML features."""
    html = "<html><form><input type='password'></input></form><iframe></iframe><a href='http://external.com'>Link</a><script src='http://external.js'></script></html>"
    features = extract_html_features(html)
    assert len(features) == 5
    assert features[0] == 1  # Forms
    assert features[1] == 1  # Password
    assert features[2] == 1  # Iframes
    assert features[4] == 1  # Suspicious scripts


@patch('src.features.requests.get')
def test_extract_features_full(mock_get):
    """Test full extraction (mock fetch)."""
    mock_get.return_value.text = "<html><form></form></html>"
    mock_get.return_value.raise_for_status = lambda: None
    features = extract_features("https://example.com")
    assert len(features) == 10


def test_validate_url():
    """Test URL validation (from utils)."""
    assert validate_url("https://example.com") is True
    assert validate_url("invalid") is False