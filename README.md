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
