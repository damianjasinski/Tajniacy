from shared.Packet import Packet


class ChooseTeamC2S(Packet):
    def __init__(self, team):
        self.team = team
