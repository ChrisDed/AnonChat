# DarkRoom - Anonymous, Encrypted, Multithreaded Python Chat Application

# Client side code

from connections import ClientConnections
import sys

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Usage: python3 client.py <server password>")
        sys.exit()
    
    ClientConnections()

