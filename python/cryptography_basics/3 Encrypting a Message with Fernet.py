# Install the library:
# pip install cryptography


from cryptography.fernet import Fernet
# Generate a secret key
key = Fernet.generate_key()
print("key value: ",key)
cipher = Fernet(key)
message = b"Hello Saksham"
encrypted = cipher.encrypt(message)
decrypted = cipher.decrypt(encrypted)

print("Original :", message.decode())
print("Encrypted:", encrypted.decode())
print("Decrypted:", decrypted.decode())

# Sample Output
# Original : Hello Cryptography
# Encrypted: gAAAAAB...
# Decrypted: Hello Cryptography