"""
Utility functions.
"""

import re
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url (str): URL to validate.
    
    Returns:
        bool: True if valid.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def normalize_url(url: str) -> str:
    """
    Normalize URL (e.g., add scheme if missing).
    
    Args:
        url (str): URL to normalize.
    
    Returns:
        str: Normalized URL.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url