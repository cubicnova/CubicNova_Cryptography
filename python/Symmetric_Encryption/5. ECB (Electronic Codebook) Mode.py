"""
=========================================================================================
5. ECB (Electronic Codebook) Mode
ECB (Electronic Codebook) is the simplest mode of operation for AES. In this mode, each plaintext block is encrypted independently using the same key. If the same plaintext block appears multiple times, it will always produce the same ciphertext block.
Because ECB is deterministic, attackers can identify repeating patterns in encrypted data, making it unsuitable for most real-world applications
=========================================================================================
"""

# Python Example: AES ECB Mode

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Generate 128-bit AES key
key = os.urandom(16)

# Create AES Cipher in ECB mode
cipher = Cipher(
    algorithms.AES(key),
    modes.ECB(),
    backend=default_backend()
)

encryptor = cipher.encryptor()
decryptor = cipher.decryptor()

# Plaintext must be exactly 16 bytes
plaintext = b"HELLOAESMODE1234"

# Encrypt
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Decrypt
decrypted = decryptor.update(ciphertext) + decryptor.finalize()

print("Plaintext :", plaintext)
print("Ciphertext:", ciphertext.hex())
print("Decrypted :", decrypted)

# Sample Output
# Plaintext : b'HELLOAESMODE1234'
# Ciphertext: 8a7c2d9f4e1b...
# Decrypted : b'HELLOAESMODE1234'

"""
=========================================================================================
How ECB Works
Step 1: Divide Plaintext into Blocks
AES processes data in fixed-size blocks (16 bytes).
    Block 1: HELLOAESMODE1234
    Block 2: HELLOAESMODE1234

Step 2: Encrypt Each Block Independently
Each block is encrypted using the same secret key.
    Ciphertext Block 1 = AES(Key, Block 1)
    Ciphertext Block 2 = AES(Key, Block 2)

Step 3: Identical Blocks Produce Identical Ciphertext
    Plaintext Block 1 = HELLOAESMODE1234
    Plaintext Block 2 = HELLOAESMODE1234

    Ciphertext Block 1 = A1B2C3D4...
    Ciphertext Block 2 = A1B2C3D4...

Since the plaintext blocks are identical, the ciphertext blocks are also identical.
=========================================================================================
"""

"""
=========================================================================================
Why ECB is Insecure

ECB does not hide data patterns.
If a file contains repeated data:
    AAAA AAAA AAAA AAAA
    AAAA AAAA AAAA AAAA

the encrypted output will also contain repeating ciphertext blocks.

Attackers can analyze these repeating patterns and make educated guesses about the original content. This is why ECB mode is generally not recommended for sensitive information.
Advantages
    >Simple to understand.
    >Easy to implement.
    >Fast encryption and decryption.
Disadvantages
    >Reveals data patterns.
    >Identical plaintext blocks create identical ciphertext blocks.
    >Vulnerable to pattern analysis attacks.
    >Not recommended for secure applications.
Real-World Recommendation
Instead of ECB, modern applications typically use:
    >CBC (Cipher Block Chaining) mode to eliminate repeating patterns.
    >CTR (Counter Mode) for higher security and performance.
=========================================================================================

"""