import hashlib
text = "Hello World"

print("MD5      :", hashlib.md5(text.encode()).hexdigest())
print("SHA-1    :", hashlib.sha1(text.encode()).hexdigest())
print("SHA-256  :", hashlib.sha256(text.encode()).hexdigest())
print("SHA3-256 :", hashlib.sha3_256(text.encode()).hexdigest())


# Sample Output

# MD5      : b10a8db164e0754105b7a99be72e3fe5
# SHA-1    : 0a4d55a8d778e5022fab701977c5d840bbc486d0
# SHA-256  : a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e
# SHA3-256 : e167f68d6563d75bb25f3aa49d3f7d8b...