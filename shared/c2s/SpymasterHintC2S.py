from shared.Packet import Packet


class SpymasterHintC2S(Packet):
    def __init__(self, hint: str, number: int):
        self.hint = hint
        self.number = number
