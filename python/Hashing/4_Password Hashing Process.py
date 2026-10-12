"""
Password Hashing Process in Python
Password hashing is used to securely store passwords. Instead of storing the actual password, a hash value is stored in the database. During login, the entered password is hashed again and compared with the stored hash.
Why Hash Passwords?
    Passwords are never stored in plain text.
    Even if the database is compromised, original passwords are difficult to recover.
    Hashing provides data integrity and security.
"""
#============================================================================================
# Example 1: SHA-256 Password Hashing
import hashlib

# User password
password = input("Enter Password: ")

# Convert password to bytes and hash it
hashed_password = hashlib.sha256(password.encode()).hexdigest()

print("\nOriginal Password:", password)
print("SHA-256 Hash:", hashed_password)

# Sample Output
# Enter Password: CubicNova@123

# Original Password: CubicNova@123
# SHA-256 Hash:
# 7f6a8d7f5f0e7c2b9c4a5d8e1f2a3b4c...

#============================================================================================
# Example 2: Password Verification
import hashlib

# Registration
password = "CubicNova@123"
stored_hash = hashlib.sha256(password.encode()).hexdigest()

# Login
login_password = input("Enter Password: ")

login_hash = hashlib.sha256(login_password.encode()).hexdigest()

if login_hash == stored_hash:
    print("Login Successful")
else:
    print("Invalid Password")

#============================================================================================

# Example 3: Secure Password Hashing with Salt
#A salt is a random value added to the password before hashing to prevent rainbow table attacks.
import hashlib
import os

password = "CubicNova@123"

# Generate random salt
salt = os.urandom(16)

# Hash password + salt
hashed_password = hashlib.sha256(
    salt + password.encode()
).hexdigest()

print("Salt:", salt.hex())
print("Hash:", hashed_password)


#============================================================================================
# Example 4: Recommended Method Using bcrypt
# Install bcrypt:
# pip install bcrypt
# Hash Password
import bcrypt

password = b"CubicNova@123"

# Generate Salt
salt = bcrypt.gensalt()

# Hash Password
hashed_password = bcrypt.hashpw(password, salt)

print("Hashed Password:")
print(hashed_password.decode())

#============================================================================================
# Verify Password
import bcrypt

stored_hash = b"$2b$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

password = input("Enter Password: ").encode()

if bcrypt.checkpw(password, stored_hash):
    print("Password Matched")
else:
    print("Invalid Password")
    
#============================================================================================