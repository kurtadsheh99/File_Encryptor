# Security Policy

## Known issue in the currently published binary

The `File_Encrypt.exe` artifact and `sources.zip` PyInstaller build in
this repository were produced against `cryptography==40.0.2` and
`cffi==1.15.1` (Python 3.11.3). The `cryptography` version embedded in
the executable has **16 known vulnerabilities**, including:

| Advisory | Summary | Fixed in |
| --- | --- | --- |
| CVE-2023-50782 | Bleichenbacher timing oracle in RSA decryption | 42.0.0 |
| CVE-2024-0727 | NULL dereference parsing malformed PKCS#12 | 42.0.2 |
| GHSA-jm77-qphf-c4w8 | DoS in OpenSSL POLY1305 MAC | 41.0.3 |
| GHSA-v8gr-m533-ghj9 | Side-channel in RSA decryption | 41.0.4 |
| GHSA-h4gh-qq45-vh27 | NULL deref / DoS in `load_pem_pkcs7_certificates` | 43.0.1 |
| PYSEC-2023-112 | NULL pointer dereference in `idp_full_name` | 41.0.2 |
| PYSEC-2023-254 | NULL pointer dereference in PKCS7 | 41.0.6 |
| PYSEC-2024-225 | NULL pointer dereference in PKCS#12 | 42.0.4 |
| GHSA-5cpq-8wj7-hf2v | OpenSSL buffer overflow | 41.0.0 |

Run `pip-audit -r requirements.txt` against the legacy pins to confirm.

## Recommended remediation

Rebuild `File_Encrypt.exe` from source using the pinned dependencies
in [`requirements.txt`](./requirements.txt):

```
python -m pip install --upgrade -r requirements.txt
pyinstaller --onefile File_Encrypt.py
```

Then replace `File_Encrypt.exe` and `sources.zip` in this repository
with the freshly built artifacts. The Python source for
`File_Encrypt.py` is not currently checked in — please add it so the
binary can be reproduced and audited.

## Reporting a vulnerability

Please open a private security advisory or an issue describing the
issue, the affected version, and steps to reproduce. Redact any
sensitive data from screenshots before attaching them.
