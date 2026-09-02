"""
10. Secure Key Generation
The security of any encryption system depends heavily on the quality of its cryptographic keys. Keys must be generated using a cryptographically secure random number generator (CSPRNG). The presentation recommends avoiding Python's standard random module for cryptographic purposes and instead using os.urandom() or secrets.SystemRandom() for secure key generation.
Why random Should Not Be Used
The Python random module is designed for simulations and general-purpose randomness, not security. Its outputs can be predictable if an attacker discovers the seed value.
"""

# Insecure Example
import random

# NOT suitable for cryptographic keys
key = random.randint(100000, 999999)

print("Generated Key:", key)


"""
Problems
    Predictable output.
    Not cryptographically secure.
    Vulnerable to brute-force and prediction attacks.
"""

# Secure Method 1: Using os.urandom()
# os.urandom() generates cryptographically secure random bytes directly from the operating system.
# Example: Generate AES-256 Key

import os

# Generate 256-bit (32-byte) AES key
key = os.urandom(32)

print("AES Key:", key.hex())


# Sample Output
#     AES Key:
#     8f3c7a91b5d4e2f18c9a7b6d5e4f3a2c...

"""   
| Algorithm | Key Size |
| --------- | -------- |
| AES-128   | 16 bytes |
| AES-192   | 24 bytes |
| AES-256   | 32 bytes |

"""
# Secure Method 2: Using secrets.SystemRandom()
# The secrets module is specifically designed for generating cryptographically secure values.

import secrets
import string

alphabet = string.ascii_letters + string.digits

# Generate a secure 16-character key
key = ''.join(secrets.choice(alphabet) for _ in range(16))

print("Secure Key:", key)

# Sample Output
# Secure Key:
# K8xP2mQ7nW4zR1sT

# Example: Generate AES Key and IV Securely

import os

# AES-256 Key
key = os.urandom(32)

# AES IV
iv = os.urandom(16)

print("Key:", key.hex())
print("IV :", iv.hex())

# Sample Output
# Key: a8c1f2d3e4b5...
# IV : 9f8e7d6c5b4a...


"""
Comparison
| Method                   | Cryptographically Secure | Recommended |
| ------------------------ | ------------------------ | ----------- |
| `random.randint()`       | ❌ No                     | ❌ No        |
| `random.choice()`        | ❌ No                     | ❌ No        |
| `os.urandom()`           | ✅ Yes                    | ✅ Yes       |
| `secrets.SystemRandom()` | ✅ Yes                    | ✅ Yes       |
| `secrets.choice()`       | ✅ Yes                    | ✅ Yes       |

Best Practices
    Use os.urandom() for encryption keys and IVs.
    Use the secrets module for passwords, tokens, and authentication secrets.
    Never generate cryptographic keys using the random module.
    Generate a new random IV for every encryption operation.
"""
