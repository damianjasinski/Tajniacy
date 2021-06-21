from shared.Packet import Packet


class SwitchSpymasterS2C(Packet):
    def __init__(self, playerName, isSpymaster):
        self.playerName = playerName
        self.isSpymaster = isSpymaster
