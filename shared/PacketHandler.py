import socket


class PacketHandler():
    def __init__(self) -> None:
        self.handlers = {}

    def register(self, packet_type, func):
        self.handlers[hash(packet_type)] = func

    def handle(self, packet):
        self.handlers[hash(packet.__class__)](packet)

    def handleWithParam(self, packet, param):
        self.handleers[hash(packet.__class__)](packet, param)
