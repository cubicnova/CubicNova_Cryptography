"""
=========================================================================================
6. CBC (Cipher Block Chaining) Mode

CBC (Cipher Block Chaining) is a secure AES mode that uses an Initialization Vector (IV) and XOR (Exclusive OR) operations to prevent identical plaintext blocks from producing identical ciphertext blocks. Each plaintext block is XORed with the previous ciphertext block before encryption, making every block dependent on all preceding blocks.
Unlike ECB mode, CBC hides repetitive patterns in data, making it much more secure for real-world applications.
=========================================================================================
"""

# Python Example: AES CBC Mode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Generate 256-bit AES key
key = os.urandom(32)

# Generate 128-bit Initialization Vector (IV)
iv = os.urandom(16)

# Create AES Cipher in CBC mode
cipher = Cipher(
    algorithms.AES(key),
    modes.CBC(iv),
    backend=default_backend()
)

encryptor = cipher.encryptor()
decryptor = cipher.decryptor()

# Message
plaintext = b"Hello CBC Encryption"

# Add PKCS7 padding
padder = padding.PKCS7(128).padder()
padded_data = padder.update(plaintext) + padder.finalize()

# Encrypt
ciphertext = encryptor.update(padded_data) + encryptor.finalize()

# Decrypt
decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

# Remove padding
unpadder = padding.PKCS7(128).unpadder()
decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

print("Original :", plaintext.decode())
print("Encrypted:", ciphertext.hex())
print("Decrypted:", decrypted.decode())

# Sample Output
# Original : Hello CBC Encryption
# Encrypted: a1b2c3d4e5f6...
# Decrypted: Hello CBC Encryption

"""
=========================================================================================
How CBC Works
Step 1: Generate Key and IV
    CBC requires:
        AES Secret Key
        Initialization Vector (IV)
        key = os.urandom(32)
        iv = os.urandom(16)
Step 2: XOR Plaintext with Previous Ciphertext
For the first block:
    Ciphertext₁ = AES(Key, Plaintext₁ ⊕ IV)
For subsequent blocks:
    Ciphertext₂ = AES(Key, Plaintext₂ ⊕ Ciphertext₁)
    Ciphertext₃ = AES(Key, Plaintext₃ ⊕ Ciphertext₂)

Each block depends on the previous encrypted block.
=========================================================================================

CBC Encryption Flow

Plaintext Block 1
        │
        ▼
      XOR IV
        │
        ▼
   AES Encryption
        │
        ▼
 Ciphertext Block 1
        │
        ▼
Plaintext Block 2
        │
        ▼
 XOR Ciphertext Block 1
        │
        ▼
   AES Encryption
        │
        ▼
 Ciphertext Block 2
 
=========================================================================================
Why CBC is More Secure than ECB
Consider two identical plaintext blocks:
    HELLO1234567890
    HELLO1234567890
ECB Mode
    Cipher Block 1 = ABC123
    Cipher Block 2 = ABC123
Patterns remain visible.

CBC Mode
    Cipher Block 1 = ABC123
    Cipher Block 2 = XYZ789
Even though the plaintext blocks are identical, the ciphertext blocks are different because of chaining and the IV.
=========================================================================================

Padding Requirement
CBC operates on fixed-size AES blocks.
If the message length is not a multiple of 16 bytes, padding must be added. PKCS7 is the recommended padding scheme.

Example:
    HELLO
After PKCS7 Padding:
    HELLO\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B

=========================================================================================

Advantages
    Hides repeated patterns in plaintext.
    More secure than ECB mode.
    Widely used in secure systems and applications.
Disadvantages
    Encryption is sequential and cannot be easily parallelized.
    Requires padding.
    Requires secure IV management.
=========================================================================================
"""