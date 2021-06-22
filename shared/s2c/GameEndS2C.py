from shared.Packet import Packet
from shared.Team import Team


class GameEndS2C(Packet):
    def __init__(self, winningTeam: Team):
        self.winningTeam = winningTeam
