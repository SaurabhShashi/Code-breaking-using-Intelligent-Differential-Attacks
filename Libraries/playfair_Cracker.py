import random
import string
from collections import Counter
from itertools import product
from math import exp

def create_key_matrix(keyword):
    keyword = keyword.upper().replace("J", "I")     # Convert keyword to uppercase, replace 'J' with 'I', and create a set of distinct characters
    key_matrix = list(set(keyword + string.ascii_uppercase.replace("J", "")))       # Split the list into 5x5 matrix
    return [key_matrix[i:i+5] for i in range(0, 25, 5)]

def swap_elements(matrix, indices):
    new_matrix = [row.copy() for row in matrix]
    a, b = indices
    new_matrix[a[0]][a[1]], new_matrix[b[0]][b[1]] = new_matrix[b[0]][b[1]], new_matrix[a[0]][a[1]]
    return new_matrix

def decrypt(ciphertext, key_matrix):
    def decrypt_pair(pair):
        row1, col1 = find_position(pair[0], key_matrix)     # Find the positions of the characters in the given pair within the key matrix
        row2, col2 = find_position(pair[1], key_matrix)
        if row1 == row2:        # Apply Playfair decryption rules
            return key_matrix[row1][(col1 - 1) % 5] + key_matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            return key_matrix[(row1 - 1) % 5][col1] + key_matrix[(row2 - 1) % 5][col2]
        else:
            return key_matrix[row1][col2] + key_matrix[row2][col1]

    def find_position(letter, matrix):          # Find the position of the given letter in the matrix
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                if col == letter:
                    return i, j
                
    ciphertext = ''.join([ch for ch in ciphertext if ch in ''.join(sum(key_matrix, []))])   # Remove characters not in the key matrix from the ciphertext

    if len(ciphertext) % 2 != 0:        # If the ciphertext length is odd, remove the last character
        ciphertext = ciphertext[:-1]
        
    pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]       # Split the ciphertext into pairs
    return "".join(decrypt_pair(pair) for pair in pairs)        # Decrypt each pair and join the result



def score(decrypted_text):      # List of most common English digraphs
    english_digraphs = ["TH", "HE", "IN", "EN", "NT", "RE", "ER", "AN", "TI", "ES", "ON", "AT", "SE", "ND", "OR", "AR", "AL", "TE", "CO", "DE", "TO", "RA", "ET", "ED", "IT", "SA", "EM", "RO", "ID", "EC", "TI", "SI", "EA", "IS", "HI", "RI", "VI", "VE", "HO", "WH", "PE", "LY", "ME", "DE", "LE", "NE", "RI", "BE", "ST", "CE", "MA", "LI", "HA", "GE", "OM", "LO"]
    digraph_counts = Counter([decrypted_text[i:i+2] for i in range(len(decrypted_text)-1)]) ## Count digraph occurrences in the decrypted text
    return sum(digraph_counts[digraph] for digraph in english_digraphs)


def break_playfair_cipher(ciphertext, initial_keyword, max_iterations=100000, annealing_schedule=200, annealing_factor=0.9995):
    key_matrix = create_key_matrix(initial_keyword)
    best_key_matrix = key_matrix
    best_decrypted_text = decrypt(ciphertext, best_key_matrix)
    best_score = score(best_decrypted_text)

    current_schedule = annealing_schedule

    for _ in range(max_iterations):
        indices = [(random.randint(0, 4), random.randint(0, 4)) for _ in range(2)]
        new_key_matrix = swap_elements(key_matrix, indices)
        new_decrypted_text = decrypt(ciphertext, new_key_matrix)
        new_score = score(new_decrypted_text)

        if new_score > best_score:
            best_key_matrix = new_key_matrix
            best_decrypted_text = new_decrypted_text
            best_score = new_score
            key_matrix = new_key_matrix
        elif random.random() < exp((new_score - best_score) / current_schedule):
            key_matrix = new_key_matrix

        current_schedule *= annealing_factor

        keyword_ret = "Best Key Matrix: "
        for row in best_key_matrix:
            keyword_ret = keyword_ret + (" ".join(row))
        retStr = keyword_ret + "\n" + "Decrypted Text:" + best_decrypted_text
        return retStr

