"""
Evaluation script.
Loads model and data, computes metrics.
Run: python -m src.evaluate
"""

import numpy as np
import pandas as pd
import joblib
import logging
from src.config import PROCESSED_PARQUET, BASELINE_MODEL
from src.data_processing import process_data
from src.ml_helpers import compute_metrics
from src.logging_config import setup_logging
from src.model import load_model

logger = logging.getLogger(__name__)
setup_logging()

def evaluate():
    """
    Main evaluation function.
    """
    try:
        model = load_model()
        df = pd.read_parquet(PROCESSED_PARQUET)
        X = df[[f'feature_{i+1}' for i in range(10)]].values
        y = df['label'].values
        
        # Split for eval (use same as train for consistency)
        from src.ml_helpers import split_data
        X_test, _, y_test, _ = split_data(X, y, random_state=42)  # Reuse train split
        
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)
        metrics = compute_metrics(y_test, y_pred, y_proba)
        
        logger.info("Evaluation complete.")
    except FileNotFoundError as e:
        logger.error(f"Missing files: {e}. Run train.py first.")


if __name__ == "__main__":
    evaluate()