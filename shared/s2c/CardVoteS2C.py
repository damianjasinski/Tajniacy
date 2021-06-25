from typing import List
from shared.Packet import Packet


class CardVoteS2C(Packet):
    def __init__(self, cardText: str, votes: List[str]):
        self.cardText = cardText
        self.votes = votes
