# Security

## Reporting a vulnerability

Please open a private security advisory on this repository (Security tab -> Report a vulnerability) rather than a public issue.

## Known issue: shipped `File_Encrypt.exe` bundles outdated libraries

The `File_Encrypt.exe` currently tracked in `main` was built with PyInstaller in April 2023 (Python 3.11.3) and embeds the following third-party libraries, per the `sources.zip` build manifest:

| Library      | Bundled version | Status                                            |
|--------------|-----------------|---------------------------------------------------|
| cryptography | 40.0.2          | vulnerable — multiple CVEs fixed in later releases |
| setuptools   | 65.5.0          | vulnerable — CVEs fixed in later releases          |
| pycryptodome | unknown         | recommend upgrading to >= 3.20.0                   |

Notable advisories that apply to the bundled versions:

- `cryptography` 40.0.2
  - CVE-2023-49083 (NULL-dereference loading PKCS7 certificates) — fixed in 41.0.6
  - CVE-2023-50782 (Bleichenbacher timing oracle on RSA PKCS#1 v1.5) — fixed in 42.0.0
  - CVE-2024-26130 (NULL-dereference in PKCS12 loading) — fixed in 42.0.4
  - Vendored OpenSSL security fixes shipped in 41.0.x / 42.0.x / 43.0.x
- `setuptools` 65.5.0
  - CVE-2022-40897 (ReDoS in `PackageIndex`) — fixed in 65.5.1
  - CVE-2024-6345 (RCE via `package_index.py`) — fixed in 70.0.0
  - CVE-2025-47273 (path traversal in `PackageIndex.download`) — fixed in 78.1.1

Rebuild `File_Encrypt.exe` against the versions pinned in `requirements.txt` before further distribution.

## Rebuilding safely

From a clean Python 3.11+ environment on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile File_Encrypt.py
```

The refreshed executable will be produced under `dist\File_Encrypt.exe`.
