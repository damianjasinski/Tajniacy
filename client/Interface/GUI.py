import sys
import os
import threading
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import (QPixmap, QPainter, QBrush, QPen, QColor, QPainterPath, QIcon)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from TeamWidget import TeamWidget
from CardsWidget import CardsWidget
from qt_material import apply_stylesheet


class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1366, 768)
        self.setMaximumSize(1920, 1080)
        self.setWindowTitle("Tajniacy")

        # Layouts set

        # The main layout
        mainLayout = QVBoxLayout()
        # Layout with teams and cards
        playLayout = QHBoxLayout()

        # setCentralWidget
        mainWidget = QWidget()
        mainWidget.setObjectName("mainWidget")
        self.setCentralWidget(mainWidget)
        mainWidget.setLayout(mainLayout)

        # set background based on which team should move
        self.setBackgroundImage("none")

        # Title Label
        titleLabel = QLabel("Tajniacy!")
        titleLabel.setStyleSheet("font-family: 'Trebuchet MS'; font-style:italic; font-weight:bold; font-size:60px; cursive; color: hsl(50, 80%, 50%);")
        titleLabel.setAlignment(Qt.AlignHCenter)
        mainLayout.addWidget(titleLabel)

        # Play (main window for cards and teams) layout set
        mainLayout.addStretch(1)
        mainLayout.addLayout(playLayout)
        mainLayout.addStretch(12)
        playLayout.setAlignment(Qt.AlignVCenter)

        # TeamRed
        teamRed = TeamWidget("red")
        playLayout.addWidget(teamRed, 10)

        # Cards
        cards = CardsWidget()
        playLayout.addWidget(cards, 50)

        # TeamBlue
        teamBlue = TeamWidget("blue")
        playLayout.addWidget(teamBlue, 10)

        # button
        button = QPushButton("Kliknij mnie!")
        mainLayout.addWidget(button)

    # can be called to show which team should move
    def setBackgroundImage(self, teamColor):
        if teamColor == 'Blue':
            self.setStyleSheet("QWidget#mainWidget { background-image: url(Images/backgroundBlue.png);"
                               "background-repeat: no-repeat ;"
                               "background-position: center}")
        elif teamColor == 'Red':
            self.setStyleSheet("QWidget#mainWidget { background-image: url(Images/backgroundRed.png);"
                               "background-repeat: no-repeat ;"
                               "background-position: center}")
        else:
            self.setStyleSheet("QWidget#mainWidget { background-image: url(Images/backgroundNeutral.png);"
                               "background-repeat: no-repeat ;"
                               "background-position: center}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogi = UserInterface()
    dialogi.show()
    apply_stylesheet(app, theme='dark_amber.xml')
    sys.exit(app.exec_())
