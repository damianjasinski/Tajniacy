import pickle
import threading
from socket import socket

from shared.Player import Player
from shared.synchronized import synchronized


class ClientHandler(threading.Thread):
    def __init__(self, socket: socket, player: Player, server, packetHandler):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.socket = socket
        self.player = player
        self.server = server
        self.packetHandler = packetHandler

    @synchronized
    def send(self, data):
        self.socket.sendall(pickle.dumps(data))

    def run(self):
        try:
            while True:
                buff = self.socket.recv(1024)

                data = pickle.loads(buff)

                print(self, data)

                self.packetHandler.handle(data, self)
        except IOError as err:
            print(err)

        print("Disconnected")
        self.server.game.removePlayer(self.player)
        self.server.clientHandlers.remove(self)
