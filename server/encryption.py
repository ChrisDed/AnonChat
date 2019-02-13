import base64
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class Encrypter:

    @staticmethod
    def get_key(password):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(password)
        return base64.urlsafe_b64encode(digest.finalize())

    @staticmethod
    def encrypt(password, token):
        try:
            f = Fernet(Encrypter.get_key(password))
            return f.encrypt(bytes(token))
        except InvalidToken:
            print("User entered wrong password")

    @staticmethod
    def decrypt(password, token):
        try:
            f = Fernet(Encrypter.get_key(password))
            return f.decrypt(bytes(token))
        except InvalidToken:
            print("User entered wrong password")

