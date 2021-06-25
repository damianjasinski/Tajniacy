from server.ServerPacketHandler import ServerPacketHandler
from shared.Player import Player
from server.ClientHandler import ClientHandler
import socket
import threading

from server.Game import Game
from shared.PacketHandler import PacketHandler
from shared.c2s.HandshakeC2S import HandshakeC2S


class Server():
    def __init__(self, port):
        self.game = Game()
        self.clientHandlers = []

        self.packetHandler = ServerPacketHandler(self)

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(("", port))
        self.serverSocket.listen()
        print(f"Server started at port {port}")

    def run(self):
        print("Waiting for clients...")
        while True:
            clientSocket, address = self.serverSocket.accept()

            print(f"Connection from {address} hasd been established")

            clientHandler = ClientHandler(
                clientSocket, Player(""), self, self.packetHandler)
            clientHandler.start()

            self.clientHandlers.append(clientHandler)


def main():
    server = Server(3414)
    server.run()


main()
