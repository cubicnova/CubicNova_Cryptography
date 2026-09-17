'''
===========================================================================
RSA Padding Demonstration
To demonstrate the importance of padding in RSA encryption and understand why RSA without padding is insecure.

🧿Theory
RSA encryption should never be used without padding. Padding adds randomness to the plaintext before encryption, making the ciphertext unpredictable and secure against various cryptographic attacks.
The presentation explicitly states that implementing RSA without padding is a serious mistake and that modern cryptographic libraries do not allow insecure RSA encryption without proper padding.

🧿Why Padding is Required?
Without padding:
    RSA becomes deterministic.
    Same plaintext always produces the same ciphertext.
    Attackers can build lookup tables of encrypted messages.
    Vulnerable to chosen ciphertext attacks.

With padding:
    Randomness is added before encryption.
    Same message encrypts to different ciphertexts each time.
    Stronger security against cryptanalytic attacks.
    
Algorithm
    Generate RSA Public and Private Keys.
    Create a plaintext message.
    Encrypt the message using OAEP padding.
    Encrypt the same message again.
    Compare both ciphertexts.
    Observe that the ciphertexts differ despite having the same plaintext.
    Decrypt the ciphertext and recover the original message.
===========================================================================
'''
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Generate RSA Keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()

message = b"Welcome to Cryptography Lab"

# First Encryption
ciphertext1 = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Second Encryption
ciphertext2 = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Ciphertext 1:")
print(ciphertext1)

print("\nCiphertext 2:")
print(ciphertext2)

print("\nAre ciphertexts equal?")
print(ciphertext1 == ciphertext2)

# Decrypt
plaintext = private_key.decrypt(
    ciphertext1,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("\nRecovered Message:")
print(plaintext.decode())


'''
Sample Output
Ciphertext 1:
b'\x93\x1f\xa2...'

Ciphertext 2:
b'\x8d\x44\xf1...'

Are ciphertexts equal?
False
Recovered Message:
Welcome to Cryptography Lab
'''
'''
===========================================================================
Explanation
🧿OAEP Padding
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )

OAEP (Optimal Asymmetric Encryption Padding) is the recommended padding scheme for RSA encryption.
===========================================================================
🧿Security Benefit
Even when the same message is encrypted multiple times:
    Message → Encrypt → Ciphertext A
    Message → Encrypt → Ciphertext B

The ciphertexts are different because OAEP introduces randomness.

This prevents deterministic outputs, which are a known weakness of raw RSA.
===========================================================================
🧿Deterministic Output Problem
Without padding:
    HELLO → RSA → ABC123
    HELLO → RSA → ABC123
    HELLO → RSA → ABC123

An attacker can recognize repeated messages and build lookup tables.
===========================================================================
With OAEP:
    HELLO → RSA+OAEP → XYZ111
    HELLO → RSA+OAEP → MNO222
    HELLO → RSA+OAEP → PQR333

Each encryption produces a unique ciphertext.
===========================================================================
'''
