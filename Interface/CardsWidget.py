import sys
import os
import threading
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import (QFont, QFontMetrics, QPixmap, QPainter, QBrush, QPen, QColor, QPainterPath, QIcon)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet



class CardsWidget(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.setMinimumSize(60, 60)

        # cardsBoard = QLabel("Cards")
        # cardsBoard.setStyleSheet("font-family: 'Trebuchet MS'; font-style:italic; font-weight:bold; font-size:60px; cursive; color: rgb(128,128,128);")
        # cardsBoard.setAlignment(Qt.AlignCenter)
        
        #mainLayout.addWidget(cardsBoard)


    def paintEvent(self, event):
        self.text = "Cards"
        self.font = QFont("Trebuchet MS",45)
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
        path.addText(px, py, self.font, self.text) # Add the path to draw the font to the path
        painter.setRenderHint(QPainter.Antialiasing) # Turn on anti-aliasing, otherwise it looks ugly
        painter.strokePath(path, pen) # Generate path
        painter.drawPath(path) # Draw path
        painter.fillPath(path, QBrush(QColor(128,128,128))) # Fill the path, where QBrush can set the fill color     



# app = QApplication(sys.argv)
# dialogi = CardsWidget()
# dialogi.show()

# sys.exit(app.exec_())