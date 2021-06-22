from shared.s2c.SpymasterHintS2C import SpymasterHintS2C
from shared.c2s.SpymasterHintC2S import SpymasterHintC2S
from shared.s2c.GameEndS2C import GameEndS2C
from shared.s2c.SwitchPlayingSideS2C import SwitchPlayingSideS2C
from shared.s2c.TeamScoreS2C import TeamScoreS2C
from shared.CardColor import CardColor
from shared.Team import Team
from shared.s2c.CardSelectS2C import CardSelectS2C
from shared.c2s.CardSelectC2S import CardSelectC2S
from shared.c2s.CardVoteC2S import CardVoteC2S
from shared.c2s.ChooseTeamC2S import ChooseTeamC2S
from shared.c2s.GameStartC2S import GameStartC2S
from shared.c2s.HandshakeC2S import HandshakeC2S
from shared.c2s.SwitchSpymasterC2S import SwitchSpymasterC2S
from shared.PacketHandler import PacketHandler
from shared.s2c.CardVoteS2C import CardVoteS2C
from shared.s2c.ChooseTeamS2C import ChooseTeamS2C
from shared.s2c.GameStartS2C import GameStartS2C
from shared.s2c.HandshakeS2C import HandshakeS2C
from shared.s2c.PlayerJoinedS2C import PlayerJoinedS2C
from shared.s2c.SwitchSpymasterS2C import SwitchSpymasterS2C
from shared.synchronized import synchronized

from server.Game import Game


class ServerPacketHandler():

    def __init__(self, server):
        self.server = server
        self.game: Game = server.game
        self.packetHandler = PacketHandler()
        self.packetHandler.register(HandshakeC2S, self.handleHandshake)
        self.packetHandler.register(ChooseTeamC2S, self.handleChooseTeam)
        self.packetHandler.register(
            SwitchSpymasterC2S, self.handleSwitchSpymaster)
        self.packetHandler.register(GameStartC2S, self.handleGameStart)
        self.packetHandler.register(CardVoteC2S, self.handleCardVote)
        self.packetHandler.register(CardSelectC2S, self.handleCardSelect)
        self.packetHandler.register(SpymasterHintC2S, self.handleSpymasterHint)

    @synchronized
    def handle(self, packet, param):
        self.packetHandler.handleWithParam(packet, param)

    def sendToOthers(self, data, param):
        for handler in self.server.clientHandlers:
            if handler is not param:
                handler.send(data)

    def sendToAll(self, data):
        for handler in self.server.clientHandlers:
            handler.send(data)

    def countTeamScore(self, team: Team):
        cardColor = CardColor.NEUTRAL

        if team == Team.RED:
            cardColor = CardColor.RED
        elif team == Team.BLUE:
            cardColor = CardColor.BLUE

        score = 8

        for card in self.game.cards:
            if card.color == cardColor and card.shown:
                score -= 1

        return score

    def handleGameEnd(self, winningTeam: Team):
        # TODO: add logic for ending game

        self.sendToAll(GameEndS2C(winningTeam))

    def handleHandshake(self, data: HandshakeC2S, param):
        param.player.name = data.name

        param.send(HandshakeS2C(self.game.players))

        self.game.players.append(param.player)
        self.sendToOthers(PlayerJoinedS2C(param.player), param)

    def handleChooseTeam(self, data: ChooseTeamC2S, param):
        param.player.team = data.team
        param.player.spymaster = False
        self.sendToAll(ChooseTeamS2C(param.player.name, data.team))

    def handleSwitchSpymaster(self, data: SwitchSpymasterC2S, param):
        param.player.spymaster = data.isSpymaster
        self.sendToAll(SwitchSpymasterS2C(param.player.name, data.team))

    def handleGameStart(self, data: GameStartC2S, param):
        self.game.generateWords()
        words = map(lambda card: card.text, self.game.cards)

        self.sendToAll(GameStartS2C(words))
        self.sendToAll(SwitchPlayingSideS2C(Team.RED, True))

    def handleCardVote(self, data: CardVoteC2S, param):
        if param.player.team != self.game.currentTeam:
            return None

        for card in self.game.cards:
            if card.text == data.cardText:
                if data.add:
                    card.votes.append(param.player.name)
                else:
                    card.votes.remove(param.player.name)

                self.sendToAll(CardVoteS2C(card.text, card.votes))

    def handleCardSelect(self, data: CardSelectC2S, param):
        if param.player.team != self.game.currentTeam:
            return None

        for card in self.game.cards:
            if card.text == data.cardText:
                card.shown = True

                self.sendToAll(CardSelectS2C(card.text, card.color))

                redScore = self.countTeamScore(Team.RED)
                blueScore = self.countTeamScore(Team.BLUE)

                self.sendToAll(TeamScoreS2C(redScore, blueScore))

                self.game.cardToGuess -= 1

                if card.color == CardColor.BLACK:
                    winningTeam = Team.NONE

                    if self.game.currentTeam == Team.RED:
                        winningTeam = Team.BLUE
                    elif self.game.currentTeam == Team.BLUE:
                        winningTeam = Team.RED

                    self.handleGameEnd(winningTeam)
                elif redScore == 0:
                    self.handleGameEnd(Team.RED)
                elif blueScore == 0:
                    self.handleGameEnd(Team.BLUE)
                else:
                    if (card.color == CardColor.RED and self.game.currentTeam == Team.BLUE or
                        card.color == CardColor.BLUE and self.game.currentTeam == Team.RED or
                        card.color == CardColor.NEUTRAL or
                            self.game.cardToGuess == 0):

                        playingTeam = Team.NONE

                        if self.game.currentTeam == Team.RED:
                            playingTeam = Team.BLUE
                        elif self.game.currentTeam == Team.BLUE:
                            playingTeam = Team.RED

                        self.game.currentTeam = playingTeam

                        self.sendToAll(SwitchPlayingSideS2C(playingTeam, True))
                break

    def handleSpymasterHint(self, data: SpymasterHintC2S, param):
        self.game.cardToGuess = data.number + 1

        self.sendToAll(SwitchPlayingSideS2C(self.game.currentTeam, False))
        self.sendToAll(SpymasterHintS2C(data.cardText, data.number))
