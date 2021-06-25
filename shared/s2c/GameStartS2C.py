from shared.SharedCard import SharedCard
from shared.CardColor import CardColor
from typing import List
from shared.Packet import Packet


class GameStartS2C(Packet):
    def __init__(self, cards: List[SharedCard], spymaster: bool):
        self.cards = cards
        self.spymaster = spymaster
