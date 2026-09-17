'''
===========================================================================
Chosen Ciphertext Attack Simulation
To demonstrate the concept of a Chosen Ciphertext Attack (CCA) on RSA and understand why secure padding schemes such as OAEP are necessary.

🧿Theory
A Chosen Ciphertext Attack (CCA) is a cryptographic attack in which an attacker can choose arbitrary ciphertexts and obtain their decrypted plaintexts. By analyzing the responses, the attacker may gain information about the secret key or other encrypted messages.
The presentation discusses chosen ciphertext attacks as one of the reasons why RSA must be used with secure padding mechanisms and why improper RSA implementations can be dangerous.

🧿Attack Scenario
Consider:
    Alice owns an RSA Private Key.
    Bob encrypts a message using Alice's Public Key.
    An attacker intercepts the ciphertext.
    The attacker modifies the ciphertext and tricks Alice into decrypting it.
    Information from the decryption result may reveal details about the original message.

This demonstrates why modern systems use secure padding schemes such as OAEP
===========================================================================
🧿Algorithm
    Generate RSA keys.
    Encrypt a message.
    Simulate an attacker intercepting the ciphertext.
    Modify the ciphertext.
    Attempt decryption of the modified ciphertext.
    Observe the behavior of the system.
    Understand how padding protects against such attacks.
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

message = b"Secret Message"

# Encrypt Message
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Original Ciphertext Generated")

# Attacker modifies ciphertext
modified_ciphertext = bytearray(ciphertext)
modified_ciphertext[10] ^= 1

try:
    decrypted = private_key.decrypt(
        bytes(modified_ciphertext),
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print("Decrypted:", decrypted)

except Exception:
    print("Decryption Failed - Tampering Detected")
    
'''
Sample Output
    Original Ciphertext Generated
    Decryption Failed - Tampering Detected
'''
'''
===========================================================================
Working Diagram

    Bob
    │
    │ Encrypt using Public Key
    ▼
    Ciphertext
    │
    │ Intercepted
    ▼
    Attacker
    │
    │ Modifies Ciphertext
    ▼
    Tampered Ciphertext
    │
    ▼
    Alice
    │
    │ Attempts Decryption
    ▼
    Error / Rejection
===========================================================================
Security Lessons
    RSA should never be used without secure padding.
    OAEP provides protection against several attack classes.
    Modified ciphertexts should fail validation.
    Cryptographic libraries should always be preferred over custom implementations.
    Decryption errors must be handled carefully to avoid leaking information.
===========================================================================
'''
