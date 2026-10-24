# 🛡️ R i d o x - Ultimate Web Vulnerability Scanner

**R i d o x** is a fast, lightweight, and accurate web vulnerability scanner written in Python. It is designed for security researchers and bug bounty hunters who demand **accuracy over noise**. 

Unlike traditional scanners that produce dozens of false positives, **R i d o x** relies on a **Proof-of-Concept (PoC) validation engine** to ensure that every reported vulnerability is actually exploitable.

---

## 🚀 Features

- **Zero False Positives**: Built-in signature validation for exposed files.
- **Advanced Soft 404 Calibration**: Automatically detects dynamic error pages to prevent false positives.
- **XSS Validation Engine**: Extracts real forms and tests both `GET` and `POST` requests.
- **SQL Error Detection**: Injects payloads to detect database misconfigurations.
- **WAF Detection**: Identifies if the target is protected by Cloudflare, Akamai, or Sucuri.
- **SSL/TLS Verification**: Strict certificate validation to catch expired certificates.
- **Beautiful Terminal UI**: A sleek red/black hacker-style interface.

---

## 📦 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/ahmedridox-create/ridox-scanner.git
cd ridox-scanner
2.Install the required dependencies:

bash
pip install -r requirements.txt
