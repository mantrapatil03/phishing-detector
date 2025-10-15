# Phishing Detection — Security Policy & Responsible Disclosure

## Overview

The Phishing Detection project prioritizes security, privacy, and model integrity across all stages — from data ingestion to deployment.
This document defines our security practices, responsible disclosure guidelines, and risk mitigation strategies for contributors, users, and researchers.

## Supported Versions
| Version              | Supported | Notes                                    |
| -------------------- | --------- | ---------------------------------------- |
| `main` (latest)      | ✅         | Actively maintained and patched.         |
| `v1.x`               | ⚠️        | Limited support for critical fixes only. |
| Pre-release branches | ❌         | Not recommended for production use.      |

>Always deploy the latest stable version. Outdated dependencies or models may expose security risks.

## 📣 Reporting a Vulnerability

We take all security reports seriously.
If you discover a vulnerability, please report it privately and responsibly.

**📬 Contact Options**

- Email: techmantrapatil@gmail.com
- Optional PGP Encryption:
    ```vbnet
    -----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: OpenPGP
    
    mQINBGU0j0YBEAC6N... [Example Key Block] ...z1kP
    -----END PGP PUBLIC KEY BLOCK-----
    ```
Include in Your Report

- Summary of the issue and potential impact.
- Steps to reproduce or proof-of-concept (if safe).
- Affected files or components.
- Suggested mitigation (optional).

Our Commitment

- Response: within 48–72 hours
- Verification & Fix: within 7–14 business days

## Responsible Disclosure Policy

To protect the community and our users:

You agree not to:

- Disclose the issue publicly before it is fixed.
- Access, modify, or damage non-public systems or data.
- Conduct denial-of-service, data exfiltration, or privacy-invasive tests.

We commit to:

- Transparent and timely communication.
- Fair credit and recognition.
- Non-retaliation toward researchers acting in good faith.

## Machine Learning Security Policy

1. Model Integrity & Verification

    - Every model in `/models/` is cryptographically hashed (SHA-256).
    - Use the verification utility in `ml_helpers.py`:
        ```python
        from src.ml_helpers import verify_model_integrity
        verify_model_integrity("models/baseline.joblib", "expected_hash_here")
        ```

    - All model updates are signed and version-tagged via Git.

2. Adversarial & Data Poisoning Defense

    - Continuous evaluation against adversarially crafted URLs and feature perturbations.

    - Automatic data validation pipelines in `data_processing.py` flag statistical anomalies.

    - Isolation of untrusted or external datasets to sandboxed environments.

3. Privacy & Data Protection

    - Strict adherence to GDPR and ISO/IEC 27001 principles for data handling.

    - Sensitive data (API keys, tokens) stored only in `.env` and excluded via `.gitignore`.

    - Use `dotenv` and encrypted storage for runtime secrets.

## Deployment & Infrastructure Security

| Category           | Recommended Practice                                                            |
| ------------------ | ------------------------------------------------------------------------------- |
| **Isolation**      | Run the system in Docker with non-root users and minimal privileges.            |
| **Network**        | Limit open ports, enforce HTTPS, use firewalls & reverse proxies (e.g., Nginx). |
| **Secrets**        | Manage credentials via secure vaults (AWS Secrets Manager, Vault, or Doppler).  |
| **Environment**    | Never commit `.env` files. Example configuration provided as `.env.example`.    |
| **Dependencies**   | Pin all dependencies and run `pip-audit` weekly for CVE checks.                 |
| **Image Security** | Use tools like **Trivy**, **Grype**, or **Dockle** to scan base images.         |
| **Logging**        | Sanitize logs to prevent leakage of sensitive URLs or credentials.              |
| **Monitoring**     | Integrate with centralized SIEM systems (ELK, Grafana Loki, Wazuh).             |

## Continuous Security Integration (CI/CD)

This repository uses GitHub Actions (.github/workflows/ci.yml) for automated security enforcement:

| Check                | Tool / Action               | Purpose                               |
| -------------------- | --------------------------- | ------------------------------------- |
| Static Code Analysis | `bandit`, `flake8`          | Detects insecure code patterns        |
| Dependency Scanning  | `pip-audit`, `Dependabot`   | Flags vulnerable libraries            |
| Model Integrity      | Custom SHA verifier         | Ensures no tampered ML artifacts      |
| Container Scan       | `aquasecurity/trivy-action` | Checks Docker image CVEs              |
| Secrets Scan         | `gitleaks`                  | Prevents secret leakage during commit |

## Hardening Guidelines

For Contributors

- Run `pre-commit` hooks to lint and check for secrets before pushing code.

- Keep branches rebased with `main` to receive patched security updates.

- Use virtual environments (`venv`, `conda`, or Docker dev containers`).

For Deployers

- Rotate all keys and credentials periodically.

- Enforce least-privilege IAM roles.

- Audit Docker and server logs monthly.

- Configure security headers (HSTS, CSP, X-Frame-Options).

## 🧾 Security Audit & Compliance Log
| Date       | Scope            | Action Taken                                      | Status |
| ---------- | ---------------- | ------------------------------------------------- | ------ |
| 2025-10-12 | Repo Setup       | Added advanced `SECURITY.md` & CI hardening       | ✅      |
| 2025-09-30 | Dependency Audit | Upgraded `scikit-learn`, `pandas`, and `requests` | ✅      |
| 2025-09-18 | Docker Review    | Implemented non-root user & pinned base image     | ✅      |

## Legal Notice

This project is distributed under the MIT License (see `LICENSE`).
All contributors and users agree not to use this project for illegal, malicious, or unauthorized surveillance activities.
Maintainers are not liable for misuse or derivative works deployed outside ethical and educational contexts.

## Final Note

- Security is a continuous process.
- We encourage collaboration, responsible research, and ethical development to make phishing detection and machine learning safer for all.

>“Build with security in mind — not as an afterthought.”
