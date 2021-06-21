from shared.Packet import Packet


class CardVoteS2C(Packet):
    def __init__(self, cardText, votes):
        self.cardText = cardText
        self.votes = votes
