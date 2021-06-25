from shared.Packet import Packet


class TeamScoreS2C(Packet):
    def __init__(self, redTeamScore, blueTeamScore):
        self.redTeamScore = redTeamScore
        self.blueTeamScore = blueTeamScore
