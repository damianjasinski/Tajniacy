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

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        self.setMinimumSize(200, 100)
        self.color = "DimGrey"

        self.wordUsed = QLabel(str(text).upper())
        self.wordUsed.setAlignment(Qt.AlignCenter)
        self.wordUsed.setStyleSheet("background-color : white;"
                                    "color : black")

        self.voteBtn = QPushButton("Vote")
        self.chooseBtn = QPushButton("Choose")
        self.chooseBtn.clicked.connect(self.revealColor)

        mainLayout.addWidget(self.wordUsed, 1, 1, 2, 2)
        mainLayout.addWidget(self.voteBtn, 3, 1, 1, 1)
        mainLayout.addWidget(self.chooseBtn, 3, 2, 1, 1)

        self.setStyleSheet("background-color : AntiqueWhite;"
                           "color : DarkGrey;")

    def setColor(self,color):
        self.color = color

    def revealColor(self):
        self.setStyleSheet("background-color : " + self.color + ";")
        #self.chooseBtn.setEnabled(False)
        #self.voteBtn.setEnabled(False)


class CardsWidget(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        self.setMinimumSize(500, 500)
        

        # TO DO: load cards from file
        # card colors:
        # Red team: DarkRed
        # Blue team: DarkBlue
        # Assassin: Black
        # Neutral: DimGrey
        file_reader = FileReader()
        file_reader.read_file("Interface/words.txt")
        words = random.choices(file_reader.get_words(), k=25)
        cardList = list()
        for row in range(5):
            for column in range(5):
                #card = Card("Row: " + str(row + 1) + " Column: " + str(column + 1))
                card = Card(words[row+5*column])
                cardList.append(card)
                mainLayout.addWidget(card, row + 1, column + 1, 1, 1)

        #randomizing cards color
        for i in range(8):
            card = random.choice(cardList)
            card.setColor("DarkBlue")
            cardList.remove(card)
        for i in range(8):
            card = random.choice(cardList)
            card.setColor("DarkRed")
            cardList.remove(card)
        for i in range(7):
            card = random.choice(cardList)
            card.setColor("DimGrey")
            cardList.remove(card)

        card = random.choice(cardList)
        card.setColor("Black")
        cardList.remove(card)

        # choose which team starts
        card = random.choice(cardList)
        if random.randint(1,100) < 50:
            card.setColor("DarkBlue")
        else:
            card.setColor("DarkRed")

        cardList.remove(card)

        # cardsBoard = QLabel("Cards")
        # cardsBoard.setStyleSheet("font-family: 'Trebuchet MS'; font-style:italic; font-weight:bold; font-size:60px; cursive; color: rgb(128,128,128);")
        # cardsBoard.setAlignment(Qt.AlignCenter)

        # mainLayout.addWidget(cardsBoard)

    def paintEvent(self, event):
        self.text = "Cards"
        self.font = QFont("Trebuchet MS", 45)
        metrics = QFontMetrics(self.font)
        painter = QPainter(self)
        path = QPainterPath()
        pen = QPen(Qt.white)
        len = metrics.width(self.text)
        w = self.width()
        px = (len - w) / 2
        if px < 0:
            px = -px
            py = (self.height() - metrics.height()) / 2 + metrics.ascent()
        if py < 0:
            py = -py
        pen.setWidth(2)
        path.addText(px, py, self.font, self.text)  # Add the path to draw the font to the path
        painter.setRenderHint(QPainter.Antialiasing)  # Turn on anti-aliasing, otherwise it looks ugly
        painter.strokePath(path, pen)  # Generate path
        painter.drawPath(path)  # Draw path
        painter.fillPath(path, QBrush(QColor(128, 128, 128)))  # Fill the path, where QBrush can set the fill color

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogi = CardsWidget()
    dialogi.show()
    sys.exit(app.exec_())
