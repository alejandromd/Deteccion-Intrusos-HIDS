#!/usr/bin/env python3

from datetime import datetime
import os
import time
from src.utils.message_management import decrypt_message, encrypt_message

from src.utils.path_management import read_directory
from src.utils.backup_management import replace_files, backup_files
from src.utils.log_management import write_log


def init_verification(backup_path, verification_path, selected_time, dir_path, key):
    # Initial configuration
    log = {}
    current_month = datetime.now().strftime("%Y-%m")

    if not os.path.exists('./logs'):
        os.makedirs('./logs')

    if not os.path.exists(f'./logs/{current_month}-log.txt'):
        with open(f'./logs/{current_month}-log.txt', 'a') as f:
            f.write(f"{current_month} - Files replaced:\n")
            f.write("\n")

    backup_files(backup_path, verification_path)

    relative_paths = read_directory(backup_path,full_path=False)

    print("HIDS successfully initiated")
    print("The verification will be carried out periodically according to the chosen time interval")

    while True: # persistent loop

        time.sleep(selected_time.total_seconds())

        if datetime.now().strftime("%Y-%m") != current_month:
            with open(f'./logs/{current_month}-log.txt', 'r+') as f:
                num_replaced = int(len(f.readlines())/2) - 1
                f.write(f"Total files replaced: {num_replaced}")
                
            current_month = datetime.now().strftime("%Y-%m")
            with open(f'./logs/{current_month}-log.txt', 'a') as f:
                f.write(f"{current_month} - Files replaced:\n")
                f.write("\n")


        log = replace_files(relative_paths, backup_path, verification_path, {}, current_month, dir_path, key)

        if len(log[current_month]) > 0:
            write_log(log, current_month)