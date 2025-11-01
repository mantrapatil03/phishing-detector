"""
Screenshot module (optional).
Uses Selenium to capture and hash screenshot for visual features.
Minimal: Returns a simple hash (0-1 similarity stub).
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import hashlib
import logging
from src.config import SELENIUM_DRIVER_PATH

logger = logging.getLogger(__name__)

def get_screenshot_hash(url: str) -> float:
    """
    Capture screenshot and return perceptual hash (stub: simple MD5-based 0-1 score).
    
    Args:
        url (str): URL.
    
    Returns:
        float: Hash value (0-1; higher = more suspicious if differs from known good).
    
    Note: In prod, use imagehash library for better perceptual hashing.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=SELENIUM_DRIVER_PATH, options=options)
    try:
        driver.get(url)
        screenshot = driver.get_screenshot_as_png()
        md5_hash = hashlib.md5(screenshot).hexdigest()
        # Stub: Convert to float (e.g., sum digits / max)
        hash_float = sum(int(d) for d in md5_hash) / (16 * 15)  # Normalize 0-1
        return hash_float
    except Exception as e:
        logger.error(f"Screenshot error: {e}")
        return 0.0
    finally:
        driver.quit()