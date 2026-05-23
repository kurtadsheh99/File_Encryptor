# Security Policy

## Reporting a Vulnerability

If you discover a security issue in File_Encryptor, please open a private
security advisory on GitHub (Security tab → Report a vulnerability) instead
of filing a public issue. Include reproduction steps, affected version,
and your OS so the fix can be verified.

## Known Issue with the Currently Published Binary

`File_Encrypt.exe` checked into this repository is a PyInstaller bundle
produced in April 2023. The bundle embeds its own copies of Python, OpenSSL,
and several PyPI packages, and the embedded versions are out of date and
contain known vulnerabilities.

### Affected components inside the bundle

| Component               | Bundled Version | Status                                                                 |
| ----------------------- | --------------- | ---------------------------------------------------------------------- |
| `cryptography` (PyPI)   | 40.0.2          | CVE-2023-49083, CVE-2023-50782, CVE-2024-26130, CVE-2024-0727          |
| OpenSSL (libcrypto-1_1) | 1.1.1           | End-of-life since 2023-09-11; numerous unpatched CVEs                  |
| Python runtime          | 3.11.3          | CVE-2023-40217, CVE-2024-0397, CVE-2024-6232, CVE-2024-8088 and others |
| `pycryptodome` (Crypto) | unknown         | Recommend upgrading to a current release                               |

The cryptographic primitives the application calls (`Fernet`, AES-CBC via
PyCryptodome) are not themselves broken, but the bundled libraries that
implement them have known flaws and the bundled OpenSSL is no longer
receiving any patches.

### Recommendation

Do not rely on the published `File_Encrypt.exe` for new work. Rebuild the
binary from source against current versions of the dependencies pinned in
[`requirements.txt`](./requirements.txt), following the steps in
[`BUILDING.md`](./BUILDING.md). The rebuilt binary will use a supported
Python runtime, a supported OpenSSL, and a patched `cryptography` release.

### Tracking

A refreshed binary will be published as a new release in this repository
once it has been rebuilt and re-tested. Until then this advisory stands.
