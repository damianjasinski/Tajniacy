from client.SoundManager import SoundManager
from client.CardsWidget import CardsWidget
from client.TeamWidget import TeamWidget
import pickle
from shared.Player import Player

from PyQt5.QtCore import QObject
from shared.c2s.CardSelectC2S import CardSelectC2S
from shared.c2s.CardVoteC2S import CardVoteC2S
from shared.c2s.ChooseTeamC2S import ChooseTeamC2S
from shared.c2s.GameStartC2S import GameStartC2S
from shared.c2s.HandshakeC2S import HandshakeC2S
from shared.c2s.SpymasterHintC2S import SpymasterHintC2S
from shared.CardColor import CardColor
from shared.PacketHandler import PacketHandler
from shared.s2c.CardSelectS2C import CardSelectS2C
from shared.s2c.CardVoteS2C import CardVoteS2C
from shared.s2c.ChooseTeamS2C import ChooseTeamS2C
from shared.s2c.GameEndS2C import GameEndS2C
from shared.s2c.GameStartS2C import GameStartS2C
from shared.s2c.HandshakeS2C import HandshakeS2C
from shared.s2c.PlayerJoinedS2C import PlayerJoinedS2C
from shared.s2c.SpymasterHintS2C import SpymasterHintS2C
from shared.s2c.SwitchPlayingSideS2C import SwitchPlayingSideS2C
from shared.s2c.TeamScoreS2C import TeamScoreS2C
from shared.Team import Team
from client.GUI import MainWindow


class ClientPacketHandler(QObject):
    def __init__(self, netClient):
        QObject.__init__(self)

        self.soundManager = SoundManager((
            "fail",
            "message",
            "music",
            "reveal",
            "start",
            "vote",
            "win"
        ))

        self.soundManager.loop_sound("music")

        netClient.onPacketReceive.connect(self.onPacket)

        self.packetHandler = PacketHandler()
        self.packetHandler.register(CardSelectS2C, self.handleCardSelect)
        self.packetHandler.register(CardVoteS2C, self.handleCardVote)
        self.packetHandler.register(ChooseTeamS2C, self.handleChooseTeam)
        self.packetHandler.register(GameEndS2C, self.handleGameEnd)
        self.packetHandler.register(GameStartS2C, self.handleGameStart)
        self.packetHandler.register(HandshakeS2C, self.handleHandshake)
        self.packetHandler.register(PlayerJoinedS2C, self.handlePlayerJoined)
        self.packetHandler.register(SpymasterHintS2C, self.handleSpymasterHint)
        self.packetHandler.register(
            SwitchPlayingSideS2C, self.handleSwitchPlayingSide)
        self.packetHandler.register(TeamScoreS2C, self.handleTeamScore)

    def onPacket(self, buff):
        data = pickle.loads(buff)
        print(data)
        self.packetHandler.handle(data)

    def setMainWindow(self, mainWindow: MainWindow):
        self.mainWindow = mainWindow
        self.game = self.mainWindow.game

    def addPlayerToTeam(self, name: str, spymaster: bool, teamWidget: TeamWidget):
        if spymaster:
            teamWidget.addSpymaster(name)
        else:
            teamWidget.addPlayer(name)
        self.soundManager.play_sound("vote")

    def handleHandshake(self, data: HandshakeS2C):
        for player in data.players:
            if player.team == Team.RED:
                self.addPlayerToTeam(player.name, player.spymaster, self.mainWindow.teamRed)
            elif player.team == Team.BLUE:
                self.addPlayerToTeam(player.name, player.spymaster, self.mainWindow.teamBlue)

    def handlePlayerJoined(self, data: PlayerJoinedS2C):
        if data.player.team == Team.RED:
            self.addPlayerToTeam(data.player, self.mainWindow.teamRed)
        elif data.player.team == Team.BLUE:
            self.addPlayerToTeam(data.player, self.mainWindow.teamBlue)

    def handleChooseTeam(self, data: ChooseTeamS2C):
        self.mainWindow.teamRed.removePlayer(data.playerName)
        self.mainWindow.teamRed.removeSpymaster(data.playerName)

        self.mainWindow.teamBlue.removePlayer(data.playerName)
        self.mainWindow.teamBlue.removeSpymaster(data.playerName)

        if data.team == Team.RED:
            self.addPlayerToTeam(data.playerName, data.spymaster, self.mainWindow.teamRed)
        elif data.team == Team.BLUE:
            self.addPlayerToTeam(data.playerName, data.spymaster, self.mainWindow.teamBlue)

        if self.game.username == data.playerName:
            print("Ja: ", data.playerName, data.team, data.spymaster)
            self.game.team = data.team
            self.game.spymaster = data.spymaster

    def handleGameStart(self, data: GameStartS2C):
        self.mainWindow.showCardsWidget()
        self.mainWindow.teamRed.hideJoinBtns()
        self.mainWindow.teamBlue.hideJoinBtns()

        self.mainWindow.cardsWidget.addCards(data.cards)
        self.mainWindow.hideCardsBtn()
        self.mainWindow.hideSkipButton()

        if data.spymaster:
            self.mainWindow.cardsWidget.showSpymasterView()
        self.soundManager.play_sound("start")

    def handleSwitchPlayingSide(self, data: SwitchPlayingSideS2C):
        self.mainWindow.setBackgroundImage(data.side.name.lower())
        self.mainWindow.hideSpymasterTipLabels()

        # reset votes
        for card in self.mainWindow.cardsWidget.cardList:
            card.setVotes(0)

        if self.game.spymaster:
            if self.game.team == data.side and data.spymaster == True:
                self.mainWindow.showSpymasterFields()
            else:
                self.mainWindow.hideSpymasterFields()
        else:
            if self.game.team == data.side and data.spymaster == False:
                self.mainWindow.showCardsBtn()
                self.mainWindow.showSkipButton()
            else:
                self.mainWindow.hideCardsBtn()
                self.mainWindow.hideSkipButton()

    def handleCardSelect(self, data: CardSelectS2C):
        self.mainWindow.cardsWidget.revealCard(data.cardText, data.color)
        self.soundManager.play_sound("reveal")

    def handleCardVote(self, data: CardVoteS2C):
        card = self.mainWindow.cardsWidget.findCard(data.cardText)

        if card != None:
            card.setVotes(len(data.votes))
            self.soundManager.play_sound("vote")

    def handleSpymasterHint(self, data: SpymasterHintS2C):
        self.mainWindow.showSpymasterTipLabels()
        self.mainWindow.setSpymasterTipLabels(data.hint, data.number)
        self.soundManager.play_sound("message")

    def handleTeamScore(self, data: TeamScoreS2C):
        self.mainWindow.teamRed.setPoints(data.redTeamScore)
        self.mainWindow.teamBlue.setPoints(data.blueTeamScore)

    def handleGameEnd(self, data: GameEndS2C):
        self.mainWindow.hideSpymasterTipLabels()

        if self.game.spymaster:
            self.mainWindow.hideSpymasterFields()
        else:
            self.mainWindow.hideCardsBtn()
            self.mainWindow.hideSkipButton()

        self.mainWindow.setTitle(data.winningTeam.name)

        if self.game.team == data.winningTeam:
            self.soundManager.play_sound("win")
        else:
            self.soundManager.play_sound("fail")
