'''
RSA KEY LOADING
To load previously serialized RSA Public and Private Keys from PEM files and use them in cryptographic operations.

🧿Theory
    After RSA keys are generated and stored in PEM format, they can be loaded back into Python objects whenever required. The cryptography library provides methods to deserialize PEM-encoded keys and reconstruct the original RSA key objects.
    Loading keys is essential in real-world applications because keys are usually stored on disk and loaded only when needed.

🧿Algorithm
    Read the private key from the PEM file.
    Load the private key using load_pem_private_key().
    Read the public key from the PEM file.
    Load the public key using load_pem_public_key().
    Display a success message after loading both keys.
'''
#======================================================================

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Load Private Key
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# Load Public Key
with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

print("Private Key Loaded Successfully")
print("Public Key Loaded Successfully")

#======================================================================
'''
Sample Output
    Private Key Loaded Successfully
    Public Key Loaded Successfully
'''

'''
Explanation
===========================================================================
🧿Loading Private Key
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
        backend=default_backend()
    )
    
Reads a PEM-formatted private key.
Since the key is not encrypted, password=None is used.
Returns an RSA Private Key object.
===========================================================================
🧿Loading Public Key
    public_key = serialization.load_pem_public_key(
        public_key_bytes,
        backend=default_backend()
    )
Reads a PEM-formatted public key.
Returns an RSA Public Key object.
===========================================================================
Key Concepts

🧿PEM Format
PEM (Privacy Enhanced Mail) is a standard encoding format used to store cryptographic keys and certificates.

Example:

-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----

-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----

===========================================================================

Why Load Keys?
    Reuse generated keys.
    Secure communication.
    Digital signatures.
    Authentication systems.
    SSL/TLS implementations.
'''
