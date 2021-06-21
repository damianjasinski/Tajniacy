from shared.Packet import Packet


class HandshakeS2C(Packet):
    def __init__(self, players):
        self.players = players
