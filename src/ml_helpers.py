"""
ML helper functions.
Common utilities for training, splitting, and metrics.
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import logging

logger = logging.getLogger(__name__)

def split_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42) -> tuple:
    """
    Split data into train/test sets.
    
    Args:
        X (np.ndarray): Features.
        y (np.ndarray): Labels.
        test_size (float): Test split ratio.
        random_state (int): Random seed.
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test).
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray = None) -> dict:
    """
    Compute classification metrics.
    
    Args:
        y_true (np.ndarray): True labels.
        y_pred (np.ndarray): Predicted labels.
        y_proba (np.ndarray, optional): Predicted probabilities.
    
    Returns:
        dict: Metrics (accuracy, precision, recall, f1, roc_auc if proba).
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred)
    }
    if y_proba is not None:
        from sklearn.metrics import roc_auc_score
        metrics['roc_auc'] = roc_auc_score(y_true, y_proba[:, 1])
    
    logger.info(f"Metrics: {metrics}")
    print(classification_report(y_true, y_pred))
    return metrics