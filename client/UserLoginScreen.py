from client.NetClient import NetClient
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qt_material import apply_stylesheet

from client.GUI import MainWindow


class UserLoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.username = ""
        self.ip = ""

        self.netClient = None

        self.mainWidget = QWidget()
        self.mainWidget.setObjectName("mainWidget")
        self.setCentralWidget(self.mainWidget)

        self.mainLayout = QGridLayout()
        self.mainWidget.setLayout(self.mainLayout)
        self.setMinimumSize(500, 300)

        self.titleWidget = QLabel("Welcome")
        self.titleWidget.setAlignment(Qt.AlignHCenter)
        self.titleWidget.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:70px;")
        self.nameLabel = QLabel("Codename:")
        self.nameLabel.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:25px;")
        self.nameLabel.setFixedWidth(200)
        self.nameLabel.setAlignment(Qt.AlignHCenter)
        self.ipLabel = QLabel("Ip:")
        self.ipLabel.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:25px;")
        self.ipLabel.setFixedWidth(200)
        self.ipLabel.setAlignment(Qt.AlignHCenter)

        self.nameInput = QLineEdit("player")
        self.ipInput = QLineEdit("127.0.0.1")
        self.ipInput.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:18px;")
        self.nameInput.setStyleSheet(
            "font-family:Berlin Sans FB; font-size:18px;")

        self.redButton = QPushButton("Connect")
        self.blueButton = QPushButton("Cancel")

        self.mainLayout.addWidget(self.titleWidget, 0, 0, 0, 0)
        self.mainLayout.addWidget(self.nameLabel, 1, 0)
        self.mainLayout.addWidget(self.ipLabel, 2, 0)
        self.mainLayout.addWidget(self.nameInput, 1, 1)
        self.mainLayout.addWidget(self.ipInput, 2, 1)
        self.mainLayout.addWidget(self.blueButton, 3, 0)
        self.mainLayout.addWidget(self.redButton, 3, 1)

        self.redButton.clicked.connect(self.onAcceptButtonClicked)
        self.blueButton.clicked.connect(self.onCancelButtonClicked)

    def onAcceptButtonClicked(self):

        self.username = self.nameInput.text()
        self.ip = self.ipInput.text()

        self.netClient = NetClient(self.ip, 4123)
        self.netClient.onConnect.connect(self.onSocketConnect)
        self.netClient.onFail.connect(self.onSocketFail)
        self.netClient.start()

    def onCancelButtonClicked(self):
        self.close()

    def onSocketConnect(self):
        self.ui = MainWindow(self.username, self.netClient)
        self.ui.show()
        self.close()

    def onSocketFail(self):
        QMessageBox.warning(self, "Fail", "Cannot connect!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogi = UserLoginScreen()
    dialogi.show()
    apply_stylesheet(app, theme='dark_amber.xml')
    sys.exit(app.exec_())
