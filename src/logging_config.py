"""
Logging configuration.
Sets up structured logging.
"""

import logging
import sys
from src.config import LOG_LEVEL

def setup_logging():
    """Configure logging."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(__name__)