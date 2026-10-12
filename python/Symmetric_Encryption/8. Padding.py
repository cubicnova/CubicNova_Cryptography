"""
=========================================================================================
8. Padding
Padding is a technique used in block cipher encryption when the plaintext size is not an exact multiple of the cipher's block size. Since AES operates on 16-byte blocks, extra bytes must be added to the plaintext before encryption. After decryption, these padding bytes are removed to recover the original message.
The presentation covers two common padding schemes:
    PKCS7 Padding
    ANSI X.923 Padding
    
=========================================================================================
Why Padding is Needed
AES requires data lengths that are multiples of 16 bytes.

Example:
    HELLO
Length = 5 bytes
    AES Block Size = 16 bytes
Additional bytes must be added before encryption.
=========================================================================================
=========================================================================================
A. PKCS7 Padding

PKCS7 adds padding bytes where each padding byte contains the number of bytes added.
Example
Original Message:
    HELLO
Length = 5 bytes
Padding Required:
    16 - 5 = 11 bytes
Padded Message:
    HELLO\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B\x0B
Here, 0B (11 in hexadecimal) is repeated 11 times because 11 bytes were added.
=========================================================================================
"""
# Python Example: PKCS7 Padding
from cryptography.hazmat.primitives import padding

message = b"HELLO"

# Create PKCS7 padder
padder = padding.PKCS7(128).padder()

# Add padding
padded_data = padder.update(message) + padder.finalize()

print("Original:", message)
print("Padded  :", padded_data)

# Sample Output
# Original: b'HELLO'
# Padded  : b'HELLO\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b'

"""
=========================================================================================
B. ANSI X.923 Padding

ANSI X.923 fills padding bytes with zeros and stores the padding length in the final byte.
Example
Original Message:
    HELLO
Length = 5 bytes
    Padding Required = 11 bytes
Padded Message:
    HELLO\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0B
The last byte (0B) indicates that 11 padding bytes were added.
=========================================================================================
"""
# Python Example: ANSI X.923 Padding

from cryptography.hazmat.primitives import padding

message = b"HELLO"

# Create ANSI X.923 padder
padder = padding.ANSIX923(128).padder()

# Add padding
padded_data = padder.update(message) + padder.finalize()

print("Original:", message)
print("Padded  :", padded_data)

# Sample Output
# Original: b'HELLO'
# Padded  : b'HELLO\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b'


"""
=========================================================================================
PKCS7 vs ANSI X.923
Feature	PKCS7	ANSI X.923

| Feature                           | PKCS7                            | ANSI X.923                     |
| --------------------------------- | -------------------------------- | ------------------------------ |
| Padding Bytes                     | All bytes contain padding length | Zeros with length in last byte |
| Example                           | `0B 0B 0B 0B...`                 | `00 00 00 0B`                  |
| Common Usage                      | Very common                      | Less common                    |
| Supported by Cryptography Library | Yes                              | Yes                            |

=========================================================================================
Advantages of Padding
    Ensures plaintext fits the required block size.
    Enables AES and other block ciphers to encrypt messages of any length.
    Standardized and widely supported.
Limitations
    Adds extra bytes to the message.
    Incorrect padding handling can cause decryption errors.
    Not required in stream cipher modes such as CTR.
=========================================================================================
"""