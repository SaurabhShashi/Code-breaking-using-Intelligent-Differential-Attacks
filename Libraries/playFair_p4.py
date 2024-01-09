''' 
i' and 'j' aren't treated as one letter. It simply removes 'j' during the key matrix generation. To make the code consistent with the rules(as per william stallings: CRYPTOGRAPHY AND NETWORK SECURITY), replacing 'j' with 'i' in the plain text and cipher text before performing encryption and decryption.
'''
import string

class PlayfairCipher:
    def __init__(self):
        self._plain_text = ''
        self._cipher_text = ''
        self._key = ''
        self._key_matrix = ''

    def _generate_key_matrix(self):
        # Create the key matrix using the given key
        alphabet = string.ascii_lowercase.replace('j', '.')
        self._key = self._key.lower()
        self._key_matrix = ['' for i in range(5)]
        row = 0
        col = 0

        # Add key characters to the key matrix
        for char in self._key:
            if char in alphabet:
                self._key_matrix[row] += char
                alphabet = alphabet.replace(char, '.')
                col += 1
                if col > 4:
                    row += 1
                    col = 0

        # Add remaining alphabet characters to the key matrix
        for char in alphabet:
            if char != '.':
                self._key_matrix[row] += char
                col += 1
                if col > 4:
                    row += 1
                    col = 0

    def encrypt(self, plain_text, key):
        # Encrypt the plain text using the Playfair cipher
        self._plain_text = plain_text
        self._key = key
        self._cipher_text = ''
        plain_text_pairs = []
        cipher_text_pairs = []

        # Generate the key matrix
        self._generate_key_matrix()
        
        # Remove spaces and convert text to lowercase
        text = self._plain_text.replace(" ", "").lower()
        index = 0

        # Create plain text pairs
        while index < len(text):
            first_char = text[index]
            if (index + 1) == len(text):
                second_char = 'x'
            else:
                second_char = text[index + 1]

            if first_char != second_char:
                plain_text_pairs.append(first_char + second_char)
                index += 2
            else:
                plain_text_pairs.append(first_char + 'x')
                index += 1

        # Encrypt plain text pairs
        for pair in plain_text_pairs:
            same_row = False
            
            # Check if characters are in the same row
            for row in self._key_matrix:
                if pair[0] in row and pair[1] in row:
                    first_char_col = row.find(pair[0])
                    second_char_col = row.find(pair[1])
                    cipher_text_pair = row[(first_char_col + 1) % 5] + row[(second_char_col + 1) % 5]
                    cipher_text_pairs.append(cipher_text_pair)
                    same_row = True
            if same_row:
                continue

            same_col = False
            # Check if characters are in the same column
            for col_index in range(5):
                column = "".join([self._key_matrix[row_index][col_index] for row_index in range(5)])
                if pair[0] in column and pair[1] in column:
                    first_char_row = column.find(pair[0])
                    second_char_row = column.find(pair[1])
                    cipher_text_pair = column[(first_char_row + 1) % 5] + column[(second_char_row + 1) % 5]
                    cipher_text_pairs.append(cipher_text_pair)
                    same_col = True
            if same_col:
                continue

            # Characters are in different rows and columns
            first_char_row = 0
            first_char_col = 0
            # Characters are in different rows and columns
            first_char_row = 0
            first_char_col = 0
            second_char_row = 0
            second_char_col = 0
            
            # Find the row and column of each character in the pair
            for row_index in range(5):
                row = self._key_matrix[row_index]
                if pair[0] in row:
                    first_char_row = row_index
                    first_char_col = row.find(pair[0])
                if pair[1] in row:
                    second_char_row = row_index
                    second_char_col = row.find(pair[1])

            # Swap the columns of the characters to form a cipher text pair
            cipher_text_pair = self._key_matrix[first_char_row][second_char_col] + self._key_matrix[second_char_row][first_char_col]
            cipher_text_pairs.append(cipher_text_pair)

        return "".join(cipher_text_pairs)

    def decrypt(self, cipher_text, key):
        # Decrypt the cipher text using the Playfair cipher
        self._cipher_text = cipher_text.lower()
        self._key = key
        self._plain_text = ''
        plain_text_pairs = []
        cipher_text_pairs = []

        # Generate the key matrix
        self._generate_key_matrix()

        # Create cipher text pairs
        index = 0
        while index < len(self._cipher_text):
            first_char = self._cipher_text[index]
            second_char = self._cipher_text[index + 1]
            cipher_text_pairs.append(first_char + second_char)
            index += 2

        # Decrypt cipher text pairs
        for pair in cipher_text_pairs:
            same_row = False

            # Check if characters are in the same row
            for row in self._key_matrix:
                if pair[0] in row and pair[1] in row:
                    first_char_col = row.find(pair[0])
                    second_char_col = row.find(pair[1])
                    plain_text_pair = row[(first_char_col - 1) % 5] + row[(second_char_col - 1) % 5]
                    plain_text_pairs.append(plain_text_pair)
                    same_row = True
            if same_row:
                continue

            same_col = False
            # Check if characters are in the same column
            for col_index in range(5):
                column = "".join([self._key_matrix[row_index][col_index] for row_index in range(5)])
                if pair[0] in column and pair[1] in column:
                    first_char_row = column.find(pair[0])
                    second_char_row = column.find(pair[1])
                    plain_text_pair = column[(first_char_row - 1) % 5] + column[(second_char_row - 1) % 5]
                    plain_text_pairs.append(plain_text_pair)
                    same_col = True
            if same_col:
                continue

            # Characters are in different rows and columns
            first_char_row = 0
            first_char_col = 0
            second_char_row = 0
            second_char_col = 0
           
             # Find the row and column of each character in the pair
            for row_index in range(5):
                row = self._key_matrix[row_index]
                if pair[0] in row:
                    first_char_row = row_index
                    first_char_col = row.find(pair[0])
                if pair[1] in row:
                    second_char_row = row_index
                    second_char_col = row.find(pair[1])

            # Swap the columns of the characters to form a plain text pair
            plain_text_pair = self._key_matrix[first_char_row][second_char_col] + self._key_matrix[second_char_row][first_char_col]
            plain_text_pairs.append(plain_text_pair)

        return "".join(plain_text_pairs)

