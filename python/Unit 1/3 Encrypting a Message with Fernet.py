# Install the library:
# pip install cryptography


from cryptography.fernet import Fernet
# Generate a secret key
key = Fernet.generate_key()
cipher = Fernet(key)
message = b"Hello Cryptography"
encrypted = cipher.encrypt(message)
decrypted = cipher.decrypt(encrypted)

print("Original :", message.decode())
print("Encrypted:", encrypted.decode())
print("Decrypted:", decrypted.decode())

# Sample Output
# Original : Hello Cryptography
# Encrypted: gAAAAAB...
# Decrypted: Hello Cryptography