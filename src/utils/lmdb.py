import hashlib
import lmdb
from cryptography.fernet import Fernet
import os

class LMDBManager:
    def __init__(self, db_path, encryption_key):
        self.db_path = db_path
        self.encryption_key = encryption_key
        self.fernet = Fernet(encryption_key)
        self._init_database()

    def _init_database(self):
        self.env = lmdb.open(self.db_path, map_size=1048576000, map_async=True)
        self.batch_txn = self.env.begin(write=True)

    def encrypt_file_name(self, file_name):
        encrypted_file_name = self.fernet.encrypt(file_name.encode())
        return encrypted_file_name

    def decrypt_file_name(self, encrypted_file_name):
        decrypted_file_name = self.fernet.decrypt(encrypted_file_name)
        return decrypted_file_name.decode()

    def insert_data(self, file_path):
        with open(file_path, 'rb') as file:
            file_content = file.read()
            encrypted_file_content_hash = self.fernet.encrypt(hashlib.sha256(file_content).digest())
        self.batch_txn.put(file_path.encode(), encrypted_file_content_hash)
    
    def commit_batch(self):
        self.batch_txn.commit()
        self.batch_txn = self.env.begin(write=True)
        
    def retrieve_data(self, key):
        with self.env.begin() as txn:
            encrypted_value = txn.get(key.encode())
        if encrypted_value:
            decrypted_value = self.fernet.decrypt(encrypted_value)
            return decrypted_value
        else:
            return None

    def close(self):
        self.commit_batch()
        self.env.close()
