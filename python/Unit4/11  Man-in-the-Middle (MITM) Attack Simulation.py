'''
===========================================================================
Man-in-the-Middle (MITM) Attack Simulation
To demonstrate a Man-in-the-Middle (MITM) Attack in Public Key Cryptography and understand how Digital Certificates help prevent such attacks.

🧿Theory
A Man-in-the-Middle (MITM) Attack occurs when an attacker secretly intercepts communication between two parties and impersonates each party to the other.
In Public Key Cryptography, the attack typically happens during public key exchange. If Alice receives an attacker's public key instead of Bob's public key, Alice may unknowingly encrypt messages that only the attacker can read.
The presentation discusses MITM attacks as a public key substitution attack and explains why Digital Certificates and Certificate Authorities (CA) are required.

🧿Algorithm
    Generate RSA keys for Alice.
    Generate RSA keys for Bob.
    Generate RSA keys for Mallory (Attacker).
    Bob sends his public key to Alice.
    Mallory intercepts the key exchange.
    Mallory sends her public key pretending to be Bob.
    Alice encrypts a message using Mallory's public key.
    Mallory decrypts the message and reads it.
    Demonstrate how the attack compromises confidentiality.
===========================================================================
'''
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Alice Keys
alice_private = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Bob Keys
bob_private = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

bob_public = bob_private.public_key()

# Mallory (Attacker) Keys
mallory_private = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

mallory_public = mallory_private.public_key()

# Mallory replaces Bob's public key
fake_bob_public = mallory_public

message = b"Transfer 10000 INR"

# Alice encrypts message believing key belongs to Bob
ciphertext = fake_bob_public.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Mallory decrypts intercepted message
stolen_message = mallory_private.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Message intercepted by attacker:")
print(stolen_message.decode())

'''
===========================================================================
Sample Output
    Message intercepted by attacker:
    Transfer 10000 INR
===========================================================================
'''
'''
===========================================================================
Explanation
🧿Normal Communication
    Alice
    │
    │ Bob's Public Key
    ▼
    Encrypt Message
    │
    ▼
    Bob

Only Bob can decrypt the message.
===========================================================================
🧿MITM Attack
    Alice
    │
    │ Receives Fake Public Key
    ▼
    Mallory
    │
    │ Reads Message
    ▼
    Bob

Mallory substitutes Bob's public key with her own public key. Alice unknowingly encrypts messages for Mallory instead of Bob.
===========================================================================
🧿How Digital Certificates Prevent MITM
Digital Certificates verify that a public key actually belongs to the claimed owner.

    Certificate Authority
            │
            ▼
    Signs Bob's Certificate
            │
            ▼
    Alice Verifies Certificate
            │
            ▼
    Trusts Bob's Public Key

Without a valid certificate, Alice cannot be certain that the public key belongs to Bob.
===========================================================================

🧿Applications of MITM Awareness
    HTTPS Security
    SSL/TLS Certificate Validation
    VPN Security
    Secure Email Communication
    Banking Applications
    Public Key Infrastructure (PKI)
===========================================================================
'''
