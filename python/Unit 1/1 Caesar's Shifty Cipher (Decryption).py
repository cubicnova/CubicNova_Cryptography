alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cipher = input("Enter Cipher Text: ").upper()
shift = int(input("Enter Shift Value: "))
plain = ""
for letter in cipher:
    if letter.isalpha():
        index = alphabet.find(letter)
        new_index = (index - shift) % 26
        plain += alphabet[new_index]
    else:
        plain += letter
print("Original Message:", plain)

# OUTPUT
# Enter Cipher Text: KHOOR
# Enter Shift Value: 3
# Original Message: HELLO