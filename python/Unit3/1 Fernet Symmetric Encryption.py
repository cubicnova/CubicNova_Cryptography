#Symmetric encryption uses a single secret key for both encryption and decryption. Both the sender and receiver must possess the same key to securely exchange information. It is widely used because it is fast, efficient, and suitable for encrypting large amounts of data.

from cryptography.fernet import Fernet

# Generate a secret key
key = Fernet.generate_key()

# Create Fernet object
cipher = Fernet(key)

# Original message
message = b"Hello CubicNova"

# Encrypt the message
encrypted = cipher.encrypt(message)

# Decrypt the message
decrypted = cipher.decrypt(encrypted)

print("Original :", message.decode())
print("Encrypted:", encrypted.decode())
print("Decrypted:", decrypted.decode())


# Sample Output
# Original : Hello CubicNova
# Encrypted: gAAAAABo...
# Decrypted: Hello CubicNova

'''
=========================================================================================
How It Works
A secret key is generated.
The same key encrypts the plaintext.
The encrypted ciphertext is transmitted or stored.
The same key decrypts the ciphertext back into the original message.
=========================================================================================
'''