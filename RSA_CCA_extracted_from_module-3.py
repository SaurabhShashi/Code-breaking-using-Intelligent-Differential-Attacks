from Crypto.PublicKey import RSA
from Crypto.Util import number
from Crypto.Util.number import bytes_to_long, long_to_bytes

def rsa_encrypt(m, public_key):
    return pow(m, public_key.e, public_key.n)

def rsa_decrypt(c, private_key):
    return pow(c, private_key.d, private_key.n)

def inverse_mod(a, m):
    return pow(a, -1, m)

# Generate RSA keys
keySize = 2048
key = RSA.generate(int(keySize))
public_key = key.publickey()
modulus_n = public_key.n

# Example plaintext as text
actualPlaintext = "This is a final text message that we want to retrieve and is only used to generate initial cipher."
P = bytes_to_long(actualPlaintext.encode())

# Encrypt the plaintext
C = rsa_encrypt(P, public_key)

# Attacker intercepts C and selects random plaintext p1
randomPlaintext = "This is the some random plaintext we use to find actualPlaintext"
p1 = bytes_to_long(randomPlaintext.encode())

# Attacker encrypts p1 using the public key to produce a new ciphertext c1
c1 = rsa_encrypt(p1, public_key)

# Attacker computes the modified ciphertext c2
c2 = (C * c1) % modulus_n 

# Attacker sends c2 to the decryption oracle and receives the decrypted plaintext p2
p2 = rsa_decrypt(c2, key)

# Attacker calculates the original plaintext P using p2 and p1
recovered_P = (p2 * inverse_mod(p1, modulus_n)) % modulus_n

# Convert the recovered plaintext back to text
recovered_text = long_to_bytes(recovered_P).decode()

print("Original plaintext:", recovered_text)
