# 1. Import the hashlib Module
import hashlib

# ---------------------------------------------------------------------------------------
# 2. View Available Hash Algorithms
# This displays all hashing algorithms supported by your Python installation.

import hashlib
print(hashlib.algorithms_available)

# Sample Output
# {'md5', 'sha1', 'sha224', 'sha256', 'sha384',
#  'sha512', 'sha3_224', 'sha3_256',
#  'sha3_384', 'sha3_512', 'blake2b', 'blake2s'}

# ---------------------------------------------------------------------------------------
# 3. Algorithms Guaranteed on All Platforms

import hashlib
print(hashlib.algorithms_guaranteed)

# ---------------------------------------------------------------------------------------
# 4. Generate an MD5 Hash
import hashlib

message = "Hello World"
hash_value = hashlib.md5(message.encode())
print(hash_value.hexdigest())

# Output
# b10a8db164e0754105b7a99be72e3fe5

# ---------------------------------------------------------------------------------------
# 5. Generate a SHA-1 Hash
import hashlib

message = "Hello World"
hash_value = hashlib.sha1(message.encode())
print(hash_value.hexdigest())

# Output
# 0a4d55a8d778e5022fab701977c5d840bbc486d0


# ---------------------------------------------------------------------------------------
# 6. Generate a SHA-256 Hash

import hashlib

message = "Hello World"
hash_value = hashlib.sha256(message.encode())
print(hash_value.hexdigest())

# Output
# a591a6d40bf420404a011733cfb7b190
# d62c65bf0bcda32b57b277d9ad9f146e


# ---------------------------------------------------------------------------------------
# 7. Generate a SHA-512 Hash
import hashlib

message = "Hello World"
hash_value = hashlib.sha512(message.encode())
print(hash_value.hexdigest())


# ---------------------------------------------------------------------------------------
# 8. Generate a SHA3-256 Hash
import hashlib

message = "Hello World"
hash_value = hashlib.sha3_256(message.encode())
print(hash_value.hexdigest())


# ---------------------------------------------------------------------------------------
# 9. Generate Multiple Hashes at Once

import hashlib

text = "Cyber Security"

print("MD5      :", hashlib.md5(text.encode()).hexdigest())
print("SHA1     :", hashlib.sha1(text.encode()).hexdigest())
print("SHA256   :", hashlib.sha256(text.encode()).hexdigest())
print("SHA512   :", hashlib.sha512(text.encode()).hexdigest())
print("SHA3-256 :", hashlib.sha3_256(text.encode()).hexdigest())


# ---------------------------------------------------------------------------------------
# 10. Using update() Method
# Useful when hashing large data or receiving data in chunks.

import hashlib

h = hashlib.sha256()

h.update(b"Hello ")
h.update(b"World")

print(h.hexdigest())


# ---------------------------------------------------------------------------------------
# 11. digest() vs hexdigest()
import hashlib

message = "Python"
hash_obj = hashlib.sha256(message.encode())
print(hash_obj.digest())
print(hash_obj.hexdigest())

# Output
# b'...binary bytes...'
# 18885f27b5af9012df19...

# Method	         Output
# digest()	         Binary bytes
# hexdigest()	     Human-readable hexadecimal string

# ---------------------------------------------------------------------------------------
# 12. Hash a File (Integrity Check)
import hashlib

with open("example.pdf", "rb") as file:
    file_hash = hashlib.sha256()
    while chunk := file.read(4096):
        file_hash.update(chunk)

print(file_hash.hexdigest())

# Use Cases

# Verify downloaded files
# Malware analysis
# Digital forensics
# Backup verification


# ---------------------------------------------------------------------------------------

# 13. Compare Two Files

import hashlib

def sha256_hash(filename):
    h = hashlib.sha256()

    with open(filename, "rb") as file:
        while chunk := file.read(4096):
            h.update(chunk)

    return h.hexdigest()

file1 = sha256_hash("file1.txt")
file2 = sha256_hash("file2.txt")

if file1 == file2:
    print("Files are identical")
else:
    print("Files are different")
    
    
    
# ---------------------------------------------------------------------------------------
# 14. Hash a Password (Demonstration Only)
# Note: This example is for learning purposes only. In production, use bcrypt, scrypt, or Argon2 for password storage.
import hashlib

password = "Admin@123"
hashed_password = hashlib.sha256(password.encode()).hexdigest()
print(hashed_password)


# ---------------------------------------------------------------------------------------
# 15. Creating a Hash Using hashlib.new()

import hashlib

text = "Cryptography"
hash_value = hashlib.new("sha256", text.encode())
print(hash_value.hexdigest())


# ---------------------------------------------------------------------------------------
# 16. Verify File Integrity

import hashlib

expected_hash = "a591a6d40bf420404a011733cfb7b190..."

with open("example.txt", "rb") as file:
    actual_hash = hashlib.sha256(file.read()).hexdigest()

if actual_hash == expected_hash:
    print("File integrity verified")
else:
    print("File has been modified")
    
    
# ---------------------------------------------------------------------------------------
