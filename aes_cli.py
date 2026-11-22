#!/usr/bin/env python3
"""
AES Text Encryptor - a command-line program that encrypts and decrypts text.

ENCRYPTION ALGORITHM USED: AES-256 in GCM mode (Advanced Encryption Standard,
256-bit key, Galois/Counter Mode). The key is made from the user's password
with PBKDF2-HMAC-SHA256 (600,000 iterations) and a random salt.

Index number: 10374922
"""
import argparse
import base64
import getpass
import os
import sys

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ALGORITHM = "AES-256-GCM (key from password via PBKDF2-HMAC-SHA256)"
SALT_SIZE = 16      # bytes, random for every message
NONCE_SIZE = 12     # bytes, random for every message (standard for GCM)
ITERATIONS = 600_000


def derive_key(password: str, salt: bytes) -> bytes:
    """Turn a password into a 32-byte (256-bit) AES key."""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS)
    return kdf.derive(password.encode("utf-8"))


def encrypt_text(plain_text: str, password: str) -> str:
    """Encrypt text and return a Base64 string (salt + nonce + ciphertext + tag)."""
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, plain_text.encode("utf-8"), None)
    return base64.b64encode(salt + nonce + ciphertext).decode("ascii")


def decrypt_text(token: str, password: str) -> str:
    """Decrypt a Base64 string made by encrypt_text. Raises ValueError on failure."""
    try:
        raw = base64.b64decode(token.strip(), validate=True)
    except Exception:
        raise ValueError("That is not valid encrypted text (bad Base64).")
    if len(raw) < SALT_SIZE + NONCE_SIZE + 16:
        raise ValueError("Encrypted text is too short to be valid.")
    salt = raw[:SALT_SIZE]
    nonce = raw[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = raw[SALT_SIZE + NONCE_SIZE:]
    key = derive_key(password, salt)
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, None).decode("utf-8")
    except InvalidTag:
        raise ValueError("Decryption failed: wrong password or the text was changed.")


def ask_password(confirm: bool = False) -> str:
    while True:
        pw = getpass.getpass("Enter password (hidden): ")
        if not pw:
            print("Password cannot be empty.")
            continue
        if confirm and getpass.getpass("Confirm password: ") != pw:
            print("Passwords do not match. Try again.")
            continue
        return pw


def do_encrypt() -> None:
    text = input("Enter the plain text to encrypt: ")
    if not text:
        print("Nothing to encrypt.")
        return
    token = encrypt_text(text, ask_password(confirm=True))
    print("\nEncrypted text (copy all of it):")
    print(token)


def do_decrypt() -> None:
    token = input("Paste the encrypted text: ")
    try:
        print("\nDecrypted text:", decrypt_text(token, ask_password()))
    except ValueError as err:
        print("\nError:", err)


def menu() -> None:
    print("=" * 56)
    print(" AES TEXT ENCRYPTOR")
    print(f" Algorithm: {ALGORITHM}")
    print("=" * 56)
    while True:
        print("\n1) Encrypt text\n2) Decrypt text\n3) Quit")
        choice = input("Choose 1, 2 or 3: ").strip()
        if choice == "1":
            do_encrypt()
        elif choice == "2":
            do_decrypt()
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Please type 1, 2 or 3.")


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Encrypt/decrypt text with {ALGORITHM}.")
    parser.add_argument("mode", nargs="?", choices=["encrypt", "decrypt"],
                        help="skip the menu and run one action directly")
    parser.add_argument("-t", "--text", help="plain text (encrypt) or encrypted text (decrypt)")
    parser.add_argument("-p", "--password", help="password (if omitted you are asked, hidden)")
    args = parser.parse_args()

    if not args.mode:
        try:
            menu()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
        return

    text = args.text if args.text is not None else input("Text: ")
    password = args.password or ask_password(confirm=(args.mode == "encrypt"))
    try:
        print(encrypt_text(text, password) if args.mode == "encrypt" else decrypt_text(text, password))
    except ValueError as err:
        print("Error:", err, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
