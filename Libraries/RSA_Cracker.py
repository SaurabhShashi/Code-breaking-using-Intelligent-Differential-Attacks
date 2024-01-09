import sys
sys.path.append("c:\\users\\kskum\\appdata\\local\\programs\\python\\python310\\lib\\site-packages\\")      #if gmpy2 installation is successful, then there is no need to include this
import gmpy2
import math
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA

def chinese_remainder_theorem(ciphertexts, moduli):
    total_modulus_product = math.prod(moduli)       #Computes the product of all the moduli (n1, n2, n3, ...) and stores it in the variable M.
    modulus_product_list_withoutNi = [total_modulus_product // single_modulus for single_modulus in moduli]     # eg: n1*n2*n3/ n1
    inverses = [gmpy2.invert(modulus_product_list_withoutNi[i], single_modulus) for i, single_modulus in enumerate(moduli)] #modular inverses of each pair
    result = sum(gmpy2.mul(gmpy2.mul(ciphertexts[i], modulus_product_list_withoutNi[i]), inverses[i]) for i in range(len(ciphertexts))) % total_modulus_product #This line computes the sum of the products of ciphertexts[i], modulus_product_list_withoutNi, and inverses[i] for each index i in the range of the length of the ciphertexts list, and then takes the result modulo M. 
    return int(result)

def broadcast_attack(ciphertexts, e, moduli):
    C = chinese_remainder_theorem(ciphertexts, moduli)
    m = gmpy2.iroot(C, e)[0]
    return long_to_bytes(int(m)).decode(errors='ignore')

e = 3   #when e is large (eg: 65537), the operation becomes more complex i.e finding the 65537th root of the combined ciphertext

# Decrypt with the provided broadcast_attack function
#plaintext_decoded = broadcast_attack(ciphertexts, e, moduli)
#print(plaintext_decoded)
