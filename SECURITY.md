# Security Policy

## Reporting a Vulnerability

To report a vulnerability, please open a private security advisory on this
repository or open an issue describing the problem, the affected version,
and (if possible) reproduction steps. Avoid posting working exploits
publicly.

## Known Issues in Shipped Binary

The committed `File_Encrypt.exe` and `sources.zip` archive were produced
with PyInstaller in 2023. Inspection of the bundled distribution metadata
(see `sources.zip` -> `sources/File_Encrypt/PKG-00.toc`) shows the binary
ships with the following outdated, vulnerable components:

| Component               | Bundled version | Known issues (fixed in)                                                                 |
| ----------------------- | --------------- | --------------------------------------------------------------------------------------- |
| `cryptography` (pyca)   | 40.0.2          | CVE-2023-49083 (41.0.6), CVE-2023-50782 (42.0.0), CVE-2024-0727 (42.0.2), CVE-2024-26130 (42.0.4) |
| `setuptools`            | 65.5.0          | CVE-2022-40897 ReDoS (65.5.1), CVE-2024-6345 RCE in `package_index` (70.0.0)            |
| `libcrypto-1_1.dll`     | OpenSSL 1.1.x   | OpenSSL 1.1.1 reached end-of-life on 2023-09-11; no further security fixes              |
| CPython runtime         | 3.11.1          | Multiple CVEs fixed in subsequent 3.11.x and 3.12+ releases                             |

Because these components are statically embedded in the PyInstaller
bundle, `pip` upgrades on an end-user machine do not remediate the
shipped binary. The executable must be rebuilt against current
dependencies and re-published.

## Remediation

A safe rebuild should:

1. Use the pinned floors in `requirements.txt` (or newer).
2. Use a supported CPython release (3.12 or later recommended).
3. Use a current PyInstaller (>= 6.10) so OpenSSL 3.x is bundled via the
   refreshed `cryptography` wheels.
4. Replace `File_Encrypt.exe` and `sources.zip` in the repository with
   the freshly built artifacts.

Until a rebuild is published, users should treat the existing binary as
unsupported for security-sensitive use.
