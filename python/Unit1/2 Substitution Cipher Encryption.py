plain_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cipher_alphabet = "QWERTYUIOPASDFGHJKLZXCVBNM"
message = input("Enter Message: ").upper()
cipher = ""
for letter in message:
    if letter.isalpha():
        index = plain_alphabet.index(letter)
        cipher += cipher_alphabet[index]
    else:
        cipher += letter
print("Encrypted Message:", cipher)


# Output
# Enter Message: HELLO
# Encrypted Message: ITSSG