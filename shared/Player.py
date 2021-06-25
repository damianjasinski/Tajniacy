from shared.Team import Team


class Player():
    def __init__(self, name):
        self.name = name
        self.spymaster = False
        self.team = Team.NONE
