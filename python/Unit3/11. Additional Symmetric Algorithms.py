"""
11. Additional Symmetric Algorithms
In addition to AES, several other symmetric encryption algorithms are available for securing data. The presentation lists Camellia, ChaCha20, TripleDES, CAST5, and SEED as examples of symmetric algorithms.

A. Camellia
Camellia is a symmetric block cipher designed to provide security comparable to AES. It supports 128-bit block sizes and multiple key lengths.

Features
    Symmetric block cipher.
    Supports 128, 192, and 256-bit keys.
    Used in government and enterprise security systems.
"""

# Python Example: Camellia Encryption

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

key = os.urandom(32)      # 256-bit key
iv = os.urandom(16)

cipher = Cipher(
    algorithms.Camellia(key),
    modes.CBC(iv)
)

print("Camellia Cipher Created Successfully")


"""
B. ChaCha20
ChaCha20 is a modern symmetric stream cipher designed for high performance and strong security. It is widely used in modern protocols and mobile devices
Features
    Stream cipher.
    Fast on software-only systems.
    No padding required.
    Commonly used in TLS and VPNs.
"""
# Python Example: ChaCha20 Encryption

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
import os

key = os.urandom(32)
nonce = os.urandom(16)

algorithm = algorithms.ChaCha20(key, nonce)
cipher = Cipher(algorithm, mode=None)

encryptor = cipher.encryptor()

plaintext = b"Hello ChaCha20"
ciphertext = encryptor.update(plaintext)

print("Ciphertext:", ciphertext.hex())

"""
C. TripleDES (3DES)
TripleDES (3DES) improves DES security by applying the DES algorithm three times with different keys.
Features
    Based on DES.
    More secure than DES.
    Slower than AES.
    Being phased out in modern applications.
"""
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

key = os.urandom(24)      # 192-bit key
iv = os.urandom(8)

cipher = Cipher(
    algorithms.TripleDES(key),
    modes.CBC(iv)
)

print("TripleDES Cipher Created Successfully")

"""
D. CAST5
CAST5 is a symmetric block cipher that supports variable key sizes and has historically been used in applications such as PGP.
Features
    Symmetric block cipher.
    Variable key lengths.
    Used in some legacy encryption systems.
"""
# Python Example: CAST5
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

key = os.urandom(16)
iv = os.urandom(8)

cipher = Cipher(
    algorithms.CAST5(key),
    modes.CBC(iv)
)

print("CAST5 Cipher Created Successfully")

"""
E. SEED
SEED is a symmetric block cipher developed for secure communications and is widely adopted in certain regional standards.
Features
    128-bit block cipher.
    Uses a 128-bit key.
    Adopted in several security standards.
"""
# Python Example: SEED
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

key = os.urandom(16)
iv = os.urandom(16)

cipher = Cipher(
    algorithms.SEED(key),
    modes.CBC(iv)
)

print("SEED Cipher Created Successfully")

"""
Comparison of Additional Symmetric Algorithms

| Algorithm | Type          | Block Size | Key Size            |
| --------- | ------------- | ---------- | ------------------- |
| Camellia  | Block Cipher  | 128-bit    | 128/192/256-bit     |
| ChaCha20  | Stream Cipher | N/A        | 256-bit             |
| TripleDES | Block Cipher  | 64-bit     | 168-bit (effective) |
| CAST5     | Block Cipher  | 64-bit     | 40–128-bit          |
| SEED      | Block Cipher  | 128-bit    | 128-bit             |

"""

