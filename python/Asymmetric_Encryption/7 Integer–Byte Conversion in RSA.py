'''
===========================================================================
Integer–Byte Conversion in RSA
To convert data between integers and bytes in Python and understand why this conversion is required in RSA cryptography.

🧿Theory
RSA mathematically operates on integers, whereas computer systems typically store and transmit data as bytes. Therefore, before encryption, a message must be converted from bytes to an integer. After decryption, the resulting integer must be converted back into bytes to recover the original message.
Python provides built-in methods:
    int.to_bytes() → Integer to Bytes
    int.from_bytes() → Bytes to Integer
These methods make conversion simple and efficient.

🧿Algorithm
    Take a text message.
    Convert the message into bytes.
    Convert bytes into an integer.
    Display the integer representation.
    Convert the integer back into bytes.
    Decode bytes into the original message.
    Verify that the original message is recovered successfully.
===========================================================================
'''
# Original Message
message = "Cryptography Lab"

# Convert String to Bytes
message_bytes = message.encode()

# Convert Bytes to Integer
message_int = int.from_bytes(message_bytes, byteorder="big")

print("Integer Representation:")
print(message_int)

# Convert Integer back to Bytes
recovered_bytes = message_int.to_bytes(
    (message_int.bit_length() + 7) // 8,
    byteorder="big"
)

# Convert Bytes back to String
recovered_message = recovered_bytes.decode()

print("\nRecovered Message:")
print(recovered_message)

'''
Sample Output
    Integer Representation:
    2291093969893568116589296640780360178290

Recovered Message:
Cryptography Lab
'''

'''
===========================================================================
Explanation
🧿Bytes to Integer
    message_int = int.from_bytes(
        message_bytes,
        byteorder="big"
    )

Converts a sequence of bytes into a single integer.
===========================================================================
🧿Integer to Bytes
    integer.to_bytes(
        (integer.bit_length()+7)//8,
        byteorder="big"
    )

Converts an integer back into bytes. The expression (bit_length()+7)//8 calculates the minimum number of bytes required to store the integer.
===========================================================================
🧿Byte Order
Python supports:
    Big Endian ("big") – Most significant byte first
    Little Endian ("little") – Least significant byte first
'''


