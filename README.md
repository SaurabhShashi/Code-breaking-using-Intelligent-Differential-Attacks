# Code-Breaking using Intelligent Differential Attacks

## Introduction

This project focuses on developing a GUI-based interactive model for breaking ciphertexts using intelligent differential attacks. The model supports various encryption algorithms such as Playfair cipher, Vigenere cipher, DES, and RSA, performing differential analysis to find decryption keys and plaintexts. It aims to demonstrate security vulnerabilities under various use-cases.

## Background Information

In network security, encryption algorithms play a crucial role in securing data transmissions. However, these algorithms are not always secure, and attackers can use techniques like differential attacks to exploit vulnerabilities and gain unauthorized access.

Differential attacks involve analyzing variations in input plaintext and output ciphertext to discover secret keys efficiently. This project explores differential attacks on encryption algorithms like Playfair cipher, Vigenere cipher, DES, and RSA.

## Methodology

The project adopts a GUI-based approach with two modules: ciphertext generation and differential analysis. It supports various encryption algorithms and follows these steps:

1. **Ciphertext Generation Module:**
   - User selects an encryption algorithm and key size.
   - Generates and displays the respective key(s).
   - Generates ciphertext for a given plaintext and key.
   - Stores the generated ciphertexts in a file.

2. **Differential Analysis Module:**
   - User selects the encryption algorithm and provides the file with ciphertext(s).
   - Performs differential analysis to find decryption keys and plaintext(s).
   - Displays the analysis output, including the secret key and plaintext.

3. **Attacks under the Relevant Standard(s):**
   - Tests the developed schemes under various use-cases to assess the security of encryption algorithms.

## Implementation

### Encryption Module

In this module, we have implemented a Python program for breaking codes using intelligent differential attacks. The program supports Playfair cipher, Vigenere cipher, DES, and RSA. It includes functions for encrypting plaintext, generating keys, and encrypting using various algorithms.

### Differential Analysis Module

The module includes an intermediate differential attack methodology outcome, showcasing letter frequencies in the ciphertext for Vigenere and Playfair algorithms. It also covers a differential attack on DES, a broadcast attack on RSA, and a differential attack on Playfair.

## Limitations

- In RSA, e must be the same for CRT attack.
- The plaintext size must be smaller than the key size for CRT to prevent loss of information.

## Attacks under Relevant Standard(s)

- Vigenere cipher: Vulnerable to CCA, CCA2.
- RSA: Vulnerable to IND-CPA (without proper padding schemes like OAEP).
- Playfair cipher: Vulnerable to IND-CPA, CCA, CCA2.

Feel free to explore the code and contribute to enhance code-breaking techniques using intelligent differential attacks.

