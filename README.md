# AES Text Encryptor (Command-Line Program)

**Name:** Addo Wesley Owereko
**Index Number:** 10374922
**Class:** IT2 Evening
**Language:** Python 3

## Encryption algorithm used

**AES-256 in GCM mode** (Advanced Encryption Standard, 256-bit key, Galois/Counter Mode).

- AES is a **symmetric** algorithm: the same secret key locks (encrypts) and unlocks (decrypts) the text.
- The 256-bit key is made from the user's **password** using **PBKDF2-HMAC-SHA256** (600,000 rounds) and a random **salt**.
- **GCM mode** also checks that the message was not changed. A wrong password or edited text gives a clear error instead of nonsense.
- Every encryption uses a new random salt and nonce, so encrypting the same text twice gives different results.

### Explained simply
Think of a **padlock on a school locker**. Your password is the key. AES scrambles your message so only someone with the same key can read it. The salt is like adding a different random pattern to the lock every time, so a thief cannot reuse one trick on all lockers. GCM is a seal: if anyone tampers with the locker, you will know.

## Features
- Enter plain text, get encrypted text (Base64) back
- Paste encrypted text and the password, get the original text back
- Hidden password input (not shown on screen)
- Friendly errors for a wrong password or damaged text
- Menu mode and quick command mode
- Unit tests

## How to run

1. Install Python 3.8 or newer.
2. Install the one library needed:
   ```
   pip install -r requirements.txt
   ```
3. Start the program:
   ```
   python aes_cli.py
   ```

### Menu mode
```
========================================================
 AES TEXT ENCRYPTOR
 Algorithm: AES-256-GCM (key from password via PBKDF2-HMAC-SHA256)
========================================================

1) Encrypt text
2) Decrypt text
3) Quit
Choose 1, 2 or 3: 1
Enter the plain text to encrypt: Meet me at UPSA at 8am
Enter password (hidden):
Confirm password:

Encrypted text (copy all of it):
7l3uGvZ0JDqAdVyMDLDlEDB0M0ONh7C8vpNLaD9PS40X7lPVZlIjGbbhp0UR/sG0Wdx6/lqAN4Q9fC1rd60S7JW9
```
Then choose `2`, paste the encrypted text, enter the same password, and the original text appears.

### Quick command mode
```
python aes_cli.py encrypt -t "Meet me at UPSA at 8am" -p mypass
python aes_cli.py decrypt -t "<encrypted text>" -p mypass
```
(If you leave out `-p`, the program asks for the password with hidden input, which is safer because command-line passwords can be seen in your command history.)

## Run the tests
```
python -m unittest -v
```

## Files
| File | Purpose |
|---|---|
| `aes_cli.py` | The program (encryption, decryption and menu) |
| `test_aes_cli.py` | Unit tests |
| `requirements.txt` | Library needed (`cryptography`) |
| `README.md` | This file |

## Security notes
- Keep your password secret. If it is lost, the text **cannot** be recovered.
- Use a long password. Short passwords can be guessed even with strong encryption.
- This is a learning project. For real systems, use well-reviewed tools.
