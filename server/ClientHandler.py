from shared.synchronized import synchronized
import threading
import pickle
from socket import socket

from server.ServerPacketHandler import ServerPacketHandler
from shared.Player import Player


class ClientHandler(threading.Thread):
    def __init__(self, socket: socket, player: Player, packetHandler: ServerPacketHandler):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.socket = socket
        self.player = player
        self.packetHandler = packetHandler

    @synchronized
    def send(self, data):
        self.socket.send(pickle.dumps(data))

    def run(self):
        while True:
            buff = self.socket.recv(1024)

            data = pickle.loads(buff)

            print(self, data)

            self.packetHandler.handle(data, self)
