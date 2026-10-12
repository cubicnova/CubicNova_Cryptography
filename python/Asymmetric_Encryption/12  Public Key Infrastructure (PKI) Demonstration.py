'''
===========================================================================
Public Key Infrastructure (PKI) Demonstration
To demonstrate the working of Public Key Infrastructure (PKI) and understand how Certificate Authorities (CA) establish trust in public key cryptography.

🧿Theory
Public Key Infrastructure (PKI) is a framework that manages digital certificates and public-key encryption. PKI ensures that a public key actually belongs to the claimed entity by using Digital Certificates issued by trusted Certificate Authorities (CA).
Without PKI, attackers could replace public keys and perform Man-in-the-Middle attacks. Digital certificates solve this problem by binding identities to public keys through a trusted third party.

🧿Components of PKI
    Certificate Authority (CA)
    Registration Authority (RA)
    Digital Certificates
    Public Keys
    Private Keys
    Certificate Repository
    
🧿Algorithm
    Generate a CA RSA key pair.
    Create a self-signed CA certificate.
    Generate a Server RSA key pair.
    Create a Certificate Signing Request (CSR).
    Sign the server certificate using the CA private key.
    Verify the server certificate issuer.
    Demonstrate the trust relationship between the CA and Server.
===========================================================================
'''
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

# --------------------------
# Step 1: Create CA
# --------------------------

ca_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

ca_public_key = ca_private_key.public_key()

ca_subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CubicNova CA"),
    x509.NameAttribute(NameOID.COMMON_NAME, "CubicNova Root CA"),
])

ca_certificate = (
    x509.CertificateBuilder()
    .subject_name(ca_subject)
    .issuer_name(ca_subject)
    .public_key(ca_public_key)
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=3650))
    .sign(ca_private_key, hashes.SHA256())
)

# --------------------------
# Step 2: Create Server Key
# --------------------------

server_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

server_public_key = server_private_key.public_key()

server_subject = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CubicNova"),
    x509.NameAttribute(NameOID.COMMON_NAME, "www.cubicnova.com"),
])

# --------------------------
# Step 3: CA signs Server Certificate
# --------------------------

server_certificate = (
    x509.CertificateBuilder()
    .subject_name(server_subject)
    .issuer_name(ca_subject)
    .public_key(server_public_key)
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=365))
    .sign(ca_private_key, hashes.SHA256())
)

print("Root CA Certificate Created")
print("Server Certificate Signed by CA")
print("PKI Trust Relationship Established")

'''
===========================================================================
Sample Output
    Root CA Certificate Created
    Server Certificate Signed by CA
    PKI Trust Relationship Established
===========================================================================
'''
'''
===========================================================================
Explanation
Step 1: Root Certificate Authority
Root CA
 ├── Private Key
 └── Public Certificate

The Root CA acts as the trusted authority in the PKI hierarchy.
===========================================================================
Step 2: Server Certificate Request
    Web Server
        │
        ▼
    Generates Key Pair
        │
        ▼
    Requests Certificate

The server creates a public/private key pair and requests a certificate.
===========================================================================
Step 3: Certificate Signing
    CA Private Key
            │
            ▼
    Signs Server Certificate
            │
            ▼
    Trusted Certificate

The CA digitally signs the server certificate, establishing trust.
===========================================================================
🧿Working Diagram
                Root CA
                   │
                   │ Signs
                   ▼
        Server Digital Certificate
                   │
                   ▼
           www.cubicnova.com
                   │
                   ▼
            Trusted by Client
===========================================================================
PKI Hierarchy
Root CA
   │
   ├── Intermediate CA
   │        │
   │        ▼
   │   Server Certificate
   │
   ▼
Trusted Clients
===========================================================================
🧿Applications
    HTTPS Websites
    SSL/TLS Security
    Secure Email (S/MIME)
    VPN Authentication
    Digital Signatures
    Banking Applications
    Government Portals
    Cloud Services
===========================================================================
🧿Advantages of PKI
    Establishes Trust
    Prevents MITM Attacks
    Provides Authentication
    Supports Digital Signatures
    Enables Secure Communication
===========================================================================
'''
