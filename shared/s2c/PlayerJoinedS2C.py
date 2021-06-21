from shared.Packet import Packet


class PlayerJoinedS2C(Packet):
    def __init__(self, player):
        self.player = player
