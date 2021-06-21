from shared.Packet import Packet


class SwitchSpymasterC2S(Packet):
    def __init__(self, isSpymaster):
        self.isSpymaster = isSpymaster
