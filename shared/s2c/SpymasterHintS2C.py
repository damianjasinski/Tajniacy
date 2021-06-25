from shared.Packet import Packet


class SpymasterHintS2C(Packet):
    def __init__(self, hint, number):
        self.hint = hint
        self.number = number
