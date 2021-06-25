from shared.c2s.CardSelectC2S import CardSelectC2S
from shared.c2s.CardVoteC2S import CardVoteC2S
from shared.c2s.SpymasterHintC2S import SpymasterHintC2S
from client.Game import Game
from shared.c2s.GameStartC2S import GameStartC2S
from shared.c2s.ChooseTeamC2S import ChooseTeamC2S
from shared.Team import Team
from shared.c2s.HandshakeC2S import HandshakeC2S
import sys
import os
import threading
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QIcon, QPainter, QPainterPath, QPen, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from client.TeamWidget import TeamWidget
from client.CardsWidget import CardsWidget
from qt_material import apply_stylesheet


class MainWindow(QMainWindow):
    def __init__(self, username: str, netClient):
        super().__init__()

        self.game = Game(username)

        self.netClient = netClient
        self.netClient.setMainWindow(self)
        self.netClient.sendData(HandshakeC2S(username))

        self.setMinimumSize(1366, 768)
        self.setMaximumSize(1920, 1080)
        self.setWindowTitle("Tajniacy")
        self.cardsWidget = None

        # Layouts set
        # The main layout
        mainLayout = QVBoxLayout()
        # Layout with teams and cards
        self.playLayout = QHBoxLayout()
        # cardsWidget layout
        self.cardsLayout = QHBoxLayout()
        # Spymaster assets layout
        bottomLayout = QHBoxLayout()
        # Button layout
        buttonLayout = QHBoxLayout()

        # setCentralWidget
        mainWidget = QWidget()
        mainWidget.setObjectName("mainWidget")
        self.setCentralWidget(mainWidget)
        mainWidget.setLayout(mainLayout)

        # set background based on which team should move
        self.setBackgroundImage("none")

        # Title Label
        self.titleLabel = QLabel("Tajniacy!")
        self.titleLabel.setStyleSheet(
            "font-family: 'Berlin Sans FB'; font-size:80px; cursive; color: hsl(50, 80%, 50%);")
        self.titleLabel.setAlignment(Qt.AlignHCenter)
        mainLayout.addStretch(4)
        mainLayout.addWidget(self.titleLabel)

        # Play (main window for cards and teams) layout set
        mainLayout.addStretch(1)
        mainLayout.addLayout(self.playLayout)
        mainLayout.addStretch(5)
        mainLayout.addLayout(bottomLayout)
        self.playLayout.setAlignment(Qt.AlignVCenter)

        # TeamRed
        self.teamRed = TeamWidget("red")
        self.teamRed.onJoinPlayer.connect(lambda: self.onPlayerSwitchTeam(Team.RED, False))
        self.teamRed.onJoinSpymaster.connect(lambda: self.onPlayerSwitchTeam(Team.RED, True))
        self.playLayout.addWidget(self.teamRed, 1)
        self.playLayout.addWidget(
            QLabel("                                                                 "))

        # add cardsLayout to play Layout
        self.playLayout.addLayout(self.cardsLayout, 5)

        # StartGame button, cards will show up after button is clicked
        self.startGameBtn = QPushButton(
            "Start Game", clicked=self.onStartGameClicked)
        self.startGameBtn.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:35px;border-radius:10px;")
        self.startGameBtn.setMaximumSize(550, 50)
        self.cardsLayout.addWidget(self.startGameBtn)

        # TeamBlue
        self.playLayout.addWidget(
            QLabel("                                                                 "))
        self.teamBlue = TeamWidget("blue")
        self.teamBlue.onJoinPlayer.connect(lambda: self.onPlayerSwitchTeam(Team.BLUE, False))
        self.teamBlue.onJoinSpymaster.connect(lambda: self.onPlayerSwitchTeam(Team.BLUE, True))
        self.playLayout.addWidget(self.teamBlue, 1)

        # bottomLayout
        bottomLayout.setAlignment(Qt.AlignHCenter)
        bottomLayout.addWidget(QLabel(""), 3)
        self.spymasterInput = QLineEdit()
        self.spymasterInput.setAlignment(Qt.AlignCenter)
        self.spymasterInput.setPlaceholderText(
            "Podaj slowo opisujace karty oraz wybierz ilosc kart do odgadniecia")
        self.spymasterInput.setFocus(False)
        self.spymasterInput.hide()
        self.spymasterInput.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:18px;")
        self.numberOfCards = QComboBox()
        self.numberOfCards.hide()
        self.numberOfCards.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:18px;")
        for i in range(8):
            self.numberOfCards.addItem(str(i+1))
        bottomLayout.addWidget(self.spymasterInput, 2)
        bottomLayout.addWidget(self.numberOfCards)
        bottomLayout.addWidget(QLabel(""), 3)
        # button
        mainLayout.addLayout(buttonLayout)
        buttonLayout.setAlignment(Qt.AlignHCenter)
        self.spymasterButton = QPushButton("Zatwierdz", clicked=self.onSpymasterButtonClick)
        self.spymasterButton.hide()
        self.spymasterButton.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:18px; border-radius:10px;")
        self.spymasterButton.setMinimumSize(150, 50)
        buttonLayout.addWidget(self.spymasterButton)

        # spymaster tip
        self.spyTipLabel = QLabel("")
        self.spyTipLabel.setMinimumSize(115, 30)
        self.spyTipLabel.setAlignment(Qt.AlignCenter)
        self.spyTipLabel.setStyleSheet(
            "background-color:white; font-family: 'Berlin Sans FB'; font-size:19px; color : black")
        self.spyTipLabel.hide()

        # spymaster cards number
        self.spyCardNumber = QLabel("")
        self.spyCardNumber.setMinimumSize(25, 30)
        self.spyCardNumber.setAlignment(Qt.AlignCenter)
        self.spyCardNumber.setStyleSheet(
            "background-color:white; font-family: 'Berlin Sans FB'; font-size:19px; color : black")
        self.spyCardNumber.hide()

        buttonLayout.addWidget(self.spyTipLabel)
        buttonLayout.addWidget(self.spyCardNumber)
        mainLayout.addStretch(8)

    def onStartGameClicked(self):
        self.netClient.sendData(GameStartC2S())

    def onPlayerSwitchTeam(self, team: Team, spymaster: bool):
        self.netClient.sendData(ChooseTeamC2S(team, spymaster))

    def onSpymasterButtonClick(self):
        self.netClient.sendData(
            SpymasterHintC2S(
                self.spymasterInput.text(),
                int(self.numberOfCards.currentText())))

    def setSpymasterTipLabels(self, word, number):
        self.spyTipLabel.setText(str(word).upper())
        self.spyCardNumber.setText(str(number))

    def hideSpymasterTipLabels(self):
        self.spyTipLabel.hide()
        self.spyCardNumber.hide()

    def showSpymasterTipLabels(self):
        self.spyTipLabel.show()
        self.spyCardNumber.show()

    def hideSpymasterFields(self):
        self.spymasterButton.hide()
        self.spymasterInput.hide()
        self.numberOfCards.hide()

    def showSpymasterFields(self):
        self.spymasterButton.show()
        self.spymasterInput.show()
        self.numberOfCards.show()

    def setTitle(self, color):
        self.titleLabel.setText(f"{color} team wins!")
        self.titleLabel.setStyleSheet(
            "font-family: 'Berlin Sans FB'; font-size:80px; cursive; color: "+color+"; ")

    def showCardsBtn(self):
        try:
            self.cardsWidget.showButtons()
        except AttributeError:
            print("Game is not yet started")

    def hideCardsBtn(self):
        try:
            self.cardsWidget.hideButtons()
        except AttributeError:
            print("Game is not yet started")

    def showCardsWidget(self):
        self.cardsWidget = CardsWidget()
        self.cardsWidget.onVote.connect(self.onCardVote)
        self.cardsWidget.onSelect.connect(self.onCardSelect)

        self.cardsLayout.itemAt(0).widget().deleteLater()
        self.cardsLayout.addWidget(self.cardsWidget)
        self.playLayout.itemAt(1).widget().deleteLater()
        self.playLayout.itemAt(3).widget().deleteLater()

    def onCardVote(self, text: str):
        self.netClient.sendData(CardVoteC2S(text))

    def onCardSelect(self, text: str):
        self.netClient.sendData(CardSelectC2S(text))

    # can be called to show which team should move
    def setBackgroundImage(self, teamColor):
        if teamColor == 'blue':
            self.setStyleSheet(
                "QWidget#mainWidget { background-image: url(resources/backgroundBlue.png);"
                "background-repeat: no-repeat ;"
                "background-position: center}")
        elif teamColor == 'red':
            self.setStyleSheet(
                "QWidget#mainWidget { background-image: url(resources/backgroundRed.png);"
                "background-repeat: no-repeat ;"
                "background-position: center}")
        else:
            self.setStyleSheet(
                "QWidget#mainWidget { background-image: url(resources/backgroundNeutral.png);"
                "background-repeat: no-repeat ;"
                "background-position: center}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogi = MainWindow("user")
    dialogi.show()
    apply_stylesheet(app, theme='dark_amber.xml')
    sys.exit(app.exec_())
