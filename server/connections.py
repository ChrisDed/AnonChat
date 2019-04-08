import sys
import configparser
from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM

from encryption import Encrypter

class ServerConnections:

    def __init__(self):
        self.clients = {}
        self.addresses = {}

        config = configparser.RawConfigParser()
        config.read(r'anonchat.conf')
        HOST = config.get('config', 'HOST')
        self.PORT = int(config.get('config', 'PORT'))
        PASSWORD = config.get('config', 'PASSWORD')

        self.key = bytes(PASSWORD, 'utf-8')
        self.BUFFER_SIZE = 1024
        self.ADDRESS = (HOST, self.PORT)

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(self.ADDRESS)

        self.mainloop()
        self.accept_incoming_connections()

    # Accepting connections

    def accept_incoming_connections(self):
        # Sets up handling for incoming clients
        while True:
            client, client_address = self.server.accept()
            print("%s:%s has connected." % client_address)
            client.send(Encrypter.encrypt(self.key, b"You have entered AnonChat. Enter your alias."))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    # Start server and listen for incoming connections

    def mainloop(self):
        self.server.listen(10)
        print("Server listening on port " + str(self.PORT) + "....")
        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        try:
            ACCEPT_THREAD.start() # Starts the infinite loop.
            ACCEPT_THREAD.join()
        except (KeyboardInterrupt, SystemExit):
            self.server.close()
            sys.exit()


    def handle_client(self, client): # Takes client socket as argument
        # Handles a single client connection
        name = client.recv(self.BUFFER_SIZE)
        name = Encrypter.decrypt(self.key, name)
        welcome = b'Welcome, %s. If you want to quit, type !quit to exit.' % name
        client.send(Encrypter.encrypt(self.key, welcome))
        msg = b"%s has joined AnonChat." % name
        self.broadcast(Encrypter.encrypt(self.key, msg))
        self.clients[client] = name

        while True:
            msg = client.recv(self.BUFFER_SIZE)
            msg = Encrypter.decrypt(self.key, msg)
            if msg != b"!quit":
                self.broadcast(Encrypter.encrypt(self.key, bytes(name + b": " + msg)))
            else:
                client.send(Encrypter.encrypt(self.key, b"!quit"))
                print("%s:%s has disconnected." % addresses[client])
                client.close()
                del clients[client]
                self.broadcast(Encrypter.encrypt(self.key, b"%s has left the AnonChat." % name))
                break

    # Broadcasts message to all users

    def broadcast(self, msg):
        for sock in self.clients:
            sock.send(msg)

