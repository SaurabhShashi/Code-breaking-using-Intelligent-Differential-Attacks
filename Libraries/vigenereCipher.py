
ALPHABETS_ENG = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'



def encryptMessage(key, message):
    return transformMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return transformMessage(key, message, 'decrypt')


def transformMessage(key, message, mode):
    UpdatedMsg = [] # Encrypted/decrypted message string is stored

    keyIndex = 0
    key = key.upper()

    for eachChar in message: # loops through each character in msg
        num = ALPHABETS_ENG.find(eachChar.upper())
        if num != -1: # -1 means character is not found
            if mode == 'encrypt':
                num += ALPHABETS_ENG.find(key[keyIndex]) # add if encrypting
            elif mode == 'decrypt':
                num -= ALPHABETS_ENG.find(key[keyIndex]) # subtract if decrypting

            num %= len(ALPHABETS_ENG) # handling potential wrap-arounds

            # Adds the encrypted/decrypted symbol to the end of UpdatedMsg.
            if eachChar.isupper():
                UpdatedMsg.append(ALPHABETS_ENG[num])
            elif eachChar.islower():
                UpdatedMsg.append(ALPHABETS_ENG[num].lower())

            keyIndex += 1 
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # When the symbol was not in ALPHABETS_ENG, adding it to UpdatedMsg as it is.
            UpdatedMsg.append(eachChar)

    return ''.join(UpdatedMsg)

