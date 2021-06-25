from shared.Player import Player
from shared.Packet import Packet


class PlayerJoinedS2C(Packet):
    def __init__(self, player: Player):
        self.player = player
