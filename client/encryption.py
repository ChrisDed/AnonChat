import sys
import base64
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class ClientEncryption:

    def get_key(self, password):
        try:
            digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            digest.update(password)
            return base64.urlsafe_b64encode(digest.finalize())
        except InvalidToken:
            print("Invalid password")
            sys.exit()

    def encrypt(self, password, token):
        try:
            f = Fernet(self.get_key(password))
            return f.encrypt(bytes(token))
        except InvalidToken:
            print("Invalid password.")
            sys.exit()

    def decrypt(self, password, token):
        try:
            f = Fernet(self.get_key(password))
            return f.decrypt(bytes(token))
        except InvalidToken:
            print("Invalid password.")
            sys.exit()
    
