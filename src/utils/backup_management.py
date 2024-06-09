#!/usr/bin/env python3


from datetime import datetime
import hashlib
import os
import shutil

from src.utils.lmdb import LMDBManager
from src.utils.path_management import encrypt_decrypt_path


def backup_files(backup_path, verification_path):
    """
    Create a backup of the verification folder
    """
    if os.path.exists(backup_path):
        shutil.rmtree(backup_path)

    os.makedirs(backup_path)
    shutil.copytree(verification_path, backup_path, dirs_exist_ok=True)


def replace_files(relative_paths, backup_path, verification_path, log, current_month, dir_path, key):
    """
    Replace the files in the verification folder with the ones in the backup folder
    """
    replaced_files = []

    lmdb_manager = LMDBManager(dir_path, key)

    for file_name in relative_paths:
        verification_file_path = os.path.join(verification_path, file_name)
        backup_file_path = os.path.join(backup_path, file_name)

        try:
            with open(verification_file_path, 'rb') as file:
                file_content = file.read()
            sha = hashlib.sha256(file_content).digest()
        except:
            sha = None

        if (lmdb_manager.retrieve_data(str(verification_file_path)) != sha) and os.path.exists(backup_file_path): 
            try:
                # Create the target directory if it doesn't exist
                dest_dir = os.path.dirname(verification_file_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                shutil.copy(backup_file_path, verification_file_path)
                replaced_files.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + file_name)
            except:
                pass

    lmdb_manager.close()

    log.setdefault(current_month, []).extend(replaced_files)
    return log