from shared.Packet import Packet
from shared.Team import Team


class SwitchPlayingSideS2C(Packet):
    def __init__(self, side: Team, spymaster: bool):
        self.side = side
        self.spymaster = spymaster
