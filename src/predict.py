"""
Prediction script (CLI).
Single URL prediction.
Run: python -m src.predict --url http://example.com
"""

import argparse
import logging
from src.model import predict  # Assumes predict function in model.py (added below)
from src.logging_config import setup_logging
from src.utils import validate_url

setup_logging()
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Predict phishing for a URL.")
    parser.add_argument("--url", required=True, help="URL to scan")
    args = parser.parse_args()
    
    if not validate_url(args.url):
        logger.error("Invalid URL.")
        return
    
    try:
        score, label, explanation = predict(args.url)
        print(f"URL: {args.url}")
        print(f"Score (phishing prob): {score:.2f}")
        print(f"Label: {label.upper()}")
        print(f"Explanation: {explanation}")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")


if __name__ == "__main__":
    main()