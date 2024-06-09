#!/usr/bin/env python3

from getpass import getpass

from src.utils.vault_management import ensure_vault_exists, add_directory
from src.utils.config import settings

def main_menu():
    ensure_vault_exists()

    actions = {'1': ('Track directory', 'add'),
               '2': ('Exit', 'exit')}
    
    with open(settings.ART_DIR, 'r') as file:
        art = file.read()
        print(art)
        
    while True:
        print("\nDirectory Tracker CLI")
        for key, (desc, _) in actions.items():
            print(f"{key}. {desc}")

        choice = input("Choose an action: ")

        if choice == '1':
            path = input("Enter the directory path to track: ")
            backup = input("Enter the directory to store the backup: ")
            password = getpass("Enter your password: ")
            add_directory(path, backup, password)
        elif choice == '2':
            exit()
        else:
            print("Invalid choice, please select a valid option.\n")

if __name__ == "__main__":
    main_menu()