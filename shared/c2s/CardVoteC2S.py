from shared.Packet import Packet


class CardVoteC2S(Packet):
    def __init__(self, cardText, add: bool):
        self.cardText = cardText
        self.add = add
