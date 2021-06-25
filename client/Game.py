from shared.Team import Team
from typing import List
from shared.Player import Player


class Game():
    def __init__(self, username: str):
        self.username = username
        self.spymaster = False
        self.team = Team.NONE
