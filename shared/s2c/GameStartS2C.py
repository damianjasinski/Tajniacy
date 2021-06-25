from shared.CardColor import CardColor
from typing import List
from shared.Packet import Packet


class GameStartS2C(Packet):
    def __init__(self, words: List[str]):
        self.words = words
