'''
===========================================================================
🧿RSA Decryption
To decrypt an RSA-encrypted message using the RSA Private Key and recover the original plaintext.

🧿Theory
RSA Decryption is the process of converting ciphertext back into plaintext using the Private Key. In RSA cryptography, a message encrypted using the public key can only be decrypted using the corresponding private key.
This property ensures confidentiality because even if the ciphertext is intercepted, it cannot be read without the private key.

🧿Algorithm
    Load the RSA Private Key from a PEM file.
    Read the encrypted ciphertext.
    Use the private key to decrypt the ciphertext.
    Convert the decrypted bytes into readable text.
    Display the original plaintext.
===========================================================================
'''

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load Private Key
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# Example ciphertext (replace with actual encrypted data)
ciphertext = b'YOUR_ENCRYPTED_MESSAGE'

# Decrypt Message
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Decrypted Message:")
print(plaintext.decode())

