# Python Example: Password Hashing with Salt
# The following example demonstrates how to generate a random salt, combine it with a password, and create a secure SHA-256 hash.
# Note: This example is for learning purposes. In production systems, use dedicated password hashing algorithms such as bcrypt, scrypt, or Argon2.
# Step 1: Import Required Modules
import os
import hashlib
# ________________________________________
# Step 2: User Password
password = "Admin@123"
# ________________________________________
# Step 3: Generate a Random Salt
salt = os.urandom(16)   # Generates a 16-byte (128-bit) random salt
# ________________________________________
# Step 4: Combine Password and Salt
salted_password = salt + password.encode()
# ________________________________________
# Step 5: Generate SHA-256 Hash
hash_value = hashlib.sha256(salted_password).hexdigest()

# ________________________________________
# Step 6: Display the Results
print("Password :", password)
print("Salt     :", salt.hex())
print("Hash     :", hash_value)
# Sample Output
# Password : Admin@123

# Salt :
# d4b8f9a3e1c24b56f8d27c4a91ab7d35

# Hash :
# d6e74cb6f7a14a5d70cb2fd3b1b1e66c8bde4a8b26b38d84d77dbba5b2f66d4f

# ________________________________________
# Complete Program
import os
import hashlib

# User password
password = "Admin@123"

# Generate random salt
salt = os.urandom(16)

# Create salted password
salted_password = salt + password.encode()

# Generate SHA-256 hash
password_hash = hashlib.sha256(salted_password).hexdigest()

# Display results
print("Original Password :", password)
print("Salt (Hex)        :", salt.hex())
print("SHA-256 Hash      :", password_hash)

# ________________________________________
# Password Verification Example
# During login, retrieve the stored salt and hash the entered password again.
import hashlib

entered_password = "Admin@123"

# Recreate hash using stored salt
verify_hash = hashlib.sha256(
    salt + entered_password.encode()
).hexdigest()

if verify_hash == password_hash:
    print("Password Verified ✓")
else:
    print("Invalid Password ✗")
# ________________________________________
