import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QPainter, QPainterPath, QPen
from PyQt5.QtCore import Qt, pyqtSignal


class TeamWidget(QWidget):
    onJoinSpymaster = pyqtSignal()
    onJoinPlayer = pyqtSignal()

    def __init__(self, color):
        super().__init__()
        self.playerList = []
        if color == 'red' or color == 'Red':
            self._color = "rgba(255, 30, 30, 95)"
        elif color == 'blue' or color == 'Blue':
            self._color = "rgba(33,79,198, 125)"

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.setMinimumSize(120,60)

        self.scoreLabel = QLabel("")
        self.scoreLabel.setStyleSheet("font-family:Berlin Sans FB; font-size:28px;")
        self.scoreLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.scoreLabel)

        # Spymasters table
        self.spylistWidget = QListWidget()
        self.spylistWidget.setParent(self)
        self.spylistWidget.setEnabled(False)
        self.spylistWidget.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:18px; border-radius:10px; Background-color:  " +
            self._color + ";"
            "border: 0px solid " + color)

        # Button join as spymaster
        self.spyButton = QPushButton(
            "Join as spymaster", clicked=lambda: self.onJoinSpymaster.emit())
        self.spyButton.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:14px; border-radius:10px;")
        mainLayout.addWidget(self.spyButton)

        mainLayout.addWidget(self.spylistWidget, 1)

        # Players table
        self.playlistWidget = QListWidget()
        self.playlistWidget.setEnabled(False)
        self.playlistWidget.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:18px; border-radius:10px; Background-color: " +
            self._color + ";"
            "border: 0px solid " + color)
        # button join as player
        self.playerButton = QPushButton("Join as player", clicked=lambda: self.onJoinPlayer.emit())
        self.playerButton.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:14px;  border-radius:10px;")
        mainLayout.addWidget(self.playerButton)

        mainLayout.addWidget(self.playlistWidget, 5)

    def addSpymaster(self, playerName):
        self.spylistWidget.addItem(playerName)
        print(f"Added {playerName} to the player list")
        self.playerList.append(playerName)

    def removeSpymaster(self, playerName):
        items_list = self.spylistWidget.findItems(playerName, QtCore.Qt.MatchExactly)
        try:
            self.playerList.remove(playerName)
        except:
            print(f"Trying to remove player {playerName} but its not in the list")
        for item in items_list:
            r = self.spylistWidget.row(item)
            self.spylistWidget.takeItem(r)

    def addPlayer(self, playerName):
        self.playerList.append(playerName)
        print(f"Added {playerName} to the player list")
        self.playlistWidget.addItem(playerName)
        for item in self.playerList:
            print(item)

    def removePlayer(self, playerName):
        items_list = self.playlistWidget.findItems(playerName, QtCore.Qt.MatchExactly)
        try:
            self.playerList.remove(playerName)
        except:
            print(f"Trying to remove player {playerName} but its not in the list")
        for item in items_list:
            r = self.playlistWidget.row(item)
            self.playlistWidget.takeItem(r)

    def isPlayerListEmpty(self):
        if not self.playerList:
            return True
        return False

    # in order to hide buttons from both teams you need to call this method from both instantions.
    def hideJoinBtns(self):
        self.playerButton.hide()
        self.spyButton.hide()

    def showJoinBtns(self):
        self.playerButton.show()
        self.addSpymaster.show()

    def setPoints(self, points):
        self.scoreLabel.setText(f"{points}")

    # def paintEvent(self, event):
    #     self.text = None
    #     if self._color == "red":
    #         self.text = "Red"
    #     elif self._color == "blue":
    #         self.text = "Blue"

    #     self.font = QFont("Trebuchet MS", 40)
    #     metrics = QFontMetrics(self.font)
    #     painter = QPainter(self)
    #     path = QPainterPath()
    #     pen = QPen(Qt.white)
    #     len = metrics.width(self.text)
    #     w = self.width()
    #     px = (len - w) / 2
    #     if px < 0:
    #         px = -px
    #         py = (self.height() - metrics.height()) / 2 + metrics.ascent()
    #     if py < 0:
    #         py = -py
    #     pen.setWidth(2)
    #     path.addText(px, py, self.font, self.text)  # Add the path to draw the font to the path
    #     painter.setRenderHint(QPainter.Antialiasing)  # Turn on anti-aliasing, otherwise it looks ugly
    #     painter.strokePath(path, pen)  # Generate path
    #     painter.drawPath(path)  # Draw path

    #     if self._color == "red":
    #         painter.fillPath(path, QBrush(QColor(255, 100, 100)))  # Fill the path, where QBrush can set the fill color
        # elif self._color == "blue":
        # painter.fillPath(path, QBrush(QColor(100, 128, 255)))  # Fill the path, where QBrush can set the fill color


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialogi = TeamWidget()
#     dialogi.show()
#     sys.exit(app.exec_())
