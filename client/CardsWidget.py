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
    def __init__(self, text):
        super().__init__()
        self.setObjectName("Card")

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.setMinimumSize(150, 100)
        self.color = "default"

        self.wordUsed = QLabel(str(text).upper())
        self.wordUsed.setAlignment(Qt.AlignCenter)
        self.wordUsed.setStyleSheet(
            "background-color:white; font-family: 'Berlin Sans FB'; font-size:14px;"
            "color : black")

        self.voteBtn = QPushButton("Vote")
        self.voteBtn.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:10px;border-radius:10px;")
        self.chooseBtn = QPushButton("Choose")
        self.chooseBtn.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:10px;border-radius:10px;")
        self.chooseBtn.clicked.connect(self.revealColor)

        self.mainLayout.addWidget(self.wordUsed, 1, 1, 2, 2)
        self.mainLayout.addWidget(self.voteBtn, 3, 1, 1, 1)
        self.mainLayout.addWidget(self.chooseBtn, 3, 2, 1, 1)

        self.setStyleSheet(
            "#Card {background-image: url(resources/" + self.color + "Card.png)}")

    def setColor(self, color):
        self.color = color

    def revealColor(self):
        self.setStyleSheet(
            "background-image: url(resources/" + self.color + "Card.png)")
        self.mainLayout.itemAt(0).widget().deleteLater()
        self.mainLayout.itemAt(1).widget().deleteLater()
        self.mainLayout.itemAt(2).widget().deleteLater()

    def spyMasterView(self):
        self.setStyleSheet(
            "#Card {background-image: url(resources/" + self.color + "Card.png)}")
        self.wordUsed.setMaximumSize(100, 30)
        self.mainLayout.itemAt(1).widget().deleteLater()
        self.mainLayout.itemAt(2).widget().deleteLater()
        self.mainLayout.addWidget(self.wordUsed, 1, 1, 1, 1)


class CardsWidget(QWidget):
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
                card = Card(sharedCard.name)

                card.setColor(sharedCard.color.name.lower())

                self.cardList.append(card)
                self.mainLayout.addWidget(card, row + 1, column + 1, 1, 1)

    # use this to get spyMaster view of board
    def showSpymasterView(self):
        for card in self.cardList:
            card.spyMasterView()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogi = CardsWidget()
    dialogi.show()
    sys.exit(app.exec_())
