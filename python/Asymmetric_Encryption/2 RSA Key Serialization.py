'''
2: RSA Key Serialization
To serialize RSA Public and Private Keys into PEM format using Python and understand the process of storing cryptographic keys securely.

🧿Theory
Serialization is the process of converting RSA keys into a byte format that can be stored in files, transmitted over a network, or saved in databases.
RSA keys are commonly serialized using the PEM (Privacy Enhanced Mail) format, which is a Base64-encoded representation of cryptographic keys. The cryptography library provides methods to serialize both public and private keys

🧿Algorithm
    Generate an RSA private key.
    Extract the corresponding public key.
    Serialize the private key into PEM format.
    Serialize the public key into PEM format.
    Save both keys into separate files.
    Display the PEM headers.
'''
#======================================================================

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate RSA Private Key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Generate Public Key
public_key = private_key.public_key()

# Serialize Private Key
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Serialize Public Key
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save Keys
with open("private_key.pem", "wb") as file:
    file.write(private_key_bytes)

with open("public_key.pem", "wb") as file:
    file.write(public_key_bytes)

print(private_key_bytes.splitlines()[0])
print(public_key_bytes.splitlines()[0])

#======================================================================
'''
Sample Output
    b'-----BEGIN RSA PRIVATE KEY-----'
    b'-----BEGIN PUBLIC KEY-----'

Generated Files:
    private_key.pem
    public_key.pem

'''
#======================================================================
'''
Explanation
🧿Private Key Serialization
    private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

Converts the private key into PEM format without password protection.

🧿Public Key Serialization
    public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

Converts the public key into PEM format.

🧿PEM Format
PEM is a standard format used to store and exchange cryptographic keys and certificates. It contains Base64 encoded data enclosed within:
'''

