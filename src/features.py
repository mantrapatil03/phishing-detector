"""
Feature extraction module.
Extracts 10 features: 5 URL, 5 HTML. Optional screenshot hash as feature 11 (stub).
"""

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging
from src.screenshot import get_screenshot_hash  # Optional

logger = logging.getLogger(__name__)

def extract_url_features(url: str) -> list[float]:
    """
    Extract 5 URL-based features.
    
    Args:
        url (str): URL.
    
    Returns:
        list[float]: 5 features.
    """
    parsed = urlparse(url)
    host = parsed.hostname or ''
    is_ip = 1 if host.replace('.', '').replace(':', '').isdigit() else 0
    features = [
        len(url),
        url.count('.'),
        1 if '@' in url else 0,
        1 if parsed.scheme == 'https' else 0,
        is_ip
    ]
    return features


def fetch_html(url: str) -> str:
    """
    Fetch HTML.
    
    Args:
        url (str): URL.
    
    Returns:
        str: HTML.
    """
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def extract_html_features(html: str) -> list[float]:
    """
    Extract 5 HTML-based features.
    
    Args:
        html (str): HTML.
    
    Returns:
        list[float]: 5 features.
    """
    soup = BeautifulSoup(html, 'html.parser')
    forms = len(soup.find_all('form'))
    password_inputs = len(soup.find_all('input', {'type': 'password'}))
    iframes = len(soup.find_all('iframe'))
    links = soup.find_all('a', href=True)
    base_url = soup.find('base')
    base_href = base_url['href'] if base_url else ''
    external_links = sum(1 for link in links if link['href'].startswith('http') and not link['href'].startswith(base_href))
    scripts = soup.find_all('script', src=True)
    suspicious_scripts = 1 if any(script['src'].startswith('http') for script in scripts) else 0
    
    return [forms, password_inputs, iframes, external_links, suspicious_scripts]


def extract_features(url: str, include_screenshot: bool = False) -> list[float]:
    """
    Extract all features.
    
    Args:
        url (str): URL.
        include_screenshot (bool): Include screenshot hash (feature 11).
    
    Returns:
        list[float]: 10 or 11 features.
    """
    url_features = extract_url_features(url)
    try:
        html = fetch_html(url)
        html_features = extract_html_features(html)
    except requests.RequestException as e:
        logger.warning(f"HTML fetch failed for {url}: {e}")
        html_features = [0.0] * 5
    
    features = url_features + html_features
    if include_screenshot:
        try:
            screenshot_hash = get_screenshot_hash(url)
            features.append(screenshot_hash)  # e.g., perceptual hash value
        except Exception as e:
            logger.warning(f"Screenshot failed for {url}: {e}")
            features.append(0.0)
    
    return features