# File_Encryptor

Application that encrypts and decrypts files. The app supports AES-128,
192, and 256-bit encryption flavors, in addition to Fernet.

## Security notice

> **The `File_Encrypt.exe` currently in this repository was built in
> April 2023 and embeds outdated, vulnerable versions of Python, OpenSSL
> 1.1.1 (end-of-life), and the `cryptography` package. Do not rely on it
> for new work.**
>
> See [`SECURITY.md`](./SECURITY.md) for the full list of affected
> components and [`BUILDING.md`](./BUILDING.md) for instructions to
> rebuild the binary against the patched dependencies pinned in
> [`requirements.txt`](./requirements.txt).
