#!/usr/bin/env python3

from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
from cryptography.fernet import Fernet


def encrypt_decrypt_path(path: str, key: bytes, encrypt=True) -> str:
    f = Fernet(key)
    if encrypt:
        return urlsafe_b64encode(f.encrypt(path.encode())).decode('utf-8')
    else:
        return f.decrypt(urlsafe_b64decode(path)).decode('utf-8')
    

def read_directory(directory_path, base_path=None, full_path=True):
    found_files = []

    # Set the base_path to directory_path if not specified
    if base_path is None:
        base_path = directory_path
    
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)

        if os.path.isfile(file_path): # If it's a file
            if full_path:
                # Append the full path
                found_files.append(file_path)
            else:
                # Calculate and append the relative path
                relative_path = os.path.relpath(file_path, base_path)
                found_files.append(relative_path)

        elif os.path.isdir(file_path): # If it's a directory
            # Recursively call read_directory for the directory
            found_files.extend(read_directory(file_path, base_path=base_path, full_path=full_path))

    return found_files