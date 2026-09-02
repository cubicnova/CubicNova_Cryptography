'''Secret-key ciphers are a form of symmetric encryption where both the sender and receiver use the same secret key for encryption and decryption. The key must remain confidential and be shared only between trusted parties. If an unauthorized person obtains the key, they can both decrypt existing messages and create fraudulent encrypted messages'''
from cryptography.fernet import Fernet

# Shared secret key (normally exchanged securely)
key = Fernet.generate_key()

# Both sender and receiver use the same key
cipher = Fernet(key)

# Sender encrypts the message
message = b"Transfer Rs. 50,000 to Account XYZ"
encrypted_message = cipher.encrypt(message)

print("Encrypted Message:")
print(encrypted_message.decode())

# Receiver decrypts using the same key
decrypted_message = cipher.decrypt(encrypted_message)

print("\nDecrypted Message:")
print(decrypted_message.decode())

'''Encrypted Message:
gAAAAABoXYZabc123...

Decrypted Message:
Transfer Rs. 50,000 to Account XYZ'''


'''
=========================================================================================
How It Works
Step 1: Generate a Secret Key
A secret key is created and securely shared between the sender and receiver.
key = Fernet.generate_key()

Step 2: Encrypt the Message
The sender uses the shared key to convert plaintext into ciphertext.
encrypted_message = cipher.encrypt(message)

Step 3: Send Ciphertext
The encrypted message can now be transmitted over an insecure network.

Step 4: Decrypt the Message
The receiver uses the same secret key to recover the original plaintext.
decrypted_message = cipher.decrypt(encrypted_message)


=========================================================================================
Security Concern

Suppose Alice and Bob share a secret key:

Secret Key: ABC123XYZ
Alice encrypts messages using this key.
Bob decrypts messages using the same key.

If an attacker steals the key:
✅ They can read all encrypted messages.
✅ They can create fake encrypted messages pretending to be Alice.
=========================================================================================

'''