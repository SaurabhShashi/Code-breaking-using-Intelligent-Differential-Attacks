import tkinter as tk
from tkinter import ttk
import random
import string
from PIL import Image, ImageTk
from Crypto.Cipher import DES       #pip3 install pycryptodome. Pycrypto is vulnerable to a heap-based buffer overflow (CVE-2013-7459)
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font as tkfont
from playFair_p4 import PlayfairCipher
from vigenere import encrypt   #Can also add decrypt, random_key
from Crypto.Cipher import DES3
#import os
#import secrets
import base64
from Crypto.Util.number import bytes_to_long, long_to_bytes


rsa_public_key = None           #Stores RSA public key, so that values need not be fetched from UI attribute


def playfair_cipher_encrypt(plaintext, key):
    playfair = PlayfairCipher()         # Create an instance of the PlayfairCipher class. 
    encrypted_text_playfair = playfair.encrypt(plaintext, key)
    return encrypted_text_playfair

    
def vigenere_cipher_encrypt(plaintext, key):
    encrypted_text_vigenere = encrypt(plaintext, key)
    return encrypted_text_vigenere

#Start - DES encryption

#DES uses 64-bit blocks, hence the data should be in a multiple of 8 bytes format. This is achieved with padding.
def apply_pkcs7_padding(plaintext, block_size):
    padding_length = block_size - (len(plaintext) % block_size)      # Calculate the padding length required to make the data length a multiple of the block_size
    return plaintext.encode('utf-8') + bytes([padding_length]) * padding_length      # Add the padding to the data, using the padding_length as the byte value for each padding byte


def des_encrypt(plaintext, key):
    # Apply PKCS7 padding to the plaintext to ensure its length is a multiple of the 3DES block size (8 bytes)
    padded_plaintext = apply_pkcs7_padding(plaintext, DES3.block_size) # DES3.block_size is 8 bytes (64 bits) 
    cipher_mode = DES3.new(key, DES3.MODE_ECB)           # With the given key, make a 3DES(as we need a minimum 128 bit key) cipher object in ECB mode
    ciphertext = cipher_mode.encrypt(padded_plaintext)   
    return ciphertext

#End - DES encryption

def rsa_encrypt(plaintext):
    plainText_long = bytes_to_long(plaintext)
    cipherText_long = pow(plainText_long, rsa_public_key.e, rsa_public_key.n) #RSA algorithm -> C = (M ^ e) mod n
    cipherText_bytes = long_to_bytes(cipherText_long)
    cipherText = base64.b64encode(cipherText_bytes).decode('utf-8') #Bytes to ASCII and ASCII to string
    return cipherText

# Key generation for Playfair cipher
def generate_playfair_key(keySize):
    key = ''.join(random.sample(string.ascii_uppercase, int(int(keySize)/8)))
    return key

# Key generation for Vigenere cipher
def generate_vigenere_key(keySize):
    key = ''.join(random.choices(string.ascii_uppercase, k=int(int(keySize)/8))) #Absence of k will throw TypeError: The number of choices must be a keyword argument: k=16
    return key

# Key generation for DES
def generate_des_key(keySize):
    key = get_random_bytes(int(int(keySize)/8))       #Alternately secrets.token_bytes can be used
    return key

# Key generation for RSA
def generate_rsa_key_pair(keySize):
    key = RSA.generate(int(keySize))                #This if printed won't show the public or private key. Only a random string will be returned.
    global rsa_public_key
    rsa_public_key = key.publickey()
    private_key = key.export_key().decode('utf-8')      #decode is used to convert bytes to string objects
    public_key = rsa_public_key.export_key().decode('utf-8')
    return public_key, private_key

def generate_key(keySize):
    selected_cipher = cipherAttr.get()
    final_key = ""
    if selected_cipher == "Playfair cipher":
        final_key = generate_playfair_key(keySize) 
    elif selected_cipher == "Vignere cipher":
        final_key = generate_vigenere_key(keySize)
    elif selected_cipher == "DES":
        final_key = generate_des_key(keySize)
        final_key = final_key.hex()
    elif selected_cipher == "RSA":
        final_key = generate_rsa_key_pair(keySize)
        
    else:
        tk.messagebox.showerror("Error", "Invalid encryption algorithm selected.")
        return
    displayed_key.configure(state='normal')  # Even for the compiler to update this attribute, it should be write mode.
    displayed_key.delete("1.0", "end")
    displayed_key.insert("1.0", final_key)
    displayed_key.configure(state='disabled')  # read-only


def p4_encryption():
    plaintext = plain_text.get("1.0", "end-1c") # 1.0 = line 1, character 0 . end-1c =  which corresponds to the position of the last character in the widget, excluding the newline character that Tkinter automatically adds to the end of the text content.
    encryption_key = displayed_key.get("1.0", "end-1c")
    selected_cipher = cipherAttr.get()

    if selected_cipher == "Playfair cipher":
        ciphertext = playfair_cipher_encrypt(plaintext, encryption_key)
    elif selected_cipher == "Vignere cipher":
        ciphertext = vigenere_cipher_encrypt(plaintext, encryption_key)
    elif selected_cipher == "DES":
        ciphertext_bytes = des_encrypt(plaintext, bytes.fromhex(encryption_key))
        ciphertext_base64 = base64.b64encode(ciphertext_bytes)      #Bytes to ASCII
        ciphertext = ciphertext_base64.decode('utf-8')              #ASCII to string
    elif selected_cipher == "RSA":
        ciphertext = rsa_encrypt(plaintext.encode('utf-8'))

    else:
        tk.messagebox.showerror("Error", "Invalid encryption algorithm selected.")

    with open("ciphertext.txt", "w") as output_file:
        output_filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if output_filepath:
            with open(output_filepath, "w") as output_file:
                output_file.write(ciphertext)
            tk.messagebox.showinfo("Success", f"Ciphertext has been saved to {output_filepath}")
        else:
            tk.messagebox.showinfo("Cancelled", "File save has been cancelled")


#Based on the selected cipher. available key size options changes
def update_key_size_options(*args):     #When using the trace() method with the "w" (write) option, it passes three arguments to the callback function: the name of the variable, the name of the index or array element being modified, and the mode(here it is write, i.e "w")

    selected_cipher = cipherAttr.get()

    if selected_cipher == "Playfair cipher":
        key_size_options = [64]
    elif selected_cipher == "Vignere cipher" or selected_cipher == "DES":
        key_size_options = [128, 192]
    elif selected_cipher == "RSA":
        key_size_options = [1024, 2048, 3072]

    key_size_menu['values'] = key_size_options  # Set the new key size options
    key_sizeAttr.set(key_size_options[0])  # Set the default key size based on the selected cipher


root = tk.Tk()
root.geometry("1200x700")
root.title("Module-1")

# Background Image
bg_image = Image.open("W:\sl.jpg")
bg_image = bg_image.resize((1200, 700), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
garamond_font = tkfont.Font(family="Garamond", size=24, weight="bold")
title_label = tk.Label(root, text="Encryption Module", font=garamond_font, fg="white", bg="black")
title_label.place(x=450, y=0)
# Left side
left_frame = tk.Frame(root, bd=1, relief="solid", width=300, height=500)
left_frame.pack(side="left", padx=20, pady=20)
left_frame.pack_propagate(0)        #Prevents automatic resizing. Else width and height would be ignored. 

cipher_label = tk.Label(left_frame, text="Select Encryption Algorithm:")
cipher_label.pack(pady=10)

cipher_options = ["Playfair cipher", "Vignere cipher", "DES", "RSA"]
cipherAttr = tk.StringVar()
cipherAttr.set(cipher_options[0])
cipherAttr.trace("w", update_key_size_options)  # Whenever cipherAttr changes, call update_key_size_options 

#cipher_menu = tk.OptionMenu(left_frame, cipherAttr, *cipher_options)
cipher_menu = ttk.Combobox(left_frame, textvariable=cipherAttr, values=cipher_options, state="readonly")
cipher_menu.pack(pady=5)
cipher_menu.bind("<<ComboboxSelected>>", update_key_size_options)       #bind() method to listen to the ComboboxSelected event.

key_size_label = tk.Label(left_frame, text="Key Size:")
key_size_label.pack(pady=5)

key_sizeAttr = tk.StringVar()
#key_size_menu = tk.OptionMenu(left_frame, key_sizeAttr, "")
key_size_menu = ttk.Combobox(left_frame, textvariable=key_sizeAttr, state="readonly") 

key_size_menu.pack(pady=5)

update_key_size_options()  # Call the function to populate the initial key size options based on the default cipher

#key_generate_button = tk.Button(left_frame, text="Generate Key", command=generate_key)
key_generate_button = tk.Button(left_frame, text="Generate Key")

key_generate_button.pack(pady=25)

key_label = tk.Label(left_frame, text="Encryption Key:")
key_label.pack(pady=15)

displayed_key = tk.Text(left_frame, wrap="word", width=30, height=15)
displayed_key.pack(pady=5)

# Using lambda function to pass the displayed_key widget to the generate_key function
key_generate_button.configure(command=lambda: generate_key(key_sizeAttr.get()))

# Middle
middle_frame = tk.Frame(root, width=200, height=200)
middle_frame.pack(side="left", padx=10, pady=10)

encrypt_button = tk.Button(middle_frame, text="Encrypt", width=15, height=3)
encrypt_button.pack(pady=5)

# Right side
right_frame = tk.Frame(root, width=350, height=400, bd=1, relief="solid")
right_frame.pack(side="left", padx=10, pady=10)

right_frame.pack_propagate(0)        #Prevents automatic resizing. Else width and height would be ignored. 

plain_text_label = tk.Label(right_frame, text="Enter Plain Text:")
plain_text_label.pack(pady=5)

plain_text = tk.Text(right_frame, wrap="word", width=60, height=20)
plain_text.pack(pady=5)

encrypt_button.configure(command= lambda:p4_encryption())

root.mainloop()
