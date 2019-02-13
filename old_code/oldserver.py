# DarkRoom - Anonymous, Encrypted, Multithreaded Python Chat Application

# Server side code

import sys
import os

import configparser
from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM

import base64
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Terminal retro logo

os.system("clear")
print ("""
          ___  ________________    ____  _________________
         / _ \ ___    ____ __ _   / _\ )__  ___  __    __ 
        / _/ // _ \  / __// / /  / _  / _ \/ _ \/  \  /  \ 
       /___ / \__/_\/_/  /_/\_\ /_/ \_\___/\___/_/\_\/_/\_\ \n
       server v 1.0 | Kristo

""")

# Server config

clients = {}
addresses = {}

config = configparser.RawConfigParser()
config.read(r'darkroom.conf')

HOST = config.get('config', 'HOST')
PORT = int(config.get('config', 'PORT'))
PASSWORD = config.get('config', 'PASSWORD')
key = bytes(PASSWORD, 'utf-8')
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDRESS)

# Encryption functions

def get_key(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())

def encrypt(password, token):
    try:
        f = Fernet(get_key(password))
        return f.encrypt(bytes(token))
    except InvalidToken:
        print("User entered wrong password")

def decrypt(password, token):
    try:
        f = Fernet(get_key(password))
        return f.decrypt(bytes(token))
    except InvalidToken:
        print("User entered wrong password")

# Accepting connections

def accept_incoming_connections():
    # Sets up handling for incoming clients
    while True:
        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)
        client.send(encrypt(key, b"You have entered the DarkRoom. Enter your alias."))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

# Handles new client

def handle_client(client): # Takes client socket as argument
    # Handles a single client connection
    name = client.recv(BUFFER_SIZE)
    name = decrypt(key, name)
    welcome = b'Welcome, %s. If you want to quit, type !quit to exit.' % name
    client.send(encrypt(key, welcome))
    msg = b"%s has joined the DarkRoom." % name
    broadcast(encrypt(key, msg))
    clients[client] = name

    while True:
        msg = client.recv(BUFFER_SIZE)
        msg = decrypt(key, msg)
        if msg != b"!quit":
            broadcast(encrypt(key, bytes(name + b": " + msg)))
        else:
            client.send(encrypt(key, b"!quit"))
            print("%s:%s has disconnected." % addresses[client])
            client.close()
            del clients[client]
            broadcast(encrypt(key, b"%s has left the DarkRoom." % name))
            break

# Broadcasts message to all users

def broadcast(msg):
    for sock in clients:
        sock.send(msg)

# Start server and listen for incoming connections

if __name__ == "__main__":
    server.listen(30)
    print("Server listening on port " + str(PORT) + "....")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    try:
        ACCEPT_THREAD.start() # Starts the infinite loop.
        ACCEPT_THREAD.join()
    except (KeyboardInterrupt, SystemExit):
        server.close()
        sys.exit()
