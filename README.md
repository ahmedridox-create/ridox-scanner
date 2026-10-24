# 🛡️ R i d o x - Ultimate Web Vulnerability Scanner

**R i d o x** is a fast, lightweight, and aggressive web vulnerability scanner written in Python. It is designed for security researchers and bug bounty hunters who demand **accuracy over noise**. 

Unlike traditional scanners that produce dozens of false positives, **R i d o x** relies on a **Proof-of-Concept (PoC) validation engine** to ensure that every reported vulnerability is actually exploitable.

## 🚀 Features

- **Zero False Positives**: Built-in signature validation for exposed files. If it says `.env` is exposed, it means it *is* exposed.
- **Advanced Soft 404 Calibration**: Automatically detects dynamic error pages to prevent false positives during directory scanning.
- **XSS Validation Engine**: Extracts real forms and URL parameters, testing both `GET` and `POST` requests with unencoded payload reflection checks.
- **SQL Error Detection**: Injects error-based payloads to detect database misconfigurations.
- **WAF Detection**: Identifies if the target is protected by Cloudflare, Akamai, or Sucuri, so you know when results might be blocked.
- **SSL/TLS Verification**: Strict certificate validation to catch expired or self-signed certificates.
- **Beautiful Terminal UI**: A sleek red/black hacker-style interface with real-time output.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ahmedridox-create/ridox-scanner.git
   cd ridox-scanner
