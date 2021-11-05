from os import close
from posixpath import expanduser
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QMessageBox, QPushButton, QVBoxLayout, QGridLayout

from client import ClientState
from client import ClientProgram

from screenshot_gui import ScreenShotUI
from streaming_gui import LivestreamUI
from directory_gui import DirectoryUI
from input_gui import InputUI
from process_gui import ProcessUI, ApplicationUI

class RequestButtonPack:
    def __init__(self, parent, identifierStr: str, button: QPushButton):
        self.identifier = identifierStr
        self.parent = parent
        self.button = button
        self.requestUI = None
        self.Refresh()

    def Refresh(self):
        if self.identifier == "APPLICATION":
            self.requestUI = ApplicationUI(self.parent, self.parent.clientProgram)
        elif self.identifier == "PROCESS":
            self.requestUI = ProcessUI(self.parent, self.parent.clientProgram)
        elif self.identifier == "KEYLOG":
            self.requestUI = InputUI(self.parent, self.parent.clientProgram)
        elif self.identifier == "DIRECTORY":
            self.requestUI = DirectoryUI(self.parent, self.parent.clientProgram)
        elif self.identifier == "SCREENSHOT":
            self.requestUI = ScreenShotUI(self.parent, self.parent.clientProgram)
        elif self.identifier == "LIVESTREAM":
            self.requestUI = LivestreamUI(self.parent, self.parent.clientProgram)

        self.button.clicked.connect(self.requestUI.OnStartGUI)

class FunctionUI(QtWidgets.QWidget):
    def __init__(self, parentWindow, clientProgram:ClientProgram):
        super().__init__()
        self.parentWindow = parentWindow
        self.clientProgram = clientProgram

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        close = QMessageBox.question(self, "Thoát", "Bạn chắc chắn muốn thoát?",
                                    QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
            self.close()
            self.parentWindow.Disconnect()
            self.parentWindow.show()
        else:
            event.ignore()

    def onShutdown(self):
        state, _ = self.clientProgram.MakeRequest("SHUTDOWN S")
        if state == ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Sau 3s máy tính sẽ tắt")
            self.clientProgram.Disconnect()
        else:
            QMessageBox.about(self, "", "Lỗi kết nối đến server")

    def onLogOut(self):
        state, _ = self.clientProgram.MakeRequest("SHUTDOWN L")
        if state == ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Sau 3s máy tính sẽ logout")
        else:
            QMessageBox.about(self, "", "Lỗi kết nối đến server")

    def onShowMACAdress(self):
        state, rawdata = self.clientProgram.MakeRequest("INFO MACADDRESS")
        macAdd = rawdata.decode("utf-8")
        if state == ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "MAC Address: " + macAdd)
        else:
            QMessageBox.about(self, "", "Lỗi kết nối đến server")

    def MakeButton(self, font, style, name, text):
        button = QtWidgets.QPushButton()
        button.setFont(font)
        button.setStyleSheet(style)
        button.setObjectName(name)
        button.setText(text)
        return button

    def HandleChildUIClose(self, identifier):
        pack = None
        if identifier == "APPLICATION":
            pack = self.application_pack
        elif identifier == "PROCESS":
            pack = self.process_pack
        elif identifier == "KEYLOG":
            pack = self.input_pack
        elif identifier == "DIRECTORY":
            pack = self.directory_pack
        elif identifier == "SCREENSHOT":
            pack = self.screenshot_pack
        elif identifier == "LIVESTREAM":
            pack = self.streaming_pack

        self.streaming_pack.Refresh()


    def setupUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Function"))
        self.setFixedSize(300,210)

        self.function_label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.function_label.setFont(font)
        self.function_label.setStyleSheet("color: rgb(155, 24, 128);")
        self.function_label.setAlignment(QtCore.Qt.AlignCenter)
        self.function_label.setObjectName("function_label")
        self.function_label.setText(_translate("MainWindow", "FUNCTION"))

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        style ="background-color: rgb(224, 237, 255)"

        self.process_pack = RequestButtonPack(
            self,
            "PROCESS",
            self.MakeButton(font, style, "process_button", _translate("MainWindow", "Process Running")))

        self.application_pack = RequestButtonPack(
            self,
            "APPLICATION",
            self.MakeButton(font, style, "application_button", _translate("MainWindow", "App Running")))

        self.input_pack = RequestButtonPack(
            self,
            "KEYLOG",
            self.MakeButton(font, style, "input_button", _translate("MainWindow", "Input")))

        self.screenshot_pack = RequestButtonPack(self,
            "SCREENSHOT",
            self.MakeButton(font, style, "screenshot_button", _translate("MainWindow", "Screenshot")))

        self.streaming_pack = RequestButtonPack(
            self,
            "LIVESTREAM",
            self.MakeButton(font, style, "streaming_button", _translate("MainWindow", "Stream")))

        self.directory_pack = RequestButtonPack(
            self,
            "DIRECTORY",
            self.MakeButton(font, style, "directory_button", _translate("MainWindow", "Directory")))

        self.shutdown_button = self.MakeButton(font, style, "shutdown_button", _translate("MainWindow", "Shutdown"))
        self.logout_button = self.MakeButton(font, style, "logout_button", _translate("MainWindow", "Logout"))
        self.info_button = self.MakeButton(font, style, "info_button", _translate("MainWindow", "MAC Address"))


        self.info_button.clicked.connect(self.onShowMACAdress)
        self.shutdown_button.clicked.connect(self.onShutdown)
        self.logout_button.clicked.connect(self.onLogOut)



        layout1 = QVBoxLayout()
        layout1.addWidget(self.screenshot_pack.button)
        layout1.addSpacing(5)
        layout1.addWidget(self.streaming_pack.button)
        layout1.addSpacing(5)

        layout2 = QVBoxLayout()
        layout2.addWidget(self.input_pack.button)
        layout2.addSpacing(5)
        layout2.addWidget(self.directory_pack.button)
        layout2.addSpacing(5)

        layout3 = QVBoxLayout()
        layout3.addWidget(self.process_pack.button)
        layout3.addSpacing(5)
        layout3.addWidget(self.application_pack.button)

        layout4t = QGridLayout()
        layout4t.setHorizontalSpacing(5)
        layout4t.addWidget(self.logout_button, 0, 0)
        layout4t.addWidget(self.shutdown_button, 0, 1)

        layout4 = QVBoxLayout()
        layout4.addWidget(self.info_button)
        layout4.addSpacing(5)
        layout4.addItem(layout4t)

        buttonLayout = QGridLayout()
        buttonLayout.setHorizontalSpacing(15)
        buttonLayout.setVerticalSpacing(10)
        buttonLayout.addItem(layout1, 0, 0)
        buttonLayout.addItem(layout2, 0, 1)
        buttonLayout.addItem(layout3, 1, 0)
        buttonLayout.addItem(layout4, 1, 1)

        tmp = QtWidgets.QWidget(self)
        tmp.setStyleSheet("background-color: rgb(124, 237, 150)")

        mainLayout = QVBoxLayout(tmp)
        mainLayout.addWidget(self.function_label)
        mainLayout.addItem(buttonLayout)

        self.setLayout(mainLayout)

if __name__ == '__main__':
    from os import environ

    def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"

    suppress_qt_warnings()

    app = QtWidgets.QApplication(sys.argv)
    demo = FunctionUI(None)
    demo.setupUI()
    demo.show()
    sys.exit(app.exec_())