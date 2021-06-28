from shared.Team import Team
from shared.synchronized import synchronized
from server.Card import Card
from shared.CardColor import CardColor
from server.WordReader import WordReader
import random


class Game():
    def __init__(self):
        self.players = []
        self.cards = []
        self.currentTeam = Team.NONE
        self.cardToGuess = 0

    @synchronized
    def addPlayer(self, player):
        self.players.append(player)

    @synchronized
    def removePlayer(self, player):
        self.players.remove(player)

    def generateWords(self):
        print("Generating cards...")
        reader = WordReader()
        reader.read_file("words.txt")
        words = random.sample(reader.get_words(), k=25)

        tempCardList = []

        self.cards = list()
        for row in range(5):
            for column in range(5):
                card = Card(words[row + 5 * column])
                tempCardList.append(card)
                self.cards.append(card)

        # randomizing cards color
        for i in range(8):
            card = random.choice(tempCardList)
            card.color = CardColor.BLUE
            tempCardList.remove(card)
        for i in range(9):
            card = random.choice(tempCardList)
            card.color = CardColor.RED
            tempCardList.remove(card)
        for i in range(6):
            card = random.choice(tempCardList)
            card.color = CardColor.NEUTRAL
            tempCardList.remove(card)

        card = random.choice(tempCardList)
        card.color = CardColor.BLACK
        tempCardList.remove(card)

        print("Cards generated!")
