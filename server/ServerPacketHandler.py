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

    def handleCardVote(self, data: CardVoteC2S, param):
        # TODO: Check if player is current playing team

        for card in self.game.cards:
            if card.text == data.cardText:
                if data.add:
                    card.votes.append(param.player.name)
                else:
                    card.votes.remove(param.player.name)

                self.sendToAll(CardVoteS2C(card.text, card.votes))

    def handleCardSelect(self, data: CardSelectC2S, param):
        # TODO: Check if player is current playing team

        for card in self.game.cards:
            if card.text == data.cardText:
                card.shown = True

                self.sendToAll(CardSelectS2C(card.text, card.color))
