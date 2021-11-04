from os import close

from posixpath import expanduser
import sys
from tkinter.constants import S
from PySide2.QtCore import *
from PySide2 import QtGui, QtWidgets
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PIL import Image

from client import ClientState
from Request_gui import Request

class LivestreamUI(Request):
    def __init__(self, client):
        super().__init__(client, 'LIVESTREAM')
        self.image = None
        pass

    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "ScreenShot"))
        self.resize(500,500)

        self.streaming_button = QPushButton(clicked = lambda:self.onLivestream())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.streaming_button.setFont(font)
        self.streaming_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.streaming_button.setObjectName("streaming_button")
        self.streaming_button.setText(QCoreApplication.translate("MainWindow", "Streaming"))

        self.stop_button = QPushButton(clicked = lambda: self.onStopLivestream())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.stop_button.setFont(font)
        self.stop_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.stop_button.setObjectName("stop_button")
        self.stop_button.setText(QCoreApplication.translate("MainWindow", "Stop"))

        self.imageView = QLabel()
        self.imageView.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.imageView.setObjectName("imageView")

        button_layout = QHBoxLayout()
        button_layout.addSpacing(100)
        button_layout.addWidget(self.streaming_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.stop_button)
        button_layout.addSpacing(100)

        mainLayout = QVBoxLayout()
        mainLayout.addStretch(0)
        mainLayout.addWidget(self.imageView)
        mainLayout.addItem(button_layout)
        self.setLayout(mainLayout)

    def onStartGUI(self):
        self.ShowWindow()

    def BytesToImage(self, rawdata:bytes):
        split = rawdata.split(b' ', 2)
        w = int(split[0].decode("utf-8"))
        h = int(split[1].decode("utf-8"))
        pixels = split[2]
        image = Image.frombytes("RGB", (w, h), pixels)
        return image

    def onLivestream(self):
        if self.image:
            self.image.close()
            self.image = None

        state = ClientState.SUCCEEDED
        rawdata = None
        state, rawdata = self.MakeBaseRequest('LIVESTREAM START')
        if state == ClientState.NOCONNECTION:
            QMessageBox.about(self, "", "Chưa kết nối đến server")
            return False
        elif state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Lỗi kết nối đến server")
            return False
        pass

    def onStopLivestream(self):
        state, _ = self.MakeBaseRequest('LIVESTREAM STOP')
        
        pass

    def ShowWindow(self):
        self.setupUI()
        self.show()
        pass

if __name__ == '__main__':
    from os import environ

    def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"

    suppress_qt_warnings()

    app = QtWidgets.QApplication(sys.argv)
    demo = LivestreamUI(None)
    demo.setupUI()
    demo.ShowWindow() 
    sys.exit(app.exec_())