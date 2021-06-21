from FileReader import FileReader
import sys
import os
import threading
import random
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import (QFont, QFontMetrics, QPixmap, QPainter, QBrush, QPen, QColor, QPainterPath, QIcon)
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
        self.wordUsed.setStyleSheet("background-color : white;"
                                    "color : black")

        self.voteBtn = QPushButton("Vote")
        self.chooseBtn = QPushButton("Choose")
        self.chooseBtn.clicked.connect(self.revealColor)

        self.mainLayout.addWidget(self.wordUsed, 1, 1, 2, 2)
        self.mainLayout.addWidget(self.voteBtn, 3, 1, 1, 1)
        self.mainLayout.addWidget(self.chooseBtn, 3, 2, 1, 1)

        self.setStyleSheet("#Card {background-image: url(Images/" + self.color + "Card.png)}")

    def setColor(self, color):
        self.color = color

    def revealColor(self):
        self.setStyleSheet("background-image: url(Images/" + self.color + "Card.png)")
        self.mainLayout.itemAt(0).widget().deleteLater()
        self.mainLayout.itemAt(1).widget().deleteLater()
        self.mainLayout.itemAt(2).widget().deleteLater()

    def spyMasterView(self):
        self.setStyleSheet("#Card {background-image: url(Images/" + self.color + "Card.png)}")
        self.wordUsed.setMaximumSize(100, 30)
        self.mainLayout.itemAt(1).widget().deleteLater()
        self.mainLayout.itemAt(2).widget().deleteLater()
        self.mainLayout.addWidget(self.wordUsed, 1, 1, 1, 1)


class CardsWidget(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        self.setMinimumSize(500, 500)

        # card colors:
        # Red team: red
        # Blue team: blue
        # Assassin: black
        # Neutral: neutral
        file_reader = FileReader()
        file_reader.read_file("words.txt")
        words = random.choices(file_reader.get_words(), k=25)
        tempCardList = list()
        self.cardList = list()
        for row in range(5):
            for column in range(5):
                # card = Card("Row: " + str(row + 1) + " Column: " + str(column + 1))
                card = Card(words[row + 5 * column])
                tempCardList.append(card)
                self.cardList.append(card)
                mainLayout.addWidget(card, row + 1, column + 1, 1, 1)

        # randomizing cards color
        for i in range(8):
            card = random.choice(tempCardList)
            card.setColor("blue")
            tempCardList.remove(card)
        for i in range(8):
            card = random.choice(tempCardList)
            card.setColor("red")
            tempCardList.remove(card)
        for i in range(7):
            card = random.choice(tempCardList)
            card.setColor("neutral")
            tempCardList.remove(card)

        card = random.choice(tempCardList)
        card.setColor("black")
        tempCardList.remove(card)

        # choose which team starts
        card = random.choice(tempCardList)
        if random.randint(1, 100) < 50:
            card.setColor("blue")
        else:
            card.setColor("red")

        tempCardList.remove(card)

        # use this to get spyMaster view of board
        # for i in self.cardList:
        #    i.spyMasterView()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogi = CardsWidget()
    dialogi.show()
    sys.exit(app.exec_())