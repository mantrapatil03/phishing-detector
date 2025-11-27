"""
Perfect tests for data_processing.py
Covers:
- load_data() with proper patching
- process_data() with feature generation and parquet output
"""

import pandas as pd
from unittest.mock import patch
from src.data_processing import load_data, process_data


def test_load_data(tmp_path):
    """Test loading CSV from temporary file, ensuring patch target is correct."""
    csv_path = tmp_path / "sample_urls.csv"
    csv_content = "url,label\nhttps://example.com,0\nhttp://phish.com,1"
    csv_path.write_text(csv_content)

    # Patch SAMPLE_CSV exactly where it's used
    with patch("src.data_processing.SAMPLE_CSV", str(csv_path)):
        df = load_data()

        assert len(df) == 2
        assert list(df["url"]) == ["https://example.com", "http://phish.com"]
        assert list(df["label"]) == [0, 1]


def test_process_data(tmp_path, monkeypatch):
    """Full integration-style test: CSV → features → parquet."""
    # Create temp CSV
    csv_path = tmp_path / "sample_urls.csv"
    csv_path.write_text("url,label\nhttps://example.com,0\nhttp://phish.com,1")

    # Temp parquet output file
    out_path = tmp_path / "out.parquet"

    # Patch paths used inside process_data()
    monkeypatch.setattr("src.data_processing.SAMPLE_CSV", str(csv_path))
    monkeypatch.setattr("src.data_processing.PROCESSED_PARQUET", str(out_path))

    df = process_data()

    # Should produce exactly 2 rows
    assert len(df) == 2

    # Parquet file must be created
    assert out_path.exists()

    # Check that all 10 expected feature columns exist
    for i in range(1, 11):
        assert f"feature_{i}" in df.columns
