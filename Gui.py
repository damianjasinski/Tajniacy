import sys
import os

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import (QPixmap, QPainter, QBrush, QPen, QColor, QPainterPath, QIcon)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet




class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800,600)
        self.setWindowTitle("Tajniacy")

        #Layouts set

        #The main layout
        mainLayout = QVBoxLayout()
        #Layout with teams and cards 
        playLayout = QHBoxLayout()

        #setCentralWidget
        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        mainWidget.setLayout(mainLayout)

        #Title Label
        titleLabel = QLabel("Tajniacy!")
        titleLabel.setStyleSheet("font-family: 'Trebuchet MS'; font-style:italic; font-weight:bold; font-size:60px; cursive; color: hsl(50, 80%, 50%);")
        titleLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(titleLabel)


        #Play (main window for cards and teams) layout set
        #


        #button
        button = QPushButton("Kliknij mnie!")
        mainLayout.addWidget(button)








app = QApplication(sys.argv)
dialogi = UserInterface()
dialogi.show()
apply_stylesheet(app, theme='dark_amber.xml')
sys.exit(app.exec_())