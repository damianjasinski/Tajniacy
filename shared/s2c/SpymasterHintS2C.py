from shared.Packet import Packet


class SpymasterHintS2C(Packet):
    def __init__(self, cardText, number):
        self.cardText = cardText
        self.number = number
