from client.ClientPacketHandler import ClientPacketHandler
import pickle
import socket
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class NetClient(QThread):
    onConnect = pyqtSignal()
    onFail = pyqtSignal()
    onPacketReceive = pyqtSignal(bytes)

    def __init__(self, ip, port):
        QThread.__init__(self)

        self._ip = ip
        self._port = port
        self._socket = None
        self._isConnected = False
        self._isRunning = True
        self._packetHandler = ClientPacketHandler(self)

    def setMainWindow(self, mainWindow):
        self._packetHandler.setMainWindow(mainWindow)

    def run(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            print(self._ip)
            print(self._port)
            self._socket.connect((self._ip, self._port))
            self.isConnected = True
            self.onConnect.emit()

            while self._isRunning:
                buff = self._socket.recv(1024)
                self.onPacketReceive.emit(buff)

        except OSError as asd:
            print(asd)
            self.onFail.emit()

        self._isConnected = False
        self._socket = None

        print("Thread end")

    def running(self):
        return self._isRunning

    def connected(self):
        return self._isConnected

    def close(self):
        self._isRunning = False

        if self._socket != None:
            self._socket.close()

    def sendData(self, data):
        self._socket.sendall(pickle.dumps(data))
