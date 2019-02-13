import sys
from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM

from encryption import ClientEncryption
from gui import ClientGUI

class ClientConnections:

    def __init__(self):
        HOST = '127.0.0.1'
        PORT = 33000
        PASSWORD = sys.argv[1]
        self.key = bytes(PASSWORD, 'utf-8')
        self.BUFFER_SIZE = 1024
        self.ADDRESS = (HOST, PORT)
        self.GUI = ClientGUI(self)
        self.Encryption = ClientEncryption()
        self.threading()
        

    def threading(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDRESS)
        receive_thread = Thread(target=self.receive)
        try:
            receive_thread.start()
            self.GUI.mainloop() # Starts GUI execution.
            receive_thread.join()
        except (KeyboardInterrupt, SystemExit):
            self.GUI.top.quit()
            sys.exit()


    def receive(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFFER_SIZE)
                decryptedMsg = self.Encryption.decrypt(self.key, msg)
                self.GUI.insert_message(decryptedMsg)
            except OSError:  # Possibly client has left the chat.
                break

    
    def send(self, event=None):  # event is passed by binders.
        msg = self.GUI.get_message()
        self.GUI.set_message("")  # Clears input field.
        self.client_socket.send(self.Encryption.encrypt(self.key, bytes(msg, 'utf-8')))
        if msg == "!quit":
            self.client_socket.close()
            self.GUI.top.after(100, self.GUI.top.quit)
            sys.exit()


    def on_closing(event=None):
        self.GUI.set_message("!quit")
        self.send()

