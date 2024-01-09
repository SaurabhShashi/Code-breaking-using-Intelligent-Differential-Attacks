# P4 - Cryptographic Differential Attacks Toolkit

Welcome to P4, your comprehensive toolkit for cryptographic differential attacks. This project is designed to provide a user-friendly interface for generating keys, creating cipher texts, and performing differential attacks with ease.

## Modules

### Module 1: Key Generation and Encryption

- **Key Generation:**
  - Select your encryption algorithm.
  - Update to your required key size.
  - Click "Generate Key" for secure key creation.

- **Encryption:**
  - Add plain text.
  - Click on "Encrypt" for quick and efficient encryption.

Make sure to avoid key regeneration when using different plain texts for the same algorithm (excluding RSA).

### RSA Encryption

For RSA encryption, follow these guidelines:

- Use the same plain text for at least 3 cipher texts.
- Generate a different key each time.
- Save the public key modulus value (n) in a text file for each generated key using 'Save PK(n)'.
- Ensure that generated cipher texts and keys have the same order.

### Differential Attacks - Module 2

- Select the cipher text and initiate the attack.
- For RSA, upload the public key modulus (n) for attack execution.

