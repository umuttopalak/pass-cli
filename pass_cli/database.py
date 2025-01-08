import base64
import os
import sqlite3
from datetime import datetime

import keyring
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PasswordManager:
    KEYRING_SERVICE = "pass-cli"
    KEYRING_USERNAME = "encryption_key"
    ITERATIONS = 100 if os.getenv('TESTING') == 'true' else 1000
    DEFAULT_DB_PATH = os.path.expanduser('~/.pass-cli/passwords.db')

    def __init__(self, encryption_key: str = None, db_path: str = None):
        self.db_path = db_path or self.DEFAULT_DB_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self._init_db()
        
        if encryption_key is None:
            return
            
        if not self._has_encryption_key():
            self._set_encryption_key(encryption_key)
            keyring.set_password(self.KEYRING_SERVICE, self.KEYRING_USERNAME, encryption_key)
        elif not self._verify_encryption_key(encryption_key):
            raise ValueError("Invalid encryption key")
            
        self._setup_cipher(encryption_key)

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS encryption_keys (
                    id INTEGER PRIMARY KEY,
                    key_hash TEXT NOT NULL,
                    salt TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY,
                    service_name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    encrypted_password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def _has_encryption_key(self) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM encryption_keys')
            return cursor.fetchone()[0] > 0

    def _set_encryption_key(self, key: str):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.ITERATIONS,
        )
        key_hash = base64.b64encode(kdf.derive(key.encode())).decode()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO encryption_keys (key_hash, salt)
                VALUES (?, ?)
            ''', (key_hash, base64.b64encode(salt).decode()))

    def _verify_encryption_key(self, key: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT key_hash, salt FROM encryption_keys LIMIT 1')
            stored_hash, stored_salt = cursor.fetchone()
            
            salt = base64.b64decode(stored_salt)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=self.ITERATIONS,
            )
            key_hash = base64.b64encode(kdf.derive(key.encode())).decode()
            return key_hash == stored_hash

    def _setup_cipher(self, key: str):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'encryption-salt',
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(key.encode()))
        self.cipher_suite = Fernet(key)

    def store_password(self, service_name: str, username: str, password: str):
        encrypted_password = self.cipher_suite.encrypt(password.encode()).decode()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO passwords (service_name, username, encrypted_password)
                VALUES (?, ?, ?)
            ''', (service_name, username, encrypted_password))

    def get_password(self, service_name: str, username: str) -> str:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT encrypted_password FROM passwords
                WHERE service_name = ? AND username = ?
            ''', (service_name, username))
            
            result = cursor.fetchone()
            if result:
                encrypted_password = result[0]
                return self.cipher_suite.decrypt(encrypted_password.encode()).decode()
            return None 

    @classmethod
    def get_stored_key(cls) -> str:
        """Get encryption key from keyring"""
        return keyring.get_password(cls.KEYRING_SERVICE, cls.KEYRING_USERNAME) 