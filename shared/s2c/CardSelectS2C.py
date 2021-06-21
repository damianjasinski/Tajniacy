from shared.Packet import Packet


class CardSelectS2C(Packet):
    def __init__(self, cardText, color):
        self.cardText = cardText
        self.color = color
