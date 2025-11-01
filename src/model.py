"""
Model module.
Loads/saves RandomForest model.
"""

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from src.config import BASELINE_MODEL
from src.features import extract_features

def load_model() -> RandomForestClassifier:
    """
    Load model.
    
    Returns:
        RandomForestClassifier.
    """
    return joblib.load(BASELINE_MODEL)


def predict_proba(features: np.ndarray) -> np.ndarray:
    """
    Predict probability.
    
    Args:
        features (np.ndarray): Feature vector.
    
    Returns:
        np.ndarray: Proba [legit, phishing].
    """
    model = load_model()
    return model.predict_proba(features)


def get_explanation(score: float) -> str:
    """
    Generate simple explanation.
    
    Args:
        score (float): Phishing prob.
    
    Returns:
        str: Explanation.
    """
    return f"Phishing score: {score:.2f}. Based on URL/ HTML features (e.g., length, forms)."