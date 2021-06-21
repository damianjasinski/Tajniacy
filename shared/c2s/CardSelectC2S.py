from shared.Packet import Packet


class CardSelectC2S(Packet):
    def __init__(self, cardText):
        self.cardText = cardText
