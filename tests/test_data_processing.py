"""
Tests for data_processing.py.
"""

import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from src.data_processing import load_data, process_data
from src.features import extract_features


def test_load_data(tmp_path):
    """Test loading CSV."""
    csv_path = tmp_path / "sample_urls.csv"
    csv_content = "url,label\nhttps://example.com,0\nhttp://phish.com,1"
    csv_path.write_text(csv_content)
    
    with patch('src.config.SAMPLE_CSV', str(csv_path)):
        df = load_data()
        assert len(df) == 2
        assert 'url' in df.columns
        assert 'label' in df.columns


@patch('src.data_processing.load_data')
@patch('src.features.extract_features')
def test_process_data(mock_extract, mock_load):
    """Test processing."""
    mock_df = pd.DataFrame({'url': ['https://example.com'], 'label': [0]})
    mock_load.return_value = mock_df
    mock_extract.return_value = [1.0] * 10
    
    with patch('src.config.PROCESSED_PARQUET', '/tmp/test.parquet'):
        df = process_data()
        assert len(df) == 1
        assert 'feature_1' in df.columns