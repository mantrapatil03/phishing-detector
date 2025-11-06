"""
Flask API.
Exposes /scan (POST JSON {"url": "str"}).
Run: python -m src.api
"""

from flask import Flask, request, jsonify
import logging
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.config import FLASK_ENV, FLASK_DEBUG
from src.model import predict
from src.logging_config import setup_logging
from src.utils import validate_url

setup_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['ENV'] = FLASK_ENV
app.config['DEBUG'] = FLASK_DEBUG

@app.route('/scan', methods=['POST'])
def scan_url():
    """
    Scan endpoint.
    """
    if not request.is_json:
        return jsonify({"error": "JSON required"}), 400
    
    data = request.get_json()
    url = data.get('url')
    if not url or not validate_url(url):
        return jsonify({"error": "Valid 'url' required"}), 400
    
    try:
        score, label, explanation = predict(url)
        return jsonify({
            "url": url,
            "score": float(score),
            "label": label,
            "explanation": explanation
        })
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health():
    """Health check."""
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5000)