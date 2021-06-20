import socket
import threading

from shared.PacketHandler import PacketHandler
from shared.c2s.HandshakeC2S import HandshakeC2S

class Server():
    def __init__(self, port):

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((socket.gethostname(), 4123))
        self.serverSocket.listen(8)

    def run(self):
        while True:
            clientSocket, address = self.serverSocket.accept()
            print(f"Connection from {address} hasd been established")


def handleAsdf(packet: HandshakeC2S):
    print(f"HandshakeC2S: {packet.name}")


def main():
    # server = Server()
    handler = PacketHandler()
    handler.register(HandshakeC2S, handleAsdf)
    handler.handle(HandshakeC2S("asdf"))
    
main()
