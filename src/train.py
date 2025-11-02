"""
Training script.
Processes data, trains RandomForest, saves model.
Run: python -m src.train
"""

import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
import logging
from src.config import PROCESSED_PARQUET, BASELINE_MODEL
from src.data_processing import process_data
from src.ml_helpers import split_data, compute_metrics
from src.logging_config import setup_logging

logger = logging.getLogger(__name__)
setup_logging()

def generate_synthetic_data(n_samples: int = 200) -> tuple[np.ndarray, np.ndarray]:
    """
    Fallback synthetic data if CSV missing.
    """
    np.random.seed(42)
    n_legit = n_samples // 2
    n_phish = n_samples - n_legit
    
    # Legit: short, secure, few suspicious elements
    X_legit = np.random.normal([30, 2, 0, 1, 0, 1, 0, 1, 3, 0], [5, 1, 0, 0, 0, 1, 0, 1, 2, 0], (n_legit, 10))
    y_legit = np.zeros(n_legit)
    
    # Phishing: long, suspicious, many forms/iframes
    X_phish = np.random.normal([80, 5, 1, 0, 1, 3, 2, 1, 10, 1], [10, 2, 0, 0, 0, 2, 1, 1, 5, 0], (n_phish, 10))
    y_phish = np.ones(n_phish)
    
    X = np.vstack([X_legit, X_phish])
    y = np.hstack([y_legit, y_phish])
    
    # Shuffle
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    return X[indices], y[indices]


def train():
    """
    Main training function.
    """
    os.makedirs(os.path.dirname(BASELINE_MODEL), exist_ok=True)
    
    try:
        # Try real data
        df = process_data()
        X = df[[f'feature_{i+1}' for i in range(10)]].values
        y = df['label'].values
        logger.info("Using real data from CSV.")
    except FileNotFoundError:
        # Fallback to synthetic
        X, y = generate_synthetic_data()
        logger.warning("CSV not found; using synthetic data.")
    
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)
    metrics = compute_metrics(y_test, y_pred, y_proba)
    
    # Save
    joblib.dump(model, BASELINE_MODEL)
    logger.info(f"Model saved to {BASELINE_MODEL}")


if __name__ == "__main__":
    train()