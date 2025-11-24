"""
Data processing module.
Loads CSV, extracts features, saves Parquet.
"""
import os 
import pandas as pd
import logging
from src.config import SAMPLE_CSV, PROCESSED_PARQUET
from src.features import extract_features
from src.utils import validate_url, normalize_url

logger = logging.getLogger(__name__)

def load_data() -> pd.DataFrame:
    """
    Load sample URLs from CSV.
    
    Returns:
        pd.DataFrame: DataFrame with 'url' and 'label'.
    
    Raises:
        FileNotFoundError: If CSV missing.
    """
    if not os.path.exists(SAMPLE_CSV):
        raise FileNotFoundError(f"{SAMPLE_CSV} not found. Add sample data.")
    df = pd.read_csv(SAMPLE_CSV)
    df['url'] = df['url'].apply(normalize_url)
    invalid = df[~df['url'].apply(validate_url)]
    if not invalid.empty:
        logger.warning(f"Invalid URLs: {len(invalid)}")
    return df[df['url'].apply(validate_url)]

def process_data() -> pd.DataFrame:
    """
    Extract features for all URLs and save as Parquet.
    
    Returns:
        pd.DataFrame: Features + labels.
    """
    df = load_data()
    features_list = []
    for url in df['url']:
        try:
            feats = extract_features(url)
            features_list.append(feats)
        except Exception as e:
            logger.error(f"Feature extraction failed for {url}: {e}")
            features_list.append([0.0] * 10)  # Fallback
    
    feature_df = pd.DataFrame(features_list, columns=[f'feature_{i+1}' for i in range(10)])
    processed_df = pd.concat([df.reset_index(drop=True), feature_df], axis=1)
    processed_df.to_parquet(PROCESSED_PARQUET)
    logger.info(f"Processed data saved to {PROCESSED_PARQUET}")
    return processed_df
