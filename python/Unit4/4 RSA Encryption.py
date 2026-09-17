'''
===========================================================================
🧿RSA Encyption
To encrypt a plaintext message using an RSA Public Key and understand the process of asymmetric encryption.

🧿Theory
RSA Encryption is an asymmetric cryptographic algorithm that uses a Public Key for encryption and a Private Key for decryption.
Anyone possessing the public key can encrypt a message, but only the owner of the corresponding private key can decrypt and read the message. This ensures confidentiality during communication.

🧿Algorithm
    Load the RSA public key from a PEM file.
    Take plaintext input from the user.
    Convert plaintext into bytes.
    Encrypt the message using the RSA public key.
    Display the encrypted ciphertext.
===========================================================================

'''

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Load Public Key
with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read()
    )

# Message to Encrypt
message = b"Hello Cryptography Students"

# Encrypt Message
ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Encrypted Message:")
print(ciphertext)

'''
Sample Output
    Encrypted Message:
    b'\x8f\x92\xab\x1d\xa7\x11\xf0\xca...'

(Ciphertext will be different every time because OAEP padding introduces randomness.)
'''
'''
===========================================================================
Explanation
🧿Load Public Key
    public_key = serialization.load_pem_public_key(
        key_file.read()
    )
    
Loads the RSA public key from a PEM file.

===========================================================================
🧿Encryption
    ciphertext = public_key.encrypt(...)

Encrypts the plaintext using the public key.
===========================================================================
🧿OAEP Padding
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
OAEP (Optimal Asymmetric Encryption Padding) provides security against deterministic output and chosen ciphertext attacks. The PPT emphasizes that RSA without padding is insecure and should never be used.
===========================================================================
'''