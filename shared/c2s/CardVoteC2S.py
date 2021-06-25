from shared.Packet import Packet


class CardVoteC2S(Packet):
    def __init__(self, cardText):
        self.cardText = cardText
