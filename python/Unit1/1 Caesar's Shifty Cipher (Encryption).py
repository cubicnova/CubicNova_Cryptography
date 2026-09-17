alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
message = input("Enter Message: ").upper()
shift = int(input("Enter Shift Value: "))
cipher = ""
for letter in message:
    if letter.isalpha():
        index = alphabet.find(letter)
        new_index = (index + shift) % 26
        cipher += alphabet[new_index]
    else:
        cipher += letter
print("Encrypted Message:", cipher)

# OUTPUT
# Enter Message: HELLO
# Enter Shift Value: 3
# Encrypted Message: KHOOR