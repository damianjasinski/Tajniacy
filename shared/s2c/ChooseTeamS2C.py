from shared.Packet import Packet


class ChooseTeamS2C(Packet):
    def __init__(self, playerName, team):
        self.playerName = playerName
        self.team = team
