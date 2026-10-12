# Python Example: Scrypt Password Hashing
import hashlib
import os

# User password
password = b"Admin@123"

# Generate a random 16-byte salt
salt = os.urandom(16)

# Generate Scrypt hash
password_hash = hashlib.scrypt(
    password=password,
    salt=salt,
    n=16384,      # CPU/Memory cost (must be power of 2)
    r=8,          # Block size
    p=1,          # Parallelization
    dklen=32      # Output length in bytes
)

print("Salt :", salt.hex())
print("Hash :", password_hash.hex())
# Sample Output
# Salt :
# 7bc91f8b6c4d2a58d98e7f4c3b1a4d9f

# Hash :
# 58d36fd8f6d7e11d73e5af8cb1dbf4d8b9dba98f56a8d1e7fd88d8b2a32d5b16


# ====================================================================================

# Password Verification
# During login, regenerate the hash using the stored salt and compare it with the stored hash.
import hashlib

entered_password = b"Admin@123"

verify_hash = hashlib.scrypt(
    password=entered_password,
    salt=salt,
    n=16384,
    r=8,
    p=1,
    dklen=32
)

if verify_hash == password_hash:
    print("Password Verified ✓")
else:
    print("Invalid Password ✗")
# Output
# Password Verified ✓
