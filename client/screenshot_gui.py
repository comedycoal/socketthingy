from PySide2.QtCore import *
from PySide2 import QtGui, QtWidgets
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PIL import Image, ImageQt

from client import ClientState
from request_gui import RequestUI

class ScreenShotUI(RequestUI):
    def __init__(self, parent, client):
        super().__init__(parent, client, 'SCREENSHOT')
        self.image = None
        self.image_bytes = None
        pass

    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "ScreenShot"))
        self.setFixedSize(1304, 750)

        self.screen_capture_button = QPushButton(clicked = lambda:self.onCapScreen())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setWeight(60)
        self.screen_capture_button.setFont(font)
        self.screen_capture_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.screen_capture_button.setObjectName("screen_capture_button")
        self.screen_capture_button.setText(QCoreApplication.translate("MainWindow", "Capture Screen"))

        self.save_button = QPushButton(clicked = lambda: self.onSavePicture())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        font.setWeight(60)
        self.save_button.setFont(font)
        self.save_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.save_button.setObjectName("save_button")
        self.save_button.setText(QCoreApplication.translate("MainWindow", "Save"))

        self.imageView = QLabel()
        self.imageView.resize(1280, 720)
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

    def BytesToQImage(self, rawdata:bytes):
        split = rawdata.split(b' ', 2)
        w = int(split[0].decode("utf-8"))
        h = int(split[1].decode("utf-8"))
        pixels = split[2]
        image = Image.frombytes("RGBA", (w, h), pixels)

        return image

    def onCapScreen(self):
        if self.image:
            self.image = None

        state = ClientState.SUCCEEDED
        rawdata = None
        state, rawdata = self.client.MakeRequest('SCREENSHOT')
        self.image_bytes = rawdata
        if state == ClientState.NOCONNECTION:
            QMessageBox.about(self, "", "Chưa kết nối đến server")
            return False
        elif state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Thao tác thất bại")
            return False

        try:
            self.image = self.BytesToQImage(rawdata)
            imageQt = ImageQt.ImageQt(self.image)
            imageQtScaled = imageQt.scaled(QSize(1280,720), Qt.KeepAspectRatio)
            self.imageView.setPixmap(QPixmap.fromImage(imageQtScaled))
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
                f.write(self.image_bytes)
        pass

    def ShowWindow(self):
        self.setupUI()
        self.show()
        pass

    def OnExitGUI(self):
        self.CleanUp()
        self.close()
        self.parentWindow.HandleChildUIClose(self.baseRequest)
        self.parentWindow.show()

if __name__ == '__main__':
    from os import environ
    import sys
    import client

    def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"

    suppress_qt_warnings()

    app = QtWidgets.QApplication(sys.argv)
    demo = ScreenShotUI(None, client.ClientProgram())
    demo.setupUI()
    demo.ShowWindow() 
    sys.exit(app.exec_())