# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| latest  | yes       |

Older versions are not maintained; always use the most recent release.

## Reporting a Vulnerability

Please open a GitHub issue describing how the issue was found and how it can
be reproduced. Include your operating system version. Screenshots are
appreciated — mask any sensitive information before posting.

## Known Advisory: Dependencies Bundled In Previous Releases

The previously-published `File_Encrypt.exe` was built with a frozen snapshot
of Python 3.11.3 and the following third-party packages, which are known to
have published CVEs:

| Package      | Version in old build | Known CVEs                                             |
| ------------ | -------------------- | ------------------------------------------------------ |
| cryptography | 40.0.2               | CVE-2023-38325, CVE-2023-49083, CVE-2023-50782, CVE-2024-26130, and others; fixed in >= 46.0.6 |
| pycryptodome | 3.17                 | GHSA-j225-cvw7-qrx7 (Marvin side-channel in RSA-OAEP); fixed in >= 3.19.1                       |
| setuptools   | 65.5.0               | CVE-2022-40897, CVE-2024-6345, CVE-2025-47273; fixed in >= 84.1.0                               |
| jinja2       | 3.1.2                | CVE-2024-22195, CVE-2024-34064, CVE-2024-56201, CVE-2024-56326, CVE-2025-27516; fixed in >= 3.1.6 |

Note: this application performs local AES / Fernet file encryption and does
not use the vulnerable code paths of these libraries over the network, so the
exploitability of the above CVEs against this particular program is limited.
They are listed here because any user running the executable loads a Python
runtime that contains them, and future changes to the program could reach
affected code paths.

### Mitigation

`requirements.txt` in the repository root now pins minimum versions that
clear all currently indexed CVEs for the dependencies above. Rebuild the
executable from the project's `.py` source with those versions before
publishing a new release:

```powershell
python -m pip install --upgrade -r requirements.txt
python -m PyInstaller --onefile --noconsole File_Encrypt.py
```

After rebuilding, replace `File_Encrypt.exe` in this repository and in any
distribution channels, then re-run `pip-audit -r requirements.txt` to
confirm the new build has no outstanding advisories.
