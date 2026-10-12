"""
=========================================================================================
7. CTR (Counter) Mode
CTR (Counter) Mode is a mode of operation that transforms AES from a block cipher into a stream cipher. Instead of directly encrypting plaintext blocks, AES encrypts a counter value to generate a keystream, which is then XORed with the plaintext to produce ciphertext.
Unlike CBC mode, CTR mode does not require padding and is generally recommended because it is simpler, more efficient, and easier to parallelize.
=========================================================================================
"""

# Python Example: AES CTR Mode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Generate 256-bit AES key
key = os.urandom(32)

# Generate nonce/counter value
nonce = os.urandom(16)

# Create AES Cipher in CTR mode
cipher = Cipher(
    algorithms.AES(key),
    modes.CTR(nonce),
    backend=default_backend()
)

encryptor = cipher.encryptor()
decryptor = cipher.decryptor()

# Plaintext
plaintext = b"Hello CTR Mode Encryption"

# Encrypt
ciphertext = encryptor.update(plaintext) + encryptor.finalize()

# Decrypt
decrypted = decryptor.update(ciphertext) + decryptor.finalize()

print("Original :", plaintext.decode())
print("Encrypted:", ciphertext.hex())
print("Decrypted:", decrypted.decode())

# Sample Output
# Original : Hello CTR Mode Encryption
# Encrypted: 8f4c7d91ab56e2...
# Decrypted: Hello CTR Mode Encryption

"""
=========================================================================================
How CTR Mode Works
Step 1: Generate a Secret Key
AES uses a shared secret key.
    key = os.urandom(32)
    
Step 2: Generate a Nonce (Counter)
CTR mode starts with a random counter (nonce).
    nonce = os.urandom(16)
    
Step 3: Generate Keystream
AES encrypts the counter value instead of the plaintext.
    Counter 1 → AES(Key, Counter1) → Keystream Block 1
    Counter 2 → AES(Key, Counter2) → Keystream Block 2
    Counter 3 → AES(Key, Counter3) → Keystream Block 3
    
Step 4: XOR with Plaintext
The generated keystream is XORed with the plaintext to produce ciphertext.
    Ciphertext = Plaintext ⊕ Keystream
    
Step 5: Decryption
The same keystream is generated and XORed again with the ciphertext.
    Plaintext = Ciphertext ⊕ Keystream

Because XOR is its own inverse, the original message is recovered.

=========================================================================================
CTR Encryption Flow
Counter Value
      │
      ▼
 AES Encryption
      │
      ▼
   Keystream
      │
      ▼
 Plaintext XOR Keystream
      │
      ▼
  Ciphertext
=========================================================================================
For decryption:

Ciphertext XOR Keystream
           │
           ▼
       Plaintext
       
=========================================================================================
Why CTR Mode is Preferred

No Padding Required
    Unlike CBC mode, CTR operates like a stream cipher and can encrypt any number of bytes directly.
Parallel Processing
    Each keystream block is generated independently from its counter value, making CTR easy to parallelize.
Better Performance
    CTR mode is often faster and simpler than CBC mode while maintaining strong security when used correctly.

=========================================================================================
Advantages
    No padding required.
    Fast encryption and decryption.
    Supports parallel processing.
    Suitable for large files and network communications.
    Converts AES into a stream cipher.

Disadvantages
    Reusing the same key and nonce/counter is extremely dangerous.
    Requires careful key and nonce management.
=========================================================================================
"""