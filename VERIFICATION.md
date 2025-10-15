# Verification & Integrity Policy

The Phishing Detection project enforces strict cryptographic and operational verification standards to maintain trust in its models, dependencies, and releases.

## 1. Model Integrity Verification
Every model distributed through this repository (`/models/*.joblib`) includes a SHA-256 hash for verification.

** Verification Steps**

Run the built-in helper before loading a model:
```python
from src.ml_helpers import verify_model_integrity

verify_model_integrity(
    model_path="models/baseline.joblib",
    expected_hash="6a9b1e7f1a24b6b8b1298db821fdf0d4e22ad0f5b8a1c33e2e2b982e9af3aef7"
)
```
**📋 Expected Output**
```nginx
Model integrity verified successfully.
```

If the hash doesn’t match:
```sql
Integrity check failed: possible tampering or corruption detected.
```

## 2. Dependency Trust & Validation
We ensure reproducibility and trust in dependencies.

** Verification Checklist **

| Step               | Tool                  | Purpose                                 |
| ------------------ | --------------------- | --------------------------------------- |
| Dependency Lock    | `requirements.txt`    | Ensures version consistency             |
| Vulnerability Scan | `pip-audit`, `bandit` | Detects CVEs                            |
| Integrity Pin      | `hashin` (optional)   | Adds hash checks to `requirements.txt`  |
| Build Verification | CI/CD workflow        | Confirms clean reproducible environment |

>Command:
```bash
pip install -r requirements.txt --require-hashes
```

## 3. Release Authenticity

All official releases and Docker images are:

- Built via GitHub Actions CI, not manual uploads.
- Tagged and signed using GPG for authenticity.
- Accompanied by a release manifest (release-signature.txt).

**Example**:
```makefile
phishing-detection-v1.0.0.tar.gz
SHA256: e2b1d3e98f6a7a7fa09b7eaf0e7c814b5cbe8f27bdf8e221d2b0e5df98c6a8c1
Signature: release-signature.asc
```
To verify:
```bash
gpg --verify release-signature.asc phishing-detection-v1.0.0.tar.gz
```

## 4. Model Reproducibility (Optional)

For verified research builds:
```bash
python src/train.py --seed 42 --deterministic
```
This ensures consistent model weights and eliminates randomness that could affect security audits.

## 5. Continuous Verification Pipeline
Automated integrity checks are part of CI/CD:

| Component    | Check Type               | Tool                   |
| ------------ | ------------------------ | ---------------------- |
| Code         | Static Security Scan     | Bandit                 |
| Models       | SHA256 Verification      | Custom script          |
| Docker       | Image Vulnerability Scan | Trivy                  |
| Dependencies | CVE Monitoring           | Dependabot / pip-audit |

## 6. Verification Logs

| Date       | Component    | Verification     | Result |
| ---------- | ------------ | ---------------- | ------ |
| 2025-10-12 | Model        | SHA-256 verified | ✅      |
| 2025-10-12 | Docker Image | Trivy scan       | ✅      |
| 2025-10-12 | Requirements | pip-audit run    | ✅      |

## Public Key for Signature Verification
```vbnet
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: OpenPGP

mQINBGX1ZxkBEAC3K... [Example Truncated] ...rA==  
=K3a1
-----END PGP PUBLIC KEY BLOCK-----
```
Use this key to verify signed releases and advisories.

## Final Note

These verification measures safeguard against:

- Model tampering or adversarial payload injection

- Dependency-based supply chain attacks

- Unauthorized or unverified builds

Security is everyone’s responsibility — verify before you trust.

>“Integrity is not a feature — it’s a foundation.”
