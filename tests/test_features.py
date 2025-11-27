"""
Tests for features.py.
"""

from unittest.mock import patch
from src.features import extract_url_features, extract_html_features, extract_features
from src.utils import validate_url


def test_extract_url_features():
    """Test URL feature extraction."""
    url = "https://example.com"
    features = extract_url_features(url)
    
    assert len(features) == 5
    assert features[0] == len(url)      # Length of URL
    assert features[3] == 1             # HTTPS detected


def test_extract_html_features():
    """Test HTML feature extraction."""
    html = (
        "<html><form><input type='password'></input></form>"
        "<iframe></iframe><a href='http://external.com'>Link</a>"
        "<script src='http://external.js'></script></html>"
    )
    features = extract_html_features(html)
    
    assert len(features) == 5
    assert features[0] == 1  # Number of forms
    assert features[1] == 1  # Number of password inputs
    assert features[2] == 1  # Number of iframes
    assert features[4] == 1  # Suspicious scripts detected


@patch('src.features.requests.get')
def test_extract_features_full(mock_get):
    """Test full feature extraction using a mocked HTTP response."""
    mock_get.return_value.text = "<html><form></form></html>"
    mock_get.return_value.raise_for_status = lambda: None
    
    features = extract_features("https://example.com")
    
    assert len(features) == 10
    # Optional: check first few features if needed
    assert features[0] > 0


def test_validate_url():
    """Test the validate_url utility."""
    assert validate_url("https://example.com") is True
    assert validate_url("http://example.com") is True
    assert validate_url("invalid") is False
    assert validate_url("ftp://example.com") is False
    assert validate_url("") is False
    assert validate_url("https://") is False
