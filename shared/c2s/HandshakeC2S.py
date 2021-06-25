from shared.Packet import Packet

class HandshakeC2S(Packet):
    def __init__(self, name):
        self.name = name
        