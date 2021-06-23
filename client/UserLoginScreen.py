import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qt_material import apply_stylesheet

from GUI import UserInterface


class UserLoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username = ""
        self.ip = ""

        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.setMinimumSize(500, 300)

        self.titleWidget = QLabel("Welcome")
        self.titleWidget.setAlignment(Qt.AlignHCenter)
        self.titleWidget.setFont(QFont('Arial', 50))
        self.nameLabel = QLabel("Codename:")
        self.nameLabel.setFixedWidth(200)
        self.nameLabel.setAlignment(Qt.AlignHCenter)
        self.ipLabel = QLabel("Ip:")
        self.ipLabel.setFixedWidth(200)
        self.ipLabel.setAlignment(Qt.AlignHCenter)


        self.nameInput = QLineEdit()
        self.ipInput = QLineEdit()

        self.acceptButton = QPushButton("Accept")
        self.cancelButton = QPushButton("Cancel")



        self.mainLayout.addWidget(self.titleWidget, 0, 0, 0, 0)
        self.mainLayout.addWidget(self.nameLabel, 1, 0)
        self.mainLayout.addWidget(self.ipLabel, 2, 0)
        self.mainLayout.addWidget(self.nameInput, 1, 1)
        self.mainLayout.addWidget(self.ipInput, 2, 1)
        self.mainLayout.addWidget(self.cancelButton, 3, 0)
        self.mainLayout.addWidget(self.acceptButton, 3, 1)

        self.acceptButton.clicked.connect(self.onAcceptButtonClicked)
        self.cancelButton.clicked.connect(self.onCancelButtonClicked)


    def onAcceptButtonClicked(self):
        self.username = self.nameInput.text
        self.ip = self.ipInput.text

        ui = UserInterface(self.username)
        ui.show()
        

    def onCancelButtonClicked(self):
        self.username = None
        self.ip = None

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogi = UserLoginScreen()
    dialogi.show()
    apply_stylesheet(app, theme='dark_amber.xml')
    sys.exit(app.exec_())

