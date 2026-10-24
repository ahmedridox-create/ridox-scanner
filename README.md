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
   Install the required dependencies:

   ```bash
   pip install -r requirements.txt
(If you encounter externally-managed-environment, use a virtual environment: python3 -m venv .venv && source .venv/bin/activate):

Run the tool:

   ```bash
    python3 ridox.py

💻 Usage
   ```bash 
   python3 ridox.py
Enter the target URL (e.g., https://example.com).

The scanner will automatically:

Check for WAF protection.

Validate SSL certificates.

Calibrate Soft 404 baselines.

Scan for exposed sensitive files.

Test for Reflected XSS (GET/POST).

Check for SQL Injection errors.

Type q to quit the scanner.

⚠️ Legal Disclaimer & Warning
THIS TOOL IS PROVIDED FOR EDUCATIONAL PURPOSES AND AUTHORIZED SECURITY TESTING ONLY.

Do NOT use this tool on any website, server, or network that you do not own or have explicit, written permission to test.

Unauthorized scanning, vulnerability testing, or exploitation is illegal in almost every jurisdiction and is a punishable criminal offense (e.g., under the Computer Fraud and Abuse Act, and local cybercrime laws).

The author (R i d o x / Ahmed) assumes no liability and is not responsible for any misuse, damage, or legal consequences caused by this program.

By using this software, you agree that you are solely responsible for your actions and that you will comply with all applicable local and international laws.

🤝 Contributing
Contributions, issues, and feature requests are welcome!

2.Install the required dependencies:

bash
pip install -r requirements.txt
(If you encounter externally-managed-environment, use a virtual environment:)

bash
python3 -m venv .venv
source .venv/bin/activate
3.Run the tool:

bash
python3 ridox.py
💻 Usage
bash
python3 ridox.py
Enter the target URL (e.g., https://example.com).

The scanner will automatically:

Check for WAF protection.

Validate SSL certificates.

Calibrate Soft 404 baselines.

Scan for exposed sensitive files.

Test for Reflected XSS (GET/POST).

Check for SQL Injection errors.

Type q to quit the scanner.

⚠️ Legal Disclaimer & Warning
THIS TOOL IS PROVIDED FOR EDUCATIONAL PURPOSES AND AUTHORIZED SECURITY TESTING ONLY.

Do NOT use this tool on any website, server, or network that you do not own or have explicit, written permission to test.

Unauthorized scanning, vulnerability testing, or exploitation is illegal in almost every jurisdiction and is a punishable criminal offense (e.g., under the Computer Fraud and Abuse Act, and local cybercrime laws).

The author (R i d o x / Ahmed) assumes no liability and is not responsible for any misuse, damage, or legal consequences caused by this program.

By using this software, you agree that you are solely responsible for your actions and that you will comply with all applicable local and international laws.

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

Created with ❤️ by Ahmed (R i d o x)
