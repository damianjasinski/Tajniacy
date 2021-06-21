from shared.synchronized import synchronized
from shared.PacketHandler import PacketHandler
from shared.c2s.HandshakeC2S import HandshakeC2S
from server.ClientHandler import ClientHandler


class ServerPacketHandler():

    def __init__(self, server):
        self.server = server
        self.packetHandler = PacketHandler()
        self.packetHandler.register(HandshakeC2S, self.handleHandshake)

    @synchronized
    def handle(self, packet, param):
        self.packetHandler.handleWithParam(packet, param)

    def handleHandshake(self, data: HandshakeC2S, param: ClientHandler):
        param.player.name = data.name

        for handler in self.server.clientHandlers:
            if handler is not param:
