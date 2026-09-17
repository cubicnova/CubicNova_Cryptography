'''To generate RSA Public and Private Keys using Python and understand the concept of asymmetric cryptography.'''
'''
Theory
RSA (Rivest-Shamir-Adleman) is one of the most widely known asymmetric encryption algorithms. It uses two keys:
    🧿Public Key  – Used for encryption and can be shared publicly.
    🧿Private Key – Used for decryption and must be kept secret.
    
Algorithm
    🧿Import required cryptography libraries.
    🧿Generate RSA private key using:
        public exponent = 65537
        key size = 2048 bits
    🧿Extract the public key from the private key.
    🧿Serialize both keys into PEM format.
    🧿Save keys into files.
    🧿Display generated keys.
'''
#======================================================================

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate Private Key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Generate Public Key
public_key = private_key.public_key()

# Serialize Private Key
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Serialize Public Key
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save Keys
with open("private_key.pem", "wb") as f:
    f.write(private_pem)

with open("public_key.pem", "wb") as f:
    f.write(public_pem)

print("RSA Keys Generated Successfully!")

#======================================================================

'''Sample Output
RSA Keys Generated Successfully!

🧿Generated Files:
    private_key.pem
    public_key.pem

🧿Explanation
    rsa.generate_private_key() generates a new RSA private key.
    public_exponent=65537 is the recommended value.
    key_size=2048 provides strong security.
    public_key() derives the public key from the private key.
    PEM format is used to store keys in a standard format.
'''
#======================================================================
