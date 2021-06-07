import sys
import os
import threading
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import (QFont, QFontMetrics, QPixmap, QPainter, QBrush, QPen, QColor, QPainterPath, QIcon)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet



class TeamWidget(QWidget):

    def __init__(self,color):
        super().__init__()
        self._color = color;
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.setMinimumSize(60, 60)

    def paintEvent(self, event):
        self.text = None
        if self._color == "red":
            self.text = "Red"
        elif self._color == "blue":
            self.text = "Blue"

        self.font = QFont("Trebuchet MS",40)
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
        
        if self._color == "red":
             painter.fillPath(path, QBrush(QColor(255,100,100))) # Fill the path, where QBrush can set the fill color     
        elif self._color == "blue":
            painter.fillPath(path, QBrush(QColor(100,128,255))) # Fill the path, where QBrush can set the fill color     

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogi = TeamWidget()
    dialogi.show()
    sys.exit(app.exec_())