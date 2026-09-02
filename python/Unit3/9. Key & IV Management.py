"""
=========================================================================================
9. Key & IV Management
Proper Key and Initialization Vector (IV) management is critical for secure symmetric encryption. A secret key should remain confidential, and the same Key-IV pair must never be reused. Reusing a Key-IV pair can expose patterns in encrypted data and significantly weaken the security of the encryption scheme.
=========================================================================================

Why Key & IV Management Matters
In modes such as CBC and CTR, the IV introduces randomness into the encryption process.
If the same Key-IV pair is reused:
    Identical plaintexts can generate related ciphertexts.
    Attackers may discover patterns in encrypted messages.
    Sensitive information may be leaked.
=========================================================================================
"""

# Python Example: Secure Key & IV Generation

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Generate a random AES-256 key
key = os.urandom(32)

# Generate a unique IV for each encryption
iv = os.urandom(16)

# Create AES CBC cipher
cipher = Cipher(
    algorithms.AES(key),
    modes.CBC(iv)
)

print("AES Key:", key.hex())
print("IV:", iv.hex())

# Sample Output
# AES Key: 8a4d2f6b7c9e1a...
# IV: 3f7c9a1d5b2e4f...

"""
Incorrect Practice: Reusing Key-IV Pair
    # Same key reused
    key = b"12345678901234567890123456789012"

    # Same IV reused
    iv = b"1234567890123456"
Using the same key and IV repeatedly for multiple messages is insecure because attackers can analyze relationships between ciphertexts.
"""
# Correct Practice: New IV for Every Encryption

import os

key = os.urandom(32)   # Secret key

# Generate a fresh IV every time
iv1 = os.urandom(16)
iv2 = os.urandom(16)

print(iv1 == iv2)

# Sample Output
# False

"""
Each encryption operation uses a different IV, ensuring that even identical plaintext messages produce different ciphertexts.

Example Scenario
Suppose two users encrypt the same message:

Message: "Transfer ₹10,000"
Reusing Same Key-IV Pair
    Ciphertext 1 = A1B2C3D4...
    Ciphertext 2 = A1B2C3D4...
Patterns become visible.

Using Different IVs
    Ciphertext 1 = A1B2C3D4...
    Ciphertext 2 = X9Y8Z7W6...

Even though the plaintext is identical, the ciphertext differs because each encryption uses a unique IV.

Best Practices
    Generate cryptographically secure keys.
    Generate a new IV for every encryption operation.
    Never reuse the same Key-IV combination.
    Store keys securely.
    IVs may be transmitted with the ciphertext, but keys must remain secret.
Advantages of Proper Key & IV Management
    Prevents ciphertext pattern leakage.
    Improves confidentiality.
    Protects against replay and cryptanalysis attacks.
    Strengthens AES-CBC and AES-CTR security.
"""