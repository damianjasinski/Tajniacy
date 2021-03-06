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
        self.voteCounter = QProgressBar()
        self.voteCounter.setRange(0, 8)
        self.voteCounter.setMinimumSize(160, 20)
        self.voteCounter.setMaximumSize(160, 20)

        self.voteCounter.setStyleSheet("QProgressBar"
                                       "{"
                                       "background-color:rgba(0,0,0,50);"
                                       "}"
                                       "QProgressBar::chunk "
                                       "{ background-color:rgba(255,255,255,130);"
                                       "margin: 2px;"
                                       "width: 16px;"
                                       "}")

        self.mainLayout.addWidget(self.voteCounter, 0, 1, 1, 2)
        self.mainLayout.addWidget(self.wordUsed, 1, 1, 2, 2)
        self.mainLayout.addWidget(self.voteBtn, 3, 1, 1, 1)
        self.mainLayout.addWidget(self.chooseBtn, 3, 2, 1, 1)

        self.setStyleSheet(
            "#Card {background-image: url(resources/" + self.color + "Card.png)}")

    # method to set votes on card
    def setVotes(self, value):
        if self.isRevealed == False:
            if value > 8:
                self.voteCounter.setValue(8)
            elif value < 0:
                self.voteCounter.setValue(0)
            else:
                self.voteCounter.setValue(value)

    def setColor(self, color):
        self.color = color

    def revealColor(self):
        self.isRevealed = True
        self.setStyleSheet(
            "background-image: url(resources/" + self.color + "Card.png)")
        self.mainLayout.removeWidget(self.wordUsed)
        self.wordUsed.deleteLater()
        self.mainLayout.removeWidget(self.voteCounter)
        self.voteCounter.deleteLater()

        if self.isSpymasterView == False:
            self.mainLayout.removeWidget(self.voteBtn)
            self.voteBtn.deleteLater()
            self.mainLayout.removeWidget(self.chooseBtn)
            self.chooseBtn.deleteLater()

    def spyMasterView(self):
        self.isSpymasterView = True
        self.setStyleSheet(
            "#Card {background-image: url(resources/" + self.color + "Card.png)}")
        self.wordUsed.setMaximumSize(160, 25)

        self.mainLayout.removeWidget(self.voteBtn)
        self.voteBtn.deleteLater()
        self.mainLayout.removeWidget(self.chooseBtn)
        self.chooseBtn.deleteLater()
        self.mainLayout.addWidget(self.wordUsed, 1, 1, 2, 3)


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

    def findCard(self, text: str) -> Card:
        for card in self.cardList:
            if card.text == text:
                return card

        return None

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
