import sys
import os
import threading
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QIcon, QPainter, QPainterPath, QPen, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from TeamWidget import TeamWidget
from CardsWidget import CardsWidget
from qt_material import apply_stylesheet


class UserInterface(QMainWindow):
    def __init__(self, username: str, color: str):
        super().__init__()
        self.setMinimumSize(1366, 768)
        self.setMaximumSize(1920, 1080)
        self.setWindowTitle("Tajniacy")

        self.spymasterView = True

        # Layouts set

        # The main layout
        mainLayout = QVBoxLayout()
        # Layout with teams and cards
        playLayout = QHBoxLayout()
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
        titleLabel = QLabel("Tajniacy!")
        titleLabel.setStyleSheet(
            "font-family: 'Berlin Sans FB'; font-size:80px; cursive; color: hsl(50, 80%, 50%);")
        titleLabel.setAlignment(Qt.AlignHCenter)
        mainLayout.addStretch(5)
        mainLayout.addWidget(titleLabel)
        

        # Play (main window for cards and teams) layout set
        mainLayout.addStretch(1)
        mainLayout.addLayout(playLayout)
        mainLayout.addStretch(5)
        mainLayout.addLayout(bottomLayout)
        playLayout.setAlignment(Qt.AlignVCenter)

        # TeamRed
        teamRed = TeamWidget("red")
        playLayout.addWidget(teamRed, 10)

        # temporary line
        teamRed.addSpymaster("Test (Spymaster)")

        # Cards
        cards = CardsWidget()
        playLayout.addWidget(cards, 50)

        # TeamBlue
        teamBlue = TeamWidget("blue")
        playLayout.addWidget(teamBlue, 10)

        # temporary line
        teamBlue.addSpymaster("Test (Spymaster)")

        if self.spymasterView:
            #cards.showSpymasterView()
            # bottomLayout
            bottomLayout.setAlignment(Qt.AlignHCenter)
            bottomLayout.addWidget(QLabel(""),3)
            self.spymasterInput = QLineEdit()
            self.spymasterInput.setAlignment(Qt.AlignCenter)
            self.spymasterInput.setPlaceholderText(
                "Podaj slowo opisujace karty oraz wybierz ilosc kart do odgadniecia")
            self.spymasterInput.setFocus(False)
            self.spymasterInput.setStyleSheet("font-family:Berlin Sans FB; font-size:18px;")
            self.numberOfCards = QComboBox()
            self.numberOfCards.setStyleSheet("font-family:Berlin Sans FB; font-size:18px;")
            for i in range(8):
                self.numberOfCards.addItem(str(i+1))

            bottomLayout.addWidget(self.spymasterInput,2)
            bottomLayout.addWidget(self.numberOfCards)
            bottomLayout.addWidget(QLabel(""),3)

            # button
            mainLayout.addLayout(buttonLayout)
            buttonLayout.setAlignment(Qt.AlignHCenter)
            button = QPushButton("Zatwierdz")
            button.setStyleSheet("font-family:Berlin Sans FB; font-size:18px; border-radius:10px;")
            button.setMinimumSize(150,50)
            buttonLayout.addWidget(button)
            mainLayout.addStretch(8)

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
    dialogi = UserInterface("user", "red")
    dialogi.show()
    apply_stylesheet(app, theme='dark_amber.xml')
    sys.exit(app.exec_())
