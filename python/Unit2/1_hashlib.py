import hashlib
message = "Hello World"
hash_value = hashlib.sha256(message.encode())
print(hash_value.hexdigest())

# Output (SHA-256):
# a591a6d40bf420404a011733cfb7b190
# d62c65bf0bcda32b57b277d9ad9f146e