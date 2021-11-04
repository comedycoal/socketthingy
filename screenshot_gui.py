from os import close

from posixpath import expanduser
import sys
from tkinter.constants import S
from PySide2.QtCore import *
from PySide2 import QtGui, QtWidgets
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PIL import Image, ImageQt

from client import ClientState
from Request_gui import Request

class ScreenShotUI(Request):
    def __init__(self, client):
        super().__init__(client, 'SCREENSHOT')
        self.image = None
        pass

    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "ScreenShot"))
        self.setGeometry(20,20,500,500)
        self.resize(500,500)

        self.screen_capture_button = QPushButton(clicked = lambda:self.onCapScreen())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.screen_capture_button.setFont(font)
        self.screen_capture_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.screen_capture_button.setObjectName("screen_capture_button")
        self.screen_capture_button.setText(QCoreApplication.translate("MainWindow", "Capture Screen"))

        self.save_button = QPushButton(clicked = lambda: self.onSavePicture())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.save_button.setFont(font)
        self.save_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.save_button.setObjectName("save_button")
        self.save_button.setText(QCoreApplication.translate("MainWindow", "Save"))

        self.imageView = QLabel()
        self.imageView.resize(450, 450)
        self.imageView.setObjectName("imageView")
        self.onCapScreen()

        button_layout = QHBoxLayout()
        button_layout.addSpacing(100)
        button_layout.addWidget(self.screen_capture_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.save_button)
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
        image.resize(size=[450,450])
        imageQt = ImageQt.ImageQt(image)
        return imageQt

    def onCapScreen(self):
        if self.image:
            self.image = None

        state = ClientState.SUCCEEDED
        rawdata = None
        state, rawdata = self.client.MakeRequest('SCREENSHOT')
        if state == ClientState.NOCONNECTION:
            QMessageBox.about(self, "", "Chưa kết nối đến server")
            return False
        elif state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Lỗi kết nối đến server")
            return False

        try:
            img = self.BytesToImage(rawdata)
            self.image = QPixmap.fromImage(img)
            self.imageView.setPixmap(self.image)
            return True
        except Exception as e:
            QMessageBox.about(self, "", str(e))
            return False

    def onSavePicture(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        imagename, _ = QFileDialog.getSaveFileName(
            self, "Save Image", r"C:", "All Files (*)", options=options
        )
        if imagename:
            with open(imagename, "wb") as f:
                f.write(self.image)
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
    demo = ScreenShotUI(None)
    demo.setupUI()
    demo.ShowWindow() 
    sys.exit(app.exec_())