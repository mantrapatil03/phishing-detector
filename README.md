
<h1 align="center"> Phishing Detection</h1>

<p align="center">
  <b>Machine Learning powered phishing website detector using URL & HTML analysis</b>  
  <br>
  Built with <code>Python</code> • <code>scikit-learn</code> • <code>Flask</code> • <code>BeautifulSoup</code>
</p>

<p align="center">
  <a href="https://github.com/mantrapatil03/phishing-detection/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/mantrapatil03/phishing-detection/ci.yml?label=CI%2FCD&logo=github" alt="CI/CD" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python 3.10+" />
  <a href="https://github.com/mantrapatil03/phishing-detection/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT" />
  </a>
  <img src="https://img.shields.io/badge/Docker-ready-blue.svg" alt="Docker ready" />
  <img src="https://img.shields.io/badge/tests-passing-brightgreen.svg" alt="Tests passing" />
  <br><br>
  <a href="https://github.com/mantrapatil03/phishing-detection/stargazers">
    <img src="https://img.shields.io/github/stars/mantrapatil03/phishing-detection?style=social" alt="GitHub stars" />
  </a>
  <a href="https://github.com/mantrapatil03/phishing-detection/network/members">
    <img src="https://img.shields.io/github/forks/mantrapatil03/phishing-detection?style=social" alt="GitHub forks" />
  </a>
</p>

---
 
> **A modular, production-ready phishing website detection system**.  


A **modular Python project** for **detecting phishing websites** using URL and HTML features extracted via `BeautifulSoup`, trained on a Random Forest model from `scikit-learn`.
Includes data processing, training, prediction (CLI + API), evaluation, testing, Docker support, and CI/CD.

## Features

- **Data Processing**
    - Load URLs/labels from CSV
    - Extract 10 features:
        - **URL features (5)**: length, dots, `@`, HTTPS, IP
        - **HTML features (5)**: forms, passwords, iframes, links, scripts
    - Save processed features as Parquet

- **Model**
    - `RandomForestClassifier` trained on extracted features
    - Optional 11th feature: screenshot hash (via Selenium)

- **Training & Evaluation**
    - `train.py`: Trains model (synthetic fallback if no CSV)
    - `evaluate.py`: Computes accuracy, precision, recall, F1, ROC-AUC

- **Prediction**
    - CLI (predict.py) → Single URL prediction
    - REST API (api.py) → /scan endpoint for predictions

- **API**
    - Flask-based, returns JSON:
    ```json
    {
      "url": "https://example.com",
      "score": 0.12,
      "label": "legit",
      "explanation": "Contains HTTPS, no suspicious patterns"
    }
    ```

- **Extras**
    - Logging & configuration via `.env`
    - Screenshot stub (optional Selenium support)
    - EDA notebook for experiments

- Testing
    - Pytest suite for data, features, and API (mocked network)

- **Deployment**
    - Docker & Docker Compose support
    - GitHub Actions for CI/CD (lint, train, test)

- **Dependencies**
    - Minimal core (scikit-learn, Flask, BeautifulSoup4)
    - Optional: Selenium for screenshots

>💡 Uses synthetic data by default. Replace data/sample_urls.csv with real labeled data
>(url,label) for production use.

## Quick Start

### 1️⃣ Setup
```bash
git clone https://github.com/mantrapatil03/phishing-detector phishing-detection
cd phishing-detection
pip install -r requirements.txt
cp .env.example .env
# (Edit paths/config in .env if needed)
```

### 2️⃣ Prepare Data (Optional)

If you want to use real URLs, create a CSV:
```csv
url,label
https://example.com,0
http://phishingsite.ru/login,1
https://google.com,0
http://fakebank.com@realbank.com,1
https://paypal.com,0
http://192.168.1.5:8080,1
```

Save it as `data/sample_urls.csv`.

### 3️⃣ Train Model
```bash
python -m src.train
```

- Generates:

    - `models/baseline.joblib`
    - `data/processed.parquet`

- Output includes accuracy (≈0.95 on synthetic data)

### 4️⃣ Evaluate
```bash
python -m src.evaluate
```

Prints detailed metrics & classification report.

### 5️⃣ Predict (CLI)
```bash
python -m src.predict --url https://example.com
```

Example Output:
```yaml
Score: 0.12
Label: legit
Explanation: Contains HTTPS and no suspicious symbols
```

### 6️⃣ Run API
```bash
python -m src.api
```

Test with `curl`:
```bash
curl -X POST http://localhost:5000/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Health Check:
```bash
curl http://localhost:5000/
```

### 7️⃣ Run Tests
```bash
pytest tests/ -v
```

### 8️⃣ EDA / Experiments

Open:
```bash
notebooks/EDA_and_experiments.ipynb
```

Run to explore:

- Data distribution

- Correlations

- Model tuning experiments

## Development Notes

- Logging → Configured via `src/logging_config.py` (`LOG_LEVEL` in `.env`)

- Config → Paths & secrets via `src/config.py`

- Screenshot Feature → Optional

- Enable by setting `include_screenshot=True` in `src/model.py``

    - Requires Selenium + ChromeDriver (included in Dockerfile)

    - Retrain model after enabling

- Extend Project

    - Add new data sources → `data_processing.py`

    - Improve model → `ml_helpers.py`

    - Add features → `features.py`

    - Tune models → GridSearchCV, XGBoost, LSTM, etc.

- Code Style
- 
```bash
black .  # line-length = 88 (pyproject.toml)
```

## Deployment

**Docker**
```bash
docker build -t phishing-detection .
docker run -p 5000:5000 phishing-detection
```

- Includes ChromeDriver
- Trains model during build

**Docker Compose**
```bash
docker-compose up
```

- Mounts `./data` and `./models` for persistence

**Production Tips**

- Use Gunicorn/Waitress for Flask

- Cache HTML to avoid rate limits

- Use Celery for batch scanning

- Add Prometheus for monitoring
  
- Implement auth & rate-limiting for API

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`):

- Runs on push/PR to main
- Steps:
    - Lint (black)
    - Install dependencies
    - Generate synthetic data
    - Train, evaluate, and test model
    - Verify model/parquet generation

## Project Structure
```
phishing-detection/
├── README.md
├── VERIFICATION.md
├── SECURITY.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .env.example
├── Dockerfile
├── docker-compose.yml
│
├── data/
│   ├── sample_urls.csv
│   └── processed.parquet
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── logging_config.py
│   ├── utils.py
│   ├── data_processing.py
│   ├── features.py
│   ├── screenshot.py
│   ├── model.py
│   ├── ml_helpers.py
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│   └── api.py
│
├── notebooks/
│   └── EDA_and_experiments.ipynb
│
├── tests/
│   ├── test_features.py
│   ├── test_data_processing.py
│   └── test_api.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── models/
│   └── baseline.joblib
│
└── LICENSE
```

## Limitations & Next Steps

| Area            | Current            | Next Steps                                     |
| --------------- | ------------------ | ---------------------------------------------- |
| **Data**        | Synthetic          | Use real datasets (e.g., PhishTank, OpenPhish) |
| **Features**    | 10 basic           | Add JS, WHOIS, SSL, domain age                 |
| **Model**       | RandomForest       | Try XGBoost, LSTM, BERT                        |
| **Security**    | No auth/rate-limit | Add JWT, API key, and rate limiting            |
| **Performance** | Synchronous fetch  | Switch to async (`aiohttp`)                    |


## Contributing

1. Fork the repo

2. Create your feature branch

3. Commit your changes

4. Run tests & lint locally

5.5 Open a Pull Request

Contributions are welcome!

## Maintainers

Author: **Mantra Patil**

[LinkedIn – Mantra Patil](https://www.linkedin.com/in/mantrapatil25/) 

GitHub: https://github.com/mantrapatil03

Email: techmantrapatil@gmail.com



<p align="center">***If you find this project useful, please ⭐ star this repository and share it with others!***

<p align="center"> <sub>Built with ❤️ by the CodeM03 organization — Stay safe online 🕵️‍♂️</sub> </p>
