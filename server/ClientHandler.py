import pickle
import threading
from socket import socket

from shared.Player import Player
from shared.synchronized import synchronized

from server.Server import Server
from server.ServerPacketHandler import ServerPacketHandler


class ClientHandler(threading.Thread):
    def __init__(self, socket: socket, player: Player, server: Server, packetHandler: ServerPacketHandler):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.socket = socket
        self.player = player
        self.server = server
        self.packetHandler = packetHandler

    @synchronized
    def send(self, data):
        self.socket.send(pickle.dumps(data))

    def run(self):
        try:
            while True:
                buff = self.socket.recv(1024)

                data = pickle.loads(buff)

                print(self, data)

                self.packetHandler.handle(data, self)
        except IOError:
            print("exception")

        print("Disconnected")
        self.server.game.removePlayer(self.player)
