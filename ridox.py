#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import time
import ssl
import socket
import random
import hashlib
import urllib.parse
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== COLORS ====================
RED = '\033[1;31m'
WHITE = '\033[1;37m'
GRAY = '\033[0;90m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
RESET = '\033[0m'

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
]

SQL_ERRORS = [
    r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"PostgreSQL.*ERROR",
    r"ORA-\d{5}", r"Microsoft.*ODBC.*SQL Server", r"Unclosed quotation mark",
    r"quoted string not properly terminated"
]

def print_banner():
    os.system('clear')
    print(f"""{RED}
    ██████╗ ██╗██████╗  ██████╗ ██╗  ██╗
    ██╔══██╗██║██╔══██╗██╔═══██╗╚██╗██╔╝
    ██████╔╝██║██║  ██║██║   ██║ ╚███╔╝ 
    ██╔══██╗██║██║  ██║██║   ██║ ██╔██╗ 
    ██║  ██║██║██████╔╝╚██████╔╝██╔╝ ██╗
    ╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
    {WHITE}══════════════════════════════════════════{RED}
    {WHITE}[+] R i d o x - Ultimate Scanner (v6.0){RESET}
    {GRAY}    Zero False Positives. Proof of Concept Only.{RESET}
    """)

class UltimateScanner:
    def __init__(self, target):
        self.target = self._normalize(target)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": random.choice(USER_AGENTS)})
        self.session.verify = False
        self.soft404_hashes = set()
        self.soft404_status = None

    @staticmethod
    def _normalize(url):
        if not re.match(r"^https?://", url, re.I):
            url = "https://" + url
        return url

    def _get(self, url, **kwargs):
        kwargs.setdefault("timeout", 10)
        kwargs.setdefault("allow_redirects", True)
        try:
            return self.session.get(url, **kwargs)
        except Exception:
            return None

    def detect_soft_404(self):
        print(f"{GRAY}[*] Calibrating Soft 404 Engine (3 random paths)...{RESET}")
        for _ in range(3):
            rand_path = f"__rand_{random.randint(10000,99999)}_{int(time.time())}__"
            url = f"{self.target.rstrip('/')}/{rand_path}"
            r = self._get(url)
            if r:
                self.soft404_status = r.status_code
                h = hashlib.md5(r.content).hexdigest()
                self.soft404_hashes.add(h)
        
        if not self.soft404_hashes:
            print(f"{YELLOW}[!] Could not calibrate Soft 404. Skipping path scanning.{RESET}")
            return False
        print(f"{GREEN}[✓] Soft 404 calibrated (Status: {self.soft404_status}).{RESET}")
        return True

    def is_soft_404(self, response):
        if not response: return True
        h = hashlib.md5(response.content).hexdigest()
        if h in self.soft404_hashes: return True
        if response.status_code == 404: return True
        return False

    def detect_waf(self):
        print(f"{GRAY}[*] Checking for Web Application Firewall (WAF)...{RESET}")
        r = self._get(self.target)
        if not r: return
        
        headers = str(r.headers).lower()
        wafs = {
            "cloudflare": ["cloudflare", "__cf_bm", "cf-ray"],
            "akamai": ["akamai", "ak_bmsc"],
            "aws": ["awselb", "awsalb"],
            "sucuri": ["sucuri"],
            "imperva": ["incap_ses", "visid_incap"]
        }
        for waf_name, sigs in wafs.items():
            if any(sig in headers for sig in sigs):
                print(f"{YELLOW}[!] WAF Detected: {waf_name.upper()}. Scan might be blocked.{RESET}")
                return
        print(f"{GREEN}[✓] No obvious WAF detected.{RESET}")

    def check_sensitive_files(self):
        print(f"{GRAY}[*] Testing for exposed files (Signature Validation)...{RESET}")
        files = {
            ".env": [b"APP_KEY", b"DB_PASSWORD", b"DB_HOST"],
            ".git/config": [b"[core]", b"repositoryformatversion"],
            "backup.sql": [b"INSERT INTO", b"CREATE TABLE", b"MySQL dump"],
            "id_rsa": [b"BEGIN RSA PRIVATE KEY"]
        }
        
        found = False
        for path, sigs in files.items():
            url = f"{self.target.rstrip('/')}/{path}"
            r = self._get(url)
            
            if self.is_soft_404(r): continue
            if r.status_code != 200: continue
            if b"<html" in r.content[:300].lower(): continue

            if any(sig in r.content for sig in sigs):
                print(f"{RED}[VULN] [CRITICAL] Real File Exposed: /{path}{RESET}")
                print(f"       {GRAY}Size: {len(r.content)}B | Hash: {hashlib.md5(r.content).hexdigest()[:8]}{RESET}")
                found = True
        
        if not found:
            print(f"{GREEN}[✓] No exposed files found.{RESET}")

    def check_xss(self):
        print(f"{GRAY}[*] Testing for XSS (GET & POST forms)...{RESET}")
        payload = "<script>alert('XSS_RIDOX')</script>"
        
        r = self._get(self.target)
        if not r: return

        parsed = urllib.parse.urlparse(self.target)
        params = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
        
        if params:
            for p in params:
                test_params = {p: payload}
                test_url = urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(test_params)))
                res = self._get(test_url)
                if res and payload in res.text:
                    print(f"{RED}[VULN] [HIGH] Reflected XSS (GET) via '{p}'{RESET}")
                    print(f"       {GRAY}URL: {test_url}{RESET}")
                    return

        forms = re.findall(r'<form[^>]*action=["\']?([^"\'>]+)["\']?[^>]*>(.*?)</form>', r.text, re.I | re.S)
        for action, body in forms[:3]:
            inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\']', body)
            if not inputs: continue
            
            post_url = urllib.parse.urljoin(self.target, action) if action else self.target
            data = {i: payload for i in inputs}
            
            try:
                res = self.session.post(post_url, data=data, timeout=10)
                if payload in res.text:
                    print(f"{RED}[VULN] [HIGH] Reflected XSS (POST) in form action.{RESET}")
                    print(f"       {GRAY}URL: {post_url}{RESET}")
                    return
            except: pass

        print(f"{GREEN}[✓] No Reflected XSS found (tried GET & POST).{RESET}")

    def check_sqli_errors(self):
        print(f"{GRAY}[*] Checking for SQL Injection errors...{RESET}")
        payloads = ["'", "\"", "1'"]
        parsed = urllib.parse.urlparse(self.target)
        params = urllib.parse.parse_qs(parsed.query)
        
        for p in params:
            for payload in payloads:
                test_params = {p: payload}
                test_url = urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(test_params)))
                r = self._get(test_url)
                if not r: continue
                
                for pattern in SQL_ERRORS:
                    if re.search(pattern, r.text, re.I):
                        print(f"{RED}[VULN] [CRITICAL] SQL Error Detected via '{p}'{RESET}")
                        print(f"       {GRAY}URL: {test_url}{RESET}")
                        return
        print(f"{GREEN}[✓] No SQL errors found.{RESET}")

    def check_ssl_certificate(self):
        print(f"{GRAY}[*] Validating SSL Certificate...{RESET}")
        parsed = urllib.parse.urlparse(self.target)
        host = parsed.hostname
        if not host or parsed.scheme != "https": return

        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((host, 443), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    print(f"{GREEN}[✓] Certificate is valid (Trusted Authority).{RESET}")
        except ssl.SSLCertVerificationError:
            print(f"{RED}[VULN] [HIGH] Invalid SSL Certificate (Self-signed or Expired){RESET}")
        except Exception:
            pass

    def run(self):
        print(f"\n{WHITE}Target: {self.target}{RESET}\n")
        
        self.detect_waf()
        print()
        self.check_ssl_certificate()
        print()
        if self.detect_soft_404():
            self.check_sensitive_files()
        print()
        self.check_xss()
        print()
        self.check_sqli_errors()

        print(f"\n{GRAY}[*] Scan Finished. Remember: Only report what you proved.{RESET}\n")

if __name__ == "__main__":
    print_banner()
    target = input(f"{RED}[?] Enter Target URL (or 'q' to quit): {WHITE}")
    if target.lower() != 'q' and target.strip():
        scanner = UltimateScanner(target)
        scanner.run()
