from shared.Packet import Packet


class GameStartS2C(Packet):
    def __init__(self, words):
        self.words = words
