import hashlib
import string
import itertools

target_hash = hashlib.sha256("ab".encode()).hexdigest()

characters = string.ascii_lowercase

for length in range(1, 3):
    for guess in itertools.product(characters, repeat=length):
        password = ''.join(guess)

        if hashlib.sha256(password.encode()).hexdigest() == target_hash:
            print("Password Found:", password)
            break

# Output
# Password Found: ab
# This example demonstrates how a computer systematically tests possible passwords until it finds the correct one.