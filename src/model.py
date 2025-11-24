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


def predict(url: str):
    """
    Full prediction pipeline for a URL.
    Returns (score, label, explanation).
    """
    # 1. Extract features from URL
    features = extract_features(url)
    features = np.array(features).reshape(1, -1)

    # 2. Predict probability [legit, phishing]
    proba = predict_proba(features)[0]
    phishing_score = float(proba[1])

    # 3. Convert probability → label
    label = "phishing" if phishing_score >= 0.5 else "legit"

    # 4. Generate explanation
    explanation = get_explanation(phishing_score)

    return phishing_score, label, explanation

