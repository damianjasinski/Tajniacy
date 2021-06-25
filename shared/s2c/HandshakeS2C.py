from typing import List
from shared.Packet import Packet
from shared.Player import Player


class HandshakeS2C(Packet):
    def __init__(self, players: List[Player]):
        self.players = players
