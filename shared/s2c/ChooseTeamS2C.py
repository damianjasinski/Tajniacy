from shared.Team import Team
from shared.Packet import Packet


class ChooseTeamS2C(Packet):
    def __init__(self, playerName: str, team: Team, spymaster: bool):
        self.playerName = playerName
        self.team = team
        self.spymaster = spymaster
