'''
===========================================================================
🧿RSA Digital Signatures
To implement RSA Digital Signatures using Python for message authentication, integrity verification, and non-repudiation.

🧿Theory
A Digital Signature is a cryptographic technique used to verify:
    Authenticity    – Confirms the sender's identity.
    Integrity       – Ensures the message has not been modified.
    Non-Repudiation – Prevents the sender from denying the message.

In RSA Digital Signatures:
    The sender signs the message using the Private Key.
    The receiver verifies the signature using the Public Key.

Unlike RSA Encryption, Digital Signatures do not provide confidentiality; instead, they provide trust and verification.

🧿Algorithm
    Generate RSA Public and Private Keys.
    Create a message to be signed.
    Generate a digital signature using the Private Key.
    Send the message and signature.
    Verify the signature using the Public Key.
    Display the verification result.
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

# Message
message = b"Welcome to Cryptography Lab"

# Sign Message using Private Key
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

print("Digital Signature Generated")

# Verify Signature using Public Key
try:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("Signature Verified Successfully")
except:
    print("Invalid Signature")
    
'''
Sample Output
    Digital Signature Generated
    Signature Verified Successfully
'''

'''
===========================================================================
🧿Explanation
Signing Process
    signature = private_key.sign(...)
The sender uses the RSA Private Key to create a digital signature for the message.

===========================================================================
🧿Verification Process
    public_key.verify(...)
The receiver uses the RSA Public Key to verify that:

    The message has not been modified.
    The sender possesses the corresponding Private Key.
This proves the authenticity of the sender.
===========================================================================
🧿Applications
    Software Code Signing
    SSL/TLS Certificates
    Secure Email (PGP/S-MIME)
    Electronic Documents
    Blockchain Transactions
    Digital Contracts
    Online Banking Systems
🧿Advantages
    Ensures Message Integrity
    Provides Authentication
    Supports Non-Repudiation
    Prevents Message Tampering
'''

