import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import struct

# AES-GCM encrypted file format:
#   salt (16 bytes) + nonce (12 bytes) + ciphertext+tag (variable)
#
# Key derivation: PBKDF2-HMAC-SHA256, 600_000 iterations
# AES-GCM provides both confidentiality and integrity (no padding oracle risk).

_PBKDF2_ITERATIONS = 600_000
_SALT_LEN = 16
_NONCE_LEN = 12


def _derive_key(password: bytes, salt: bytes, key_len: int) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_len,
        salt=salt,
        iterations=_PBKDF2_ITERATIONS,
    )
    return kdf.derive(password)


class FileEncryptor:
    def __init__(self, master):
        master.title("File Encryptor")

        self.file_path = ""
        self.encryption_type = tk.StringVar(value="AES-256-GCM")
        self.key = tk.StringVar()

        # --- Encryption type ---
        tk.Label(master, text="Encryption Type:").grid(
            row=0, column=0, padx=8, pady=6, sticky="w"
        )
        self.encryption_combobox = ttk.Combobox(
            master,
            textvariable=self.encryption_type,
            values=["AES-128-GCM", "AES-192-GCM", "AES-256-GCM", "Fernet"],
            state="readonly",
            width=20,
        )
        self.encryption_combobox.grid(row=0, column=1, padx=8, pady=6, sticky="w")

        # --- File selection ---
        tk.Button(master, text="Select File", command=self.select_file).grid(
            row=1, column=0, padx=8, pady=4, sticky="w"
        )
        self.file_name_label = tk.Label(master, text="No file selected.", fg="grey")
        self.file_name_label.grid(row=1, column=1, padx=8, pady=4, sticky="w")

        # --- Key / Password ---
        tk.Label(master, text="Password / Key:").grid(
            row=2, column=0, padx=8, pady=4, sticky="w"
        )
        self.key_entry = tk.Entry(master, textvariable=self.key, show="*", width=30)
        self.key_entry.grid(row=2, column=1, padx=8, pady=4, sticky="w")

        # --- Action buttons ---
        tk.Button(master, text="Encrypt", command=self.encrypt, width=18).grid(
            row=3, column=0, padx=8, pady=6
        )
        tk.Button(master, text="Decrypt", command=self.decrypt, width=18).grid(
            row=3, column=1, padx=8, pady=6, sticky="w"
        )
        tk.Button(
            master,
            text="Generate Fernet Key",
            command=self.generate_fernet_key,
            width=20,
        ).grid(row=4, column=0, columnspan=2, padx=8, pady=4)

        # --- Status ---
        self.status_label = tk.Label(master, text="", fg="blue")
        self.status_label.grid(row=5, column=0, columnspan=2, padx=8, pady=6)

    def _set_status(self, msg: str, error: bool = False):
        self.status_label.config(text=msg, fg="red" if error else "green")

    def select_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path = path
            self.file_name_label.config(text=os.path.basename(path), fg="black")

    def generate_fernet_key(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".key",
            filetypes=[("Key files", "*.key"), ("All files", "*.*")],
            title="Save Fernet Key",
        )
        if not save_path:
            return
        fk = Fernet.generate_key()
        with open(save_path, "wb") as f:
            f.write(fk)
        self._set_status(f"Fernet key saved to {os.path.basename(save_path)}")

    # ------------------------------------------------------------------
    # Encryption
    # ------------------------------------------------------------------

    def encrypt(self):
        if not self.file_path:
            self._set_status("No file selected.", error=True)
            return

        password = self.key.get()
        if not password:
            self._set_status("Password/key is required.", error=True)
            return

        enc_type = self.encryption_type.get()

        try:
            with open(self.file_path, "rb") as f:
                plaintext = f.read()

            if enc_type in ("AES-128-GCM", "AES-192-GCM", "AES-256-GCM"):
                key_len = {"AES-128-GCM": 16, "AES-192-GCM": 24, "AES-256-GCM": 32}[
                    enc_type
                ]
                salt = os.urandom(_SALT_LEN)
                nonce = os.urandom(_NONCE_LEN)
                key_bytes = _derive_key(password.encode(), salt, key_len)
                aesgcm = AESGCM(key_bytes)
                ciphertext = aesgcm.encrypt(nonce, plaintext, None)

                out_path = self.file_path + ".enc"
                with open(out_path, "wb") as f:
                    f.write(salt + nonce + ciphertext)

            elif enc_type == "Fernet":
                # Fernet key must be 32 url-safe base64 bytes; treat user input
                # as the key directly (generated via Generate Fernet Key button).
                try:
                    fernet_key = password.encode()
                    cipher = Fernet(fernet_key)
                except Exception:
                    self._set_status(
                        "Invalid Fernet key. Use 'Generate Fernet Key' to create one.",
                        error=True,
                    )
                    return
                ciphertext = cipher.encrypt(plaintext)
                out_path = self.file_path + ".enc"
                with open(out_path, "wb") as f:
                    f.write(ciphertext)

            else:
                self._set_status("Unknown encryption type.", error=True)
                return

            self._set_status(
                f"Encrypted → {os.path.basename(out_path)}"
            )

        except OSError as e:
            self._set_status(f"File error: {e}", error=True)
        except Exception as e:
            self._set_status(f"Encryption failed: {e}", error=True)

    # ------------------------------------------------------------------
    # Decryption
    # ------------------------------------------------------------------

    def decrypt(self):
        if not self.file_path:
            self._set_status("No file selected.", error=True)
            return

        password = self.key.get()
        if not password:
            self._set_status("Password/key is required.", error=True)
            return

        enc_type = self.encryption_type.get()

        try:
            with open(self.file_path, "rb") as f:
                data = f.read()

            if enc_type in ("AES-128-GCM", "AES-192-GCM", "AES-256-GCM"):
                min_len = _SALT_LEN + _NONCE_LEN + 16  # 16-byte GCM tag minimum
                if len(data) < min_len:
                    self._set_status("File is too short or corrupted.", error=True)
                    return

                salt = data[:_SALT_LEN]
                nonce = data[_SALT_LEN: _SALT_LEN + _NONCE_LEN]
                ciphertext = data[_SALT_LEN + _NONCE_LEN:]

                key_len = {"AES-128-GCM": 16, "AES-192-GCM": 24, "AES-256-GCM": 32}[
                    enc_type
                ]
                key_bytes = _derive_key(password.encode(), salt, key_len)
                aesgcm = AESGCM(key_bytes)
                try:
                    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
                except Exception:
                    self._set_status(
                        "Decryption failed: wrong password or corrupted file.",
                        error=True,
                    )
                    return

            elif enc_type == "Fernet":
                try:
                    fernet_key = password.encode()
                    cipher = Fernet(fernet_key)
                    plaintext = cipher.decrypt(data)
                except InvalidToken:
                    self._set_status(
                        "Decryption failed: wrong key or corrupted file.", error=True
                    )
                    return
                except Exception as e:
                    self._set_status(f"Decryption failed: {e}", error=True)
                    return

            else:
                self._set_status("Unknown encryption type.", error=True)
                return

            out_path = (
                self.file_path[:-4]
                if self.file_path.endswith(".enc")
                else self.file_path + ".dec"
            )
            with open(out_path, "wb") as f:
                f.write(plaintext)

            self._set_status(f"Decrypted → {os.path.basename(out_path)}")

        except OSError as e:
            self._set_status(f"File error: {e}", error=True)
        except Exception as e:
            self._set_status(f"Decryption failed: {e}", error=True)


if __name__ == "__main__":
    root = tk.Tk()
    FileEncryptor(root)
    root.mainloop()
