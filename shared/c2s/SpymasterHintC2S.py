from shared.Packet import Packet


class SpymasterHintC2S(Packet):
    def __init__(self, cardText, number):
        self.cardText = cardText
        self.number = number
