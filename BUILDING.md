# Building File_Encryptor from source

The `File_Encrypt.exe` checked into this repo was built in April 2023 and
embeds outdated, vulnerable copies of Python, OpenSSL, and the
`cryptography` package. See [`SECURITY.md`](./SECURITY.md) for the list
of CVEs. Rebuild from source as described below before relying on the
binary.

## Prerequisites

- Windows 10 or 11 (the app uses `tkinter`, which ships with Python)
- Python 3.11.9 or newer (3.12.x recommended). Download from
  <https://www.python.org/downloads/>.
- A copy of `File_Encrypt.py` (the original source). If you only have
  the historical `.exe`, recover the source from your own working copy
  rather than from the binary.

## Build steps

```powershell
# 1. Create and activate a clean virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install pinned, patched dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3. Sanity-check the installed versions
python -m pip list | Select-String "cryptography|pycryptodome|cffi|pyinstaller"

# 4. Build a single-file executable
pyinstaller --onefile --noconsole --name File_Encrypt File_Encrypt.py
```

The fresh binary is written to `dist\File_Encrypt.exe`.

## Verifying the rebuilt binary

After the build, confirm that the embedded `cryptography` dist-info
reports the patched version:

```powershell
# Extract the PyInstaller archive (one-off, for verification only)
python -m pip install pyinstaller-utils    # provides pyi-archive_viewer
pyi-archive_viewer dist\File_Encrypt.exe
```

Look for a `cryptography-44.*.dist-info` entry and confirm there is no
`libssl-1_1.dll` / `libcrypto-1_1.dll` left over from the old build —
modern `cryptography` wheels statically link OpenSSL 3.x.

## Publishing

Once the binary has been rebuilt and tested:

1. Replace `File_Encrypt.exe` in the repo root with the new build.
2. Note the rebuild in the release notes, referencing this advisory.
3. Update `SECURITY.md` to record the date the advisory was resolved.
