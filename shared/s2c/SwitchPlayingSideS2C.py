from shared.Packet import Packet
from shared.Team import Team


class SwitchPlayingSideS2C(Packet):
    def __init__(self, side: Team, spyMaster: bool):
        self.side = side
        self.spyMaster = spyMaster
