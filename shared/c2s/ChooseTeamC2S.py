from shared.Packet import Packet
from shared.Team import Team


class ChooseTeamC2S(Packet):
    def __init__(self, team: Team, spymaster: bool):
        self.team = team
        self.spymaster = spymaster
