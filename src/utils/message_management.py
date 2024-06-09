from cryptography.fernet import Fernet
from pathlib import Path
import os

def init_Fernet():
    if not os.path.exists(str(Path.home()) +"/PAI1"):
        os.makedirs(str(Path.home()) +"/PAI1")
    if not os.path.exists(str(Path.home()) +"/PAI1/key_fernet.txt"):
        with open(str(Path.home()) + "/PAI1/key_fernet.txt", "wb") as f:
            f.write(Fernet.generate_key())

    with open(str(Path.home()) + "/PAI1/key_fernet.txt", "rb") as f:
        return Fernet(f.read())

def encrypt_message(message):
    cipher_suite = init_Fernet()
    return cipher_suite.encrypt(message.encode())

def decrypt_message(message):
    cipher_suite = init_Fernet()
    return cipher_suite.decrypt(message).decode()