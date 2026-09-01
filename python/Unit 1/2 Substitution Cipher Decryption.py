plain_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cipher_alphabet = "QWERTYUIOPASDFGHJKLZXCVBNM"
cipher = input("Enter Cipher Text: ").upper()
plain = ""
for letter in cipher:
    if letter.isalpha():
        index = cipher_alphabet.index(letter)
        plain += plain_alphabet[index]
    else:
        plain += letter
print("Original Message:", plain)



# Output
# Enter Cipher Text: ITSSG
# Original Message: HELLO