"""
Configuration module.
Loads from .env or defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Paths
DATA_DIR = os.getenv('DATA_DIR', 'data')
MODELS_DIR = os.getenv('MODELS_DIR', 'models')
SAMPLE_CSV = os.path.join(DATA_DIR, 'sample_urls.csv')
PROCESSED_PARQUET = os.path.join(DATA_DIR, 'processed.parquet')
BASELINE_MODEL = os.path.join(MODELS_DIR, 'baseline.joblib')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# API
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# Selenium (optional)
SELENIUM_DRIVER_PATH = os.getenv('SELENIUM_DRIVER_PATH', '/usr/local/bin/chromedriver')