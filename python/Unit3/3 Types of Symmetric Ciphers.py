'''
=========================================================================================
3. Types of Symmetric Ciphers
Symmetric encryption algorithms are commonly classified into two categories: Stream Ciphers and Block Ciphers. Stream ciphers encrypt data one byte (or bit) at a time, whereas block ciphers encrypt data in fixed-size blocks
=========================================================================================
'''
'''
=========================================================================================
A. Stream Cipher
A Stream Cipher encrypts data continuously, processing one byte at a time. It generates a keystream and combines it with the plaintext to produce ciphertext. RC4 is a common example mentioned in the presentation.
========================================================================================='''

# Python Example (Simple XOR Stream Cipher)

import os

# Generate a random key stream
key = os.urandom(5)

plaintext = b"HELLO"

# Encryption
ciphertext = bytes([p ^ k for p, k in zip(plaintext, key)])

# Decryption
decrypted = bytes([c ^ k for c, k in zip(ciphertext, key)])

print("Plaintext :", plaintext)
print("Ciphertext:", ciphertext)
print("Decrypted :", decrypted)

# Plaintext : b'HELLO'
# Ciphertext: b'\x1f\x87\xab...'
# Decrypted : b'HELLO'

'''
=========================================================================================
B. Block Cipher
A Block Cipher encrypts data in fixed-size blocks. AES, DES, and Triple DES (3DES) are common examples. AES operates on 16-byte blocks, while DES and 3DES operate on 8-byte blocks
=========================================================================================
'''
# Python Example (AES Block Cipher)

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Generate AES key (256-bit)
key = os.urandom(32)

# Generate IV (128-bit)
iv = os.urandom(16)

# Create AES Cipher in CBC mode
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

encryptor = cipher.encryptor()
decryptor = cipher.decryptor()

# Plaintext must be 16 bytes
plaintext = b"SecretMessage123"

# Encrypt
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Decrypt
decrypted = decryptor.update(ciphertext) + decryptor.finalize()

print("Plaintext :", plaintext)
print("Ciphertext:", ciphertext.hex())
print("Decrypted :", decrypted)

# Sample Output
# Plaintext : b'SecretMessage123'
# Ciphertext: a5b7c8d9...
# Decrypted : b'SecretMessage123'

'''
=========================================================================================
How It Works
1.Data is divided into fixed-size blocks.
2.Each block is encrypted using the secret key.
3.The receiver uses the same key to decrypt the blocks.
4.Modes such as ECB, CBC, and CTR determine how blocks are processed.
=========================================================================================
'''