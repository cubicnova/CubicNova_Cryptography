# CubicNova Cryptography: Python

Hands-on Python scripts for learning applied cryptography, from classical ciphers to modern symmetric encryption, RSA and PKI, and secure password hashing.

Each script is self-contained and runnable. Most open with a docstring covering the **theory**, the **algorithm** (step by step) and **sample output**, so the files double as study notes.

> **Educational use only.** These scripts exist to explain concepts. Several deliberately show *insecure* patterns (ECB mode, unsalted SHA-256 for passwords, `random` for keys, unpadded RSA) next to the secure alternatives so the difference is visible. Do not copy the insecure examples into production code.

---

## Contents

| Folder | Topic | Files |
|---|---|---|
| [`cryptography_basics/`](cryptography_basics) | Classical ciphers and a first look at Fernet | 5 |
| [`Symmetric_Encryption/`](Symmetric_Encryption) | Fernet, AES modes, padding, key and IV management | 11 + 1 project brief |
| [`Asymmetric_Encryption/`](Asymmetric_Encryption) | RSA, signatures, certificates, attacks, PKI | 13 |
| [`Hashing/`](Hashing) | Hash functions, salting, Argon2, scrypt, cracking, auth system | 8 + project docs |

```
python/
├── cryptography_basics/
├── Symmetric_Encryption/
├── Asymmetric_Encryption/
└── Hashing/
    └── password-auth-system/      # Flask + MySQL + bcrypt demo app
```

---

## Requirements

- Python 3.9 or newer
- [`cryptography`](https://pypi.org/project/cryptography/) for symmetric, asymmetric and X.509 scripts
- [`argon2-cffi`](https://pypi.org/project/argon2-cffi/) for `6_ARGON2_HASHING.py` only

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install cryptography argon2-cffi
```

`hashlib`, `os`, `itertools` and the other standard-library modules need no installation. Note that `hashlib.scrypt` requires a Python build linked against OpenSSL 1.1+.

---

## Running a script

Filenames contain spaces, so quote them:

```bash
cd Symmetric_Encryption
python "4. AES (Advanced Encryption Standard).py"
```

Some scripts depend on others. `Asymmetric_Encryption/1 RSA Key Generation.py` writes `private_key.pem` and `public_key.pem` to the current directory, and scripts 3, 4 and 5 load them. Run the scripts in numeric order from the same folder.

---

## 1. Cryptography Basics

| Script | What it demonstrates |
|---|---|
| `1 Caesar's Shifty Cipher (Encryption).py` | Shift cipher encryption with modular arithmetic (`HELLO` + 3 → `KHOOR`) |
| `1 Caesar's Shifty Cipher (Decryption).py` | Reversing the shift |
| `2 Substitution Cipher Encryption.py` | Monoalphabetic substitution using a keyed alphabet |
| `2 Substitution Cipher Decryption.py` | Reversing the substitution |
| `3 Encrypting a Message with Fernet.py` | First taste of modern authenticated encryption |

The Caesar and substitution scripts take input interactively. They show why classical ciphers fall to brute force and frequency analysis.

## 2. Symmetric Encryption

One shared key encrypts and decrypts.

| # | Script | Concepts |
|---|---|---|
| 1 | Fernet Symmetric Encryption | Authenticated symmetric encryption (AES-128-CBC + HMAC) with key generation |
| 2 | Secret-Key Ciphers | Shared-secret model, sender and receiver flow |
| 3 | Types of Symmetric Ciphers | Stream ciphers (XOR keystream demo) vs block ciphers |
| 4 | AES | AES-256 with CBC through the `Cipher` API |
| 5 | ECB Mode | Deterministic encryption and why repeated blocks leak patterns |
| 6 | CBC Mode | IV-based chaining with PKCS7 padding |
| 7 | CTR Mode | Counter mode, which turns AES into a stream cipher (no padding) |
| 8 | Padding | PKCS7 and ANSI X.923 |
| 9 | Key & IV Management | Never reusing a key/IV pair, generating a fresh IV per message |
| 10 | Secure Key Generation | `random` (insecure) vs `os.urandom()` (CSPRNG) |
| 11 | Additional Symmetric Algorithms | Camellia, ChaCha20, TripleDES, CAST5, SEED |

`AES Image Encryption Web Project.docx` is a project brief for a Flask web app that encrypts images with AES in ECB, CBC and CTR modes, a classic way to visualize the weakness of ECB.

## 3. Asymmetric Encryption

Public and private key pairs, mostly RSA-2048 with exponent 65537.

| # | Script | Concepts |
|---|---|---|
| 1 | RSA Key Generation | Generating a key pair and writing PEM files |
| 2 | RSA Key Serialization | PEM encoding of public and private keys |
| 3 | RSA Key Loading | `load_pem_private_key` / `load_pem_public_key` |
| 4 | RSA Encryption | Encrypting with the public key using OAEP (SHA-256 + MGF1) |
| 5 | RSA Decryption | Decrypting with the private key |
| 5.1 | Combined RSA Encryption & Decryption | End-to-end round trip in one file |
| 6 | RSA Digital Signatures | Authenticity, integrity and non-repudiation |
| 7 | Integer–Byte Conversion in RSA | `int.from_bytes` / `to_bytes` and why RSA works on integers |
| 8 | Digital Certificate Demonstration | Self-signed X.509 certificate |
| 9 | RSA Padding Demonstration | OAEP randomness: the same plaintext gives different ciphertexts |
| 10 | Chosen Ciphertext Attack Simulation | Why padding and CCA resistance matter |
| 11 | Man-in-the-Middle (MITM) Attack Simulation | Public-key substitution by "Mallory" |
| 12 | Public Key Infrastructure (PKI) Demonstration | CA key, self-signed CA cert, server CSR, CA-signed certificate |

Scripts 10 and 11 are local simulations (Alice, Bob and Mallory exist only as variables in one process). Nothing touches the network.

## 4. Hashing

| Script | Concepts |
|---|---|
| `1_hashlib.py` | SHA-256 of a string |
| `2_HASH.py` | MD5, SHA-1, SHA-256 and SHA3-256 side by side |
| `3_Python hashlib Examples.py` | Algorithm discovery, file hashing and more `hashlib` usage |
| `4_Password Hashing Process.py` | Why passwords are hashed, plus the register and verify flow |
| `5_SHA256_WITH_SALT.py` | Random salts (and why plain salted SHA-256 is still not enough for passwords) |
| `6_ARGON2_HASHING.py` | Argon2id via `argon2-cffi`: self-contained hash string, verification |
| `7_SCRYPT_HASHING.py` | Memory-hard hashing with `hashlib.scrypt` (n=16384, r=8, p=1) |
| `8_PASSWORD_CRACKING.py` | Tiny brute-force demo showing why short or weak passwords fall quickly |

Accompanying `.docx` files cover salted hashing, Argon2, scrypt, and project briefs for Flask password-authentication systems using **bcrypt** and **PBKDF2**.

**Recommended for real password storage:** Argon2id, then scrypt or bcrypt. Plain SHA-256, even salted, is too fast and is shown for learning only.

### `password-auth-system/`

A Flask + MySQL authentication demo (also shipped as `password-auth-system.zip`):

- bcrypt hashing with per-password salts and a configurable cost factor
- Registration, login, logout and a session-protected dashboard
- Account lockout policy and session timeout
- CSRF protection (Flask-WTF) and Jinja2 auto-escaping
- Client-side validation and password-strength meter (server re-validates everything)
- Config via environment variables

Setup instructions are in [`Hashing/password-auth-system/project/README.md`](Hashing/password-auth-system/project/README.md). Dependencies: Flask, Flask-WTF, mysql-connector-python, bcrypt, python-dotenv, email-validator.

---

## Suggested learning path

1. `cryptography_basics`: understand why classical ciphers are weak
2. `Hashing` scripts 1–5: integrity and the idea of salting
3. `Symmetric_Encryption` 1–11: Fernet, then AES modes, padding and key and IV handling
4. `Asymmetric_Encryption` 1–7: RSA mechanics
5. `Asymmetric_Encryption` 8–12: certificates, attacks and PKI
6. `Hashing` 6–8 and the auth system: password storage done properly

---

## Security notes

- Never hard-code or commit keys, `.pem` private keys or `.env` files. The generated `private_key.pem` is written **unencrypted** (`NoEncryption()`) for demo purposes only.
- Use `os.urandom()` / `secrets`, never `random`, for key material.
- Never reuse a key/IV pair, and prefer authenticated encryption (Fernet, AES-GCM, ChaCha20-Poly1305) over bare CBC or CTR.
- Avoid MD5 and SHA-1 for anything security-relevant, and avoid ECB mode and unpadded RSA entirely.
- Run the attack simulations only on your own demo data.

---

## Contributing

Issues and pull requests are welcome, especially for new topics (AES-GCM, HMAC, ECDSA/ECDH, key exchange, JWT signing).

## License

Released under the [MIT License](../LICENSE).

---

Built by **CubicNova**.
