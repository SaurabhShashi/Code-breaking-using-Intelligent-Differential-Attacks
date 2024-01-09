import random
import string
import sys
sys.path.append("D:\\1-2\\NS\\P4_KS-Kumar_Shivanshi_Avinash_Saurabh\\Lib")
from playFair_p4 import PlayfairCipher


# Example larger plaintexts
M1 = "THIS IS THE SECOND PROJECT IN NETWORK SECURITY PROJECT"
M2 = "HERE WE ARE WORKING ON PLAY FAIR CIPHER ALGORITHM"

# Encryption key
key = "KEYWORD"

# Encryption oracle function
def encryption_oracle(plaintext, key):
    playfair = PlayfairCipher()         # Create an instance of the PlayfairCipher class. 
    return playfair.encrypt(plaintext, key)
'''
# Generate candidate plaintexts
def generate_candidate_plaintexts(M1, M2, num_candidates=100):
    candidates = []
    for _ in range(num_candidates):
        base = random.choice([M1, M2])
        modified = list(base)
        idx = random.randint(0, len(base) - 1)
        while modified[idx] == base[idx]:
            modified[idx] = random.choice(string.ascii_uppercase)
        candidates.append("".join(modified))
    return candidates

# CPA attack
def playfair_cpa_attack(M1, M2, key):
    # Step 1 & 2
    C = encryption_oracle(random.choice([M1, M2]), key)

    # Step 3
    candidates = generate_candidate_plaintexts(M1, M2)

    # Step 4
    candidate_ciphertexts = {candidate: encryption_oracle(candidate, key) for candidate in candidates}

    # Step 5 & 6
    for candidate, candidate_ciphertext in candidate_ciphertexts.items():
        differences_C = sum([1 for c1, c2 in zip(C, candidate_ciphertext) if c1 != c2])
        if candidate in M1:
            differences_M = sum([1 for m1, m2 in zip(M1, candidate) if m1 != m2])
        else:
            differences_M = sum([1 for m1, m2 in zip(M2, candidate) if m1 != m2])

        if differences_C == differences_M:
            encrypted_message = M1 if candidate in M1 else M2
            break
    else:
        encrypted_message = M2

    return encrypted_message

# Test the attack
encrypted_message = playfair_cpa_attack(M1, M2, key)
print("Encrypted message:", encrypted_message)
'''



def generate_alternative_plaintexts(M1, M2, num_alternatives=100):
    alternatives = []
    for _ in range(num_alternatives):
        base = random.choice([M1, M2])
        modified = list(base)
        for idx in range(0, len(base), 2):
            modified[idx] = random.choice(string.ascii_uppercase)
        alternatives.append("".join(modified))
    return alternatives

def playfair_cpa_attack(M1, M2, key):
    C = encryption_oracle(random.choice([M1, M2]), key)
    alternatives = generate_alternative_plaintexts(M1, M2)
    print(alternatives)
    alternative_ciphertexts = {alternative: encryption_oracle(alternative, key) for alternative in alternatives}

    for alternative, alternative_ciphertext in alternative_ciphertexts.items():
        differences_C = sum([1 for c1, c2 in zip(C, alternative_ciphertext) if c1 != c2])
        if alternative in M1:
            differences_M = sum([1 for m1, m2 in zip(M1, alternative) if m1 != m2])
        else:
            differences_M = sum([1 for m1, m2 in zip(M2, alternative) if m1 != m2])

        if differences_C == differences_M:
            encrypted_message = M1 if alternative in M1 else M2
            break
    else:
        encrypted_message = M2

    return encrypted_message

encrypted_message = playfair_cpa_attack(M1, M2, key)
print("Encrypted message:", encrypted_message)
