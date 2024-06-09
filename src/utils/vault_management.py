#!/usr/bin/env python3

import hashlib
import os
import time
from src.checker import init_verification
from src.utils.config import settings
from src.utils.lmdb import LMDBManager
from src.utils.key_management import derive_key
from src.utils.path_management import encrypt_decrypt_path, read_directory
from src.utils.backup_management import backup_files


def ensure_vault_exists():
    if not os.path.exists(settings.VAULT_DIR):
        os.makedirs(settings.VAULT_DIR)


def add_directory(path: str, backup: str, password: str):
    ensure_vault_exists()

    # Generate encryption key based on the provided password
    salt = os.urandom(16)
    key = derive_key(password, salt)
    encrypted_path = encrypt_decrypt_path(path, key, encrypt=True)

    # Check if the directory exists and has read permissions
    if not os.path.isdir(path) or not os.access(path, os.R_OK):
        print(f"Error: The directory '{path}' does not exist or cannot be read.")
        return

    # Proceed with adding the directory
    dir_path = os.path.join(settings.VAULT_DIR, encrypted_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    with open(os.path.join(dir_path, 'salt.dat'), 'wb') as salt_file:
        salt_file.write(salt)
    
    lmdb_manager = LMDBManager(dir_path, key)

    files = read_directory(path)

    start_time = time.time()  # Record start time
    for i, file in enumerate(files):
        lmdb_manager.insert_data(file)
        if (i + 1) % settings.BATCH_SIZE == 0:
            lmdb_manager.commit_batch()  # Commit batch transaction every `batch_size` insertions

    # Commit any remaining insertions that didn't fit into a full batch
    lmdb_manager.commit_batch()

    lmdb_manager.close()

    end_time = time.time()  # Record end time

   
    # Calculate and print the time taken for insertion
    print(f"Time taken for insertion: {end_time - start_time} seconds")
    
    print(f"Directory '{path}' is now being tracked under encrypted name '{encrypted_path}'.")

    init_verification(backup, path, settings.CHECK_INTERVAL, dir_path, key)

    