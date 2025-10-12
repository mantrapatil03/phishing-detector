# phishing-detector


```
phishing-detector/
├── app/                            # Flask app + detectors
│   ├── __init__.py
│   ├── api.py
│   ├── detector.py                 # feature extraction + predict()
│   └── models/
│       └── rf_model.pkl            # example trained model (gitignored)
├── data/
│   ├── raw/                        # raw datasets (NOT committed)
│   └── processed/
├── notebooks/                      # EDA / training notebooks
├── tests/
│   ├── test_detector.py
├── docker/
│   └── Dockerfile
├── requirements.txt
├── train.py                        # example training script
├── cli.py                          # command line scanner
├── README.md
└── .github/
    ├── workflows/ci.yml
    └── ISSUE_TEMPLATE.md
```


1) Short repo description (GitHub "description" field)

Phishing Website Detector — ML + heuristics to detect phishing URLs & pages; Flask API + CLI + Docker; includes dataset processing, model training, and real-time scanning.

2) GitHub repo README (copy this entire block into README.md)
Phishing Website Detector

Lightweight phishing-site detector combining URL/HTML heuristics and a machine learning model. Exposes a Flask REST API and a CLI scanner. Designed for research, demos and light production use.

Features

URL feature extraction (length, tokens, domain age placeholder, suspicious substrings)

HTML features (forms, suspicious links, inline scripts)

Combined ML model (example: RandomForest) + heuristic fallback

REST API for real-time scanning

CLI scanner for batch checks

Docker-ready and CI-tested

Tech stack

Python 3.10+

Flask (API)

scikit-learn (model)

pandas/numpy (data)

BeautifulSoup4 (HTML analysis)

pytest (tests)

Docker

GitHub Actions for lint/test

Repo layout
phishing-detector/
├── app/                            # Flask app + detectors
│   ├── __init__.py
│   ├── api.py
│   ├── detector.py                 # feature extraction + predict()
│   └── models/
│       └── rf_model.pkl            # example trained model (gitignored)
├── data/
│   ├── raw/                        # raw datasets (NOT committed)
│   └── processed/
├── notebooks/                      # EDA / training notebooks
├── tests/
│   ├── test_detector.py
├── docker/
│   └── Dockerfile
├── requirements.txt
├── train.py                        # example training script
├── cli.py                          # command line scanner
├── README.md
└── .github/
    ├── workflows/ci.yml
    └── ISSUE_TEMPLATE.md

Quick start
1. Clone and install
git clone https://github.com/<your-org>/phishing-detector.git
cd phishing-detector
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

2. Run tests
pytest -q

3. Run API (development)
export FLASK_APP=app.api
flask run --host=0.0.0.0 --port=5000
# POST JSON to http://localhost:5000/scan

4. Docker
docker build -t phishing-detector:latest -f docker/Dockerfile .
docker run -p 5000:5000 phishing-detector:latest

API

POST /scan
Body:

{
  "url": "http://example.com",
  "html": "<html>...</html>"    # optional, improves accuracy
}


Response:

{
  "url": "http://example.com",
  "score": 0.87,
  "label": "phishing",
  "explanation": {
    "url_length": 78,
    "has_ip": false,
    "num_forms": 2
  }
}

Training

train.py demonstrates feature extraction and training a scikit-learn model using local dataset CSVs (expected columns: url, html, label).

Contributing

Fork

Create branch feat/your-feature

Add tests

Open PR; include one-line changelog in PR description

License

MIT

3) One-line repo creation prompt (for AI repository generator or gh CLI)
Create a new GitHub repo named "phishing-detector" with description "Phishing Website Detector — ML + heuristics; Flask API, CLI, Docker" and initialize with README, .gitignore (Python), MIT license.

4) Starter files & snippets
app/detector.py (core feature extraction + predict)
# app/detector.py
import re
import pickle
from bs4 import BeautifulSoup
from urllib.parse import urlparse

SUSPICIOUS_TOKENS = ['login', 'secure', 'bank', 'verify', 'update', 'confirm', 'account', 'signin']

def extract_url_features(url: str):
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""
    features = {}
    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['has_ip'] = bool(re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname))
    features['has_at'] = '@' in url
    features['suspicious_tokens'] = sum(tok in url.lower() for tok in SUSPICIOUS_TOKENS)
    return features

def extract_html_features(html: str):
    soup = BeautifulSoup(html or "", 'html.parser')
    forms = soup.find_all('form')
    features = {
        'num_forms': len(forms),
        'num_inputs': len(soup.find_all('input')),
        'num_iframes': len(soup.find_all('iframe')),
        'num_external_links': sum(1 for a in soup.find_all('a', href=True) if urlparse(a['href']).netloc)
    }
    return features

class Detector:
    def __init__(self, model_path=None):
        self.model = None
        if model_path:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)

    def predict(self, url: str, html: str = None):
        f = {}
        f.update(extract_url_features(url))
        if html:
            f.update(extract_html_features(html))
        X = [list(f.values())]
        if self.model:
            score = float(self.model.predict_proba(X)[:,1][0])
            label = 'phishing' if score > 0.5 else 'benign'
        else:
            # heuristic fallback
            score = min(1.0, 0.1 * f['suspicious_tokens'] + 0.01*f['url_length'])
            label = 'phishing' if score > 0.5 else 'benign'
        return {'url': url, 'score': score, 'label': label, 'explanation': f}

app/api.py (Flask)
# app/api.py
from flask import Flask, request, jsonify
from .detector import Detector

app = Flask(__name__)
detector = Detector()  # optionally pass model path

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json(force=True)
    url = data.get('url')
    html = data.get('html')
    if not url:
        return jsonify({'error': 'url required'}), 400
    res = detector.predict(url, html)
    return jsonify(res)

train.py (very small example)
# train.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
from app.detector import extract_url_features, extract_html_features

def featurize(row):
    f = extract_url_features(row['url'])
    if 'html' in row and pd.notna(row.get('html')):
        f.update(extract_html_features(row['html']))
    return pd.Series(f)

def main():
    df = pd.read_csv('data/processed/train.csv')  # expects columns url,html,label
    X = df.apply(featurize, axis=1)
    y = df['label'].map({'phishing':1, 'benign':0})
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    with open('app/models/rf_model.pkl','wb') as f:
        pickle.dump(clf, f)
    print("Model saved to app/models/rf_model.pkl")

if __name__=='__main__':
    main()

cli.py
# cli.py
import argparse
from app.detector import Detector
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL to scan')
    parser.add_argument('--html', help='Path to HTML file to include', default=None)
    args = parser.parse_args()
    html = None
    if args.html:
        html = open(args.html, 'r', encoding='utf-8').read()
    det = Detector(model_path='app/models/rf_model.pkl')
    print(det.predict(args.url, html))

if __name__=='__main__':
    main()

requirements.txt
Flask>=2.0
scikit-learn>=1.0
pandas
numpy
beautifulsoup4
pytest
gunicorn

docker/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=app.api
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.api:app", "--workers", "2"]

5) GitHub Actions CI (.github/workflows/ci.yml)
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest -q

6) Issue & PR templates (create .github/ISSUE_TEMPLATE/bug.md etc.)

ISSUE_TEMPLATE.md example:

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. ...
2. ...

**Expected behavior**
What you expected to happen.

**Environment**
- Python version:
- OS:

7) Useful git commit messages / PR title templates

Initial commit: chore: initial scaffold (README, layout)

Add detector: feat(detector): add url/html feature extraction and heuristic detector

Add API: feat(api): add Flask scan endpoint

Add training: feat(train): add training script for RandomForest model

Fix tests: test: add unit tests for detector

8) Minimal tests example (tests/test_detector.py)
from app.detector import extract_url_features, extract_html_features, Detector

def test_url_features_basic():
    f = extract_url_features("http://example.com/path")
    assert f['url_length'] > 0
    assert f['num_dots'] >= 1

def test_html_features():
    html = "<html><form action='/a'><input name='u'/></form></html>"
    f = extract_html_features(html)
    assert f['num_forms'] == 1
    assert f['num_inputs'] == 1

def test_detector_heuristic():
    d = Detector()
    res = d.predict("http://secure-login-bank.example/login", html=None)
    assert 'score' in res and 'label' in res

9) Suggested .gitignore
__pycache__/
*.pyc
.venv/
app/models/*.pkl
data/raw/
.env

10) One-shot prompt for AI to generate the repo files
Generate a Python project named "phishing-detector" that implements:
- URL + HTML feature extraction
- A Flask REST API (/scan) that returns {url, score, label, explanation}
- A CLI tool to scan a URL
- A simple RandomForest training script (train.py)
- Unit tests with pytest
- Dockerfile and GitHub Actions CI
Include README.md, requirements.txt, .gitignore. Use BeautifulSoup for HTML parsing and scikit-learn for the model. Provide small, well-documented functions and keep dependencies minimal.
