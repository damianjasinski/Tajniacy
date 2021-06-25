from shared.CardColor import CardColor
from shared.SharedCard import SharedCard
import sys
import os
import threading
import random
from typing import List
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import (QFont, QFontMetrics, QPixmap,
                         QPainter, QBrush, QPen, QColor, QPainterPath, QIcon)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet


class Card(QFrame):
    def __init__(self, cardsWidget, text):
        super().__init__()

        self.text = text
        self.color = "default"
        self.isRevealed = False
        self.isSpymasterView = False

        self.setObjectName("Card")

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.setMinimumSize(170, 100)

        self.wordUsed = QLabel(str(text).upper())
        self.wordUsed.setAlignment(Qt.AlignCenter)
        self.wordUsed.setStyleSheet(
            "background-color:white; font-family: 'Berlin Sans FB'; font-size:17px; color: black")

        self.voteBtn = QPushButton("Vote", clicked=lambda: cardsWidget._onVote(text))
        self.voteBtn.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:12px;border-radius:10px;")
        self.chooseBtn = QPushButton("Choose", clicked=lambda: cardsWidget._onSelect(text))
        self.chooseBtn.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:12px;border-radius:10px;")

        # vote counter
        self.votesLabel = QLabel("")
        self.votesLabel.setStyleSheet("font-family:Berlin Sans FB; font-size:20px; color: black")
        self.votesLabel.setAlignment(Qt.AlignHCenter)

        # self.mainLayout.addWidget(self.votesLabel, 0, 1, 1, 2)
        self.mainLayout.addWidget(self.wordUsed, 1, 1, 2, 2)
        self.mainLayout.addWidget(self.voteBtn, 3, 1, 1, 1)
        self.mainLayout.addWidget(self.chooseBtn, 3, 2, 1, 1)

        self.setStyleSheet(
            "#Card {background-image: url(resources/" + self.color + "Card.png)}")

    # method to set votes on card
    def setVotes(self, votes):
        self.votesLabel.setText(f"{votes}")

    def setColor(self, color):
        self.color = color

    def revealColor(self):
        self.isRevealed = True
        self.setStyleSheet(
            "background-image: url(resources/" + self.color + "Card.png)")
        self.mainLayout.itemAt(0).widget().deleteLater()

        if self.isSpymasterView == False:
            self.mainLayout.itemAt(1).widget().deleteLater()
            self.mainLayout.itemAt(2).widget().deleteLater()

    def spyMasterView(self):
        self.isSpymasterView = True
        self.setStyleSheet(
            "#Card {background-image: url(resources/" + self.color + "Card.png)}")
        self.wordUsed.setMaximumSize(100, 30)
        self.mainLayout.itemAt(1).widget().deleteLater()
        self.mainLayout.itemAt(2).widget().deleteLater()
        self.mainLayout.addWidget(self.wordUsed, 1, 1, 1, 1)


class CardsWidget(QWidget):
    onVote = pyqtSignal(str)
    onSelect = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.cardList = []

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.setMinimumSize(500, 500)

    def addCards(self, cards: List[SharedCard]):
        for row in range(5):
            for column in range(5):
                sharedCard = cards[row + 5 * column]
                card = Card(self, sharedCard.name)

                card.setColor(sharedCard.color.name.lower())

                self.cardList.append(card)
                self.mainLayout.addWidget(card, row + 1, column + 1, 1, 1)

    def revealCard(self, text: str, color: CardColor):
        for card in self.cardList:
            if card.text == text:
                card.setColor(color.name.lower())
                card.revealColor()
                break

    # hide vote and choose buttons
    def hideButtons(self):
        for card in self.cardList:
            if card.isRevealed == False:
                card.voteBtn.hide()
                card.chooseBtn.hide()

    # show vote and choose buttons
    def showButtons(self):
        for card in self.cardList:
            if card.isRevealed == False:
                card.voteBtn.show()
                card.chooseBtn.show()

    # use this to get spyMaster view of board
    def showSpymasterView(self):
        for card in self.cardList:
            card.spyMasterView()

    def _onVote(self, text: str):
        self.onVote.emit(text)

    def _onSelect(self, text: str):
        self.onSelect.emit(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogi = CardsWidget()
    dialogi.show()
    sys.exit(app.exec_())
