'''
===========================================================================
🧿Digital Certificate Demonstration
To demonstrate the concept of Digital Certificates and understand how certificates bind a public key to the identity of its owner.

🧿Theory
A Digital Certificate is an electronic document used to verify the identity of a user, website, organization, or device. It binds a Public Key to the identity of its owner through a trusted Certificate Authority (CA).
Knowledge of a public key alone does not guarantee the identity of its owner. Digital certificates solve this problem by providing a trusted association between the public key and the owner.

🧿Components of a Digital Certificate
    Certificate Owner Name
    Public Key
    Certificate Serial Number
    Validity Period
    Issuing Certificate Authority (CA)
    Digital Signature of CA
    
🧿Algorithm
    Generate RSA Public and Private Keys.
    Create certificate subject information.
    Create certificate issuer information.
    Generate a self-signed certificate.
    Save the certificate in PEM format.
    Display certificate details.
===========================================================================
'''
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta

# Generate RSA Key Pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = private_key.public_key()

# Subject and Issuer Information
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Madhya Pradesh"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Indore"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CubicNova"),
    x509.NameAttribute(NameOID.COMMON_NAME, "www.cubicnova.com"),
])

# Create Certificate
certificate = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(public_key)
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.utcnow())
    .not_valid_after(datetime.utcnow() + timedelta(days=365))
    .sign(private_key, hashes.SHA256())
)

# Save Certificate
with open("certificate.pem", "wb") as f:
    f.write(certificate.public_bytes(serialization.Encoding.PEM))

print("Digital Certificate Generated Successfully")


'''
Sample Output
    Digital Certificate Generated Successfully

Generated File:
    certificate.pem
'''
'''
===========================================================================
Explanation
🧿Subject
The subject identifies the certificate owner.
    subject = x509.Name([...])

Example:
    Country      : IN
    State        : Madhya Pradesh
    Organization : CubicNova
    Common Name  : www.cubicnova.com
===========================================================================
🧿Issuer
The issuer identifies who issued the certificate.
For a self-signed certificate:
    issuer = subject
===========================================================================
🧿Certificate Signing
    .sign(private_key, hashes.SHA256())

The certificate is digitally signed using the issuer's private key.
===========================================================================
'''
