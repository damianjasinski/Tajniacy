import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QPainter, QPainterPath, QPen
from PyQt5.QtCore import Qt


class TeamWidget(QWidget):

    def __init__(self, color):
        super().__init__()
        if color == 'red' or color == 'Red':
            self._color = "rgb(153, 0, 0)"
        elif color == 'blue' or color == 'Blue':
            self._color = "rgb(0, 0, 153)"

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        self.setMinimumSize(60, 60)

        self.listWidget = QListWidget()
        self.listWidget.setEnabled(False)                 
        self.listWidget.setStyleSheet("font-family:Berlin Sans FB; font-size:18px; Background-color: "+self._color+";"
                                      "border: 2px solid "+color)

        #self.listWidget.setStyleSheet("QListWidget::item {color: yellow}")

        mainLayout.addWidget(self.listWidget)

    def addPlayer(self, playerName):
        self.listWidget.addItem(playerName)

    def removePlayer(self, playerPosition):
        self.listWidget.takeItem(self.listWidget.itemAt(playerPosition))

    
    # def paintEvent(self, event):
    #     self.text = None
    #     if self._color == "red":
    #         self.text = "Red"
    #     elif self._color == "blue":
    #         self.text = "Blue"
    
    #     self.font = QFont("Trebuchet MS", 40)
    #     metrics = QFontMetrics(self.font)
    #     painter = QPainter(self)
    #     path = QPainterPath()
    #     pen = QPen(Qt.white)
    #     len = metrics.width(self.text)
    #     w = self.width()
    #     px = (len - w) / 2
    #     if px < 0:
    #         px = -px
    #         py = (self.height() - metrics.height()) / 2 + metrics.ascent()
    #     if py < 0:
    #         py = -py
    #     pen.setWidth(2)
    #     path.addText(px, py, self.font, self.text)  # Add the path to draw the font to the path
    #     painter.setRenderHint(QPainter.Antialiasing)  # Turn on anti-aliasing, otherwise it looks ugly
    #     painter.strokePath(path, pen)  # Generate path
    #     painter.drawPath(path)  # Draw path
    
    #     if self._color == "red":
    #         painter.fillPath(path, QBrush(QColor(255, 100, 100)))  # Fill the path, where QBrush can set the fill color
        #elif self._color == "blue":
            #painter.fillPath(path, QBrush(QColor(100, 128, 255)))  # Fill the path, where QBrush can set the fill color


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     dialogi = TeamWidget()
#     dialogi.show()
#     sys.exit(app.exec_())
