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
from tkinter import filedialog
from vigenere import encrypt   #Can also add decrypt, random_key
from Crypto.Cipher import DES3
#import os
#import secrets
import base64
from Crypto.Util.number import bytes_to_long, long_to_bytes
import sys
sys.path.append("D:\\1-2\\NS\\P4_KS-Kumar_Shivanshi_Avinash_Saurabh\\Lib")
import vigenere_Cracker
import RSA_Cracker
import playfair_Cracker

cipherText_files_list = []
publicKeys_n_list = []

def initiateAttacks():
    selected_cipher = cipherAttr.get()
    keyAndPlainText = None
    if selected_cipher == "Playfair cipher":
        cipherTexts_combined = "".join(cipherText_files_list)
        keyAndPlainText = playfair_Cracker.break_playfair_cipher(cipherTexts_combined, "Monarchy")
    elif selected_cipher == "Vignere cipher":
        cipherTexts_combined = "".join(cipherText_files_list)
        keyAndPlainText = vigenere_Cracker.crack_vigenere(cipherTexts_combined)
    elif selected_cipher == "DES":
        keyAndPlainText = "no differential attack for 128-bit key encrypted data"
    elif selected_cipher == "RSA":
        e = 3   #when e is large (eg: 65537), the operation becomes more complex i.e finding the 65537th root of the combined ciphertext
        keyAndPlainText = RSA_Cracker.broadcast_attack(cipherText_files_list, e, publicKeys_n_list)
    plain_text.configure(state='normal')  # Even for the compiler to update this attribute, it should be write mode.
    plain_text.delete("1.0", "end")
    plain_text.insert("1.0", keyAndPlainText)
    plain_text.configure(state='disabled')  # read-only

def setButtonVisibility(*args):
    selected_cipher = cipherAttr.get()
    if selected_cipher == "RSA":
        select_PKn_button.pack(pady=5)
        publicKeys_n_label.pack(pady=15)
        publicKeys_display.pack(pady=5)

    else:
        select_PKn_button.pack_forget()
        publicKeys_n_label.pack_forget()
        publicKeys_display.pack_forget()


def open_files_for_cipherTexts():
    file_paths = filedialog.askopenfilenames(title="Select files", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    global cipherText_files_list
    cipherText_files_list.clear()

    for file_path in file_paths:
        with open(file_path, "r") as file:
            content_ct = file.read()
            selected_cipher = cipherAttr.get()
            if selected_cipher == "RSA":
                cipherText_files_list.append(int(content_ct))
            else:
                cipherText_files_list.append(content_ct)
            cipherTexts_display.insert(tk.END, f"{content_ct}\n\n")     #f"File Info: {file_path}\n{content}\n\n")

def open_files_for_publicKeys():
    file_paths = filedialog.askopenfilenames(title="Select files", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    global publicKeys_n_list
    publicKeys_n_list.clear()

    for file_path in file_paths:
        with open(file_path, "r") as file:
            content_publicKey_n = file.read()
            publicKeys_n_list.append(int(content_publicKey_n))
            publicKeys_display.insert(tk.END, f"{content_publicKey_n}\n\n")     #f"File Info: {file_path}\n{content}\n\n")

root = tk.Tk()
root.geometry("1200x700")
root.title("Module-2")

# Background Image
bg_image = Image.open("W:\sl.jpg")
bg_image = bg_image.resize((1200, 700), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
garamond_font = tkfont.Font(family="Garamond", size=24, weight="bold")
title_label = tk.Label(root, text="Differential Analysis Module", font=garamond_font, fg="white", bg="black")
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
cipherAttr.trace("w", setButtonVisibility)  # Whenever cipherAttr changes, call update_key_size_options 

#cipher_menu = tk.OptionMenu(left_frame, cipherAttr, *cipher_options)
cipher_menu = ttk.Combobox(left_frame, textvariable=cipherAttr, values=cipher_options, state="readonly")
cipher_menu.pack(pady=5)

select_ciphers_button = tk.Button(left_frame, text="Select CipherTexts", command=open_files_for_cipherTexts)
select_ciphers_button.pack(pady=20)

select_PKn_button = tk.Button(left_frame, text="Select PublicKeys(n)", command=open_files_for_publicKeys)
select_ciphers_button.pack(pady=25)


cipherTexts_label = tk.Label(left_frame, text="CipherTexts")
cipherTexts_label.pack(pady=5)

cipherTexts_display = tk.Text(left_frame, wrap="word", width=30, height=7)
cipherTexts_display.pack(pady=5)

publicKeys_n_label = tk.Label(left_frame, text="PublicKeys(n)")

publicKeys_display = tk.Text(left_frame, wrap="word", width=30, height=7)

# Middle
middle_frame = tk.Frame(root, width=200, height=200)
middle_frame.pack(side="left", padx=10, pady=10)

attack_button = tk.Button(middle_frame, text="Attack", width=15, height=3)
attack_button.pack(pady=5)
attack_button.configure(command= lambda:initiateAttacks())

# Right side
right_frame = tk.Frame(root, width=350, height=400, bd=1, relief="solid")
right_frame.pack(side="left", padx=10, pady=10)

right_frame.pack_propagate(0)        #Prevents automatic resizing. Else width and height would be ignored. 

plain_text_label = tk.Label(right_frame, text="Key and Plain Text:")
plain_text_label.pack(pady=5)

plain_text = tk.Text(right_frame, wrap="word", width=60, height=20)
plain_text.pack(pady=5)

#attack_button.configure(command= lambda:start_diff_attack())

root.mainloop()
