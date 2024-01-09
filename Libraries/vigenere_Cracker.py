
import string
import math
from collections import Counter
from itertools import cycle
import matplotlib.pyplot as plt

# English letter frequency
ENGLISH_LETTER_FREQS = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702, 'F': 0.02228,
    'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
    'M': 0.02406, 'N': 0.06749, 'O': 0.07507, 'P': 0.01929, 'Q': 0.00095, 'R': 0.05987,
    'S': 0.06327, 'T': 0.09056, 'U': 0.02758, 'V': 0.00978, 'W': 0.0236, 'X': 0.0015,
    'Y': 0.01974, 'Z': 0.00074
}

# Function to plot letter frequencies in the ciphertext
def plot_letter_frequencies(ciphertext):
    # Calculate the frequency of each letter in the ciphertext
    letter_counts = Counter(ciphertext)
    letters = sorted(list(ENGLISH_LETTER_FREQS.keys()))
    frequencies = [letter_counts[letter] / len(ciphertext) for letter in letters]

    # Plot the letter frequencies in a bar chart
    plt.bar(letters, frequencies)
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.title('Letter Frequencies in Ciphertext')
    plt.show()

def index_of_coincidence(ct):
    letter_counts = Counter(ct)
    text_length = len(ct)
    ic = 0.0
    for count in letter_counts.values():
        ic += count * (count - 1)
    ic /= text_length * (text_length - 1)
    return ic

def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    for char, key_char in zip(ciphertext, cycle(key)):
        decrypted_char = chr(((ord(char) - ord(key_char)) % 26) + ord('A'))
        decrypted_text.append(decrypted_char)
    return ''.join(decrypted_text)

def find_key_length(ciphertext):
    english_ic = 0.065
    ciphertext = ''.join(char.upper() for char in ciphertext if char.isalpha())

    # Kasiski examination to find repeating sequences
    distances = []
    for length in range(3, 6):
        for i in range(len(ciphertext) - length):
            substring = ciphertext[i:i+length]
            if substring in ciphertext[i+length:]:
                distance = ciphertext[i+length:].index(substring) + length
                distances.append(distance)
    if not distances:
        return None

    # Calculate the key length estimates from the distances
    factors = []
    for i in range(len(distances)):
        for j in range(i+1, len(distances)):
            factor = math.gcd(distances[i], distances[j])
            if factor > 1:
                factors.append(factor)
    if not factors:
        return None
    key_length = max(set(factors), key=factors.count)

    # Friedman test to refine key length estimate
    n = len(ciphertext)
    ciphertext_ic = index_of_coincidence(ciphertext)
    key_length_estimate = (english_ic * (n - 1)) / ((n * ciphertext_ic) - (n * english_ic) + ciphertext_ic)
    key_length_estimate = round(key_length_estimate)
    if abs(key_length_estimate - key_length) <= 2:
        return key_length
    return 16

def find_key(ciphertext, key_length):
    key = []
    for i in range(key_length):
        substring = ciphertext[i::key_length]
        max_corr = -1
        key_char = 'A'
        for candidate_key_char in string.ascii_uppercase:
            decrypted_text = vigenere_decrypt(substring, candidate_key_char)
            letter_freqs = Counter(decrypted_text)
            total_characters = len(decrypted_text)
            corr = sum(ENGLISH_LETTER_FREQS[letter] * (letter_freqs[letter] / total_characters) for letter in string.ascii_uppercase)
            if corr > max_corr:
                max_corr = corr
                key_char = candidate_key_char
        key.append(key_char)
    return ''.join(key)

def crack_vigenere(ciphertext):
    ciphertext = ''.join(char.upper() for char in ciphertext if char.isalpha())
    key_length = find_key_length(ciphertext)
    key = find_key(ciphertext, key_length)
    plaintext = vigenere_decrypt(ciphertext, key)
    # Plot the letter frequencies and the IC values for different key lengths
    plot_letter_frequencies(ciphertext)
    return "key:" + key + "plaintext:" + plaintext

