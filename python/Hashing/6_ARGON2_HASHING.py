# Python Example: Password Hashing Using Argon2 (Recommended)
# Why Argon2?
# Argon2 is the modern standard for password hashing because it:
# •	Automatically generates a unique random salt for every password.
# •	Is resistant to brute-force and GPU attacks.
# •	Is memory-hard, making large-scale password cracking much more difficult.
# •	Is recommended by OWASP and many cybersecurity professionals.

# Step 1: Install the Library
# pip install argon2-cffi
# ________________________________________
# Step 2: Import the Required Module
from argon2 import PasswordHasher
# ________________________________________
# Step 3: Create a Password Hasher
from argon2 import PasswordHasher

ph = PasswordHasher()
# ________________________________________
# Step 4: Hash the Password
password = "Admin@123"

hashed_password = ph.hash(password)

print("Original Password :", password)
print("Hashed Password   :", hashed_password)
# Sample Output
# Original Password : Admin@123

# Hashed Password :
# $argon2id$v=19$m=65536,t=3,p=4$
# N4LwTnVvU0hFbGxYQ2k0bQ$
# nDgWq2wJxM2n8k8jO0sXgH4y6m3yR2M6...
# The generated hash already contains: - Algorithm (Argon2id) - Version - Memory cost - Time cost - Parallelism - Random Salt - Password Hash
# ________________________________________

# Step 5: Verify the Password
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

password = "Admin@123"

stored_hash = ph.hash(password)

try:
    ph.verify(stored_hash, "Admin@123")
    print("Password Verified ✓")
except VerifyMismatchError:
    print("Invalid Password ✗")
# Output
# Password Verified ✓

# ________________________________________
# Step 6: Incorrect Password Example
try:
    ph.verify(stored_hash, "WrongPassword")
    print("Password Verified")
except VerifyMismatchError:
    print("Invalid Password")
# Output
# Invalid Password