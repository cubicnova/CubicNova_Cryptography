'''
=========================================================================================
4. AES (Advanced Encryption Standard)
AES (Advanced Encryption Standard) is a modern symmetric-key block cipher used to securely encrypt and decrypt data. It is one of the most widely adopted encryption algorithms and is used in many Internet protocols and operating system services, including TLS (HTTPS), IPSec, and file-level or full-disk encryption.
=========================================================================================
AES supports several modes of operation, including:
1.ECB (Electronic Codebook)
2.CBC (Cipher Block Chaining)
3.CTR (Counter Mode)
=========================================================================================
'''

# Python Example: AES Encryption using CBC Mode

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Generate a 256-bit AES key
key = os.urandom(32)

# Generate a 128-bit Initialization Vector (IV)
iv = os.urandom(16)

# Create AES Cipher in CBC mode
cipher = Cipher(
    algorithms.AES(key),
    modes.CBC(iv),
    backend=default_backend()
)

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
# Ciphertext: 8f3c9d2b5a7e...
# Decrypted : b'SecretMessage123'


"""
=========================================================================================
How AES Works
Step 1: Generate a Secret Key
    AES uses a shared secret key for encryption and decryption.
    key = os.urandom(32)  # 256-bit key

Step 2: Generate an Initialization Vector (IV)
    CBC mode requires a random IV to ensure identical messages produce different ciphertexts.
    iv = os.urandom(16)

Step 3: Encrypt Plaintext
    AES transforms readable plaintext into unreadable ciphertext.
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

Step 4: Decrypt Ciphertext
    Using the same key and IV, the ciphertext is converted back into the original plaintext.
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
=========================================================================================
"""
"""
=========================================================================================
AES Modes of Operation
Mode Description
    ECB	Encrypts each block independently. Not recommended because identical plaintext blocks produce identical ciphertext blocks.
    CBC	Uses an IV and XOR operations to hide patterns between blocks.
    CTR	Generates a keystream using a counter and XORs it with plaintext. Padding is not required.

==>Advantages of AES
    Strong and widely trusted encryption standard.
    Fast and efficient for large volumes of data.
    Used globally in web security, VPNs, disk encryption, and secure communications.
    Supports multiple secure modes of operation.
==>Real-World Applications
    HTTPS/TLS secure websites
    IPSec VPNs
    BitLocker disk encryption
    Cloud storage encryption
    Secure file transfer systems
=========================================================================================

"""