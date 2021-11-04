from os import close
from posixpath import expanduser
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QMessageBox, QVBoxLayout

from client import ClientState
from client import ClientProgram

from screenshot_gui import ScreenShotUI
from directory_gui import DirectoryUI
from input_gui import InputUI
from process_gui import ProcessUI, ApplicationUI

class FunctionUI(QtWidgets.QWidget):
    def __init__(self, clientProgram:ClientProgram):
        super().__init__()
        self.clientProgram = clientProgram
        self.keystroke = InputUI(self.clientProgram)
        self.screenshot = ScreenShotUI(self.clientProgram)
        self.directory = DirectoryUI(self.clientProgram)
        self.process = ProcessUI(self.clientProgram)
        self.application = ApplicationUI(self.clientProgram)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        close = QMessageBox.question(self, "Thoát", "Bạn chắc chắn muốn thoát?", 
                                    QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
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

    def setupUI(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Function"))
        # self.resize(400,400)
        self.setFixedSize(300,300)

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

        self.process_button = QtWidgets.QPushButton(clicked = lambda:self.process.OnStartGUI())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.process_button.setFont(font)
        self.process_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.process_button.setObjectName("process_button")
        self.process_button.setText(_translate("MainWindow", "Process Running"))

        self.application_button = QtWidgets.QPushButton(clicked = lambda:self.application.OnStartGUI())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.application_button.setFont(font)
        self.application_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.application_button.setObjectName("application_button")
        self.application_button.setText(_translate("MainWindow", "App Running"))

        self.shutdown_button = QtWidgets.QPushButton(clicked = lambda:self.onShutdown())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.shutdown_button.setFont(font)
        self.shutdown_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.shutdown_button.setObjectName("shutdown_button")
        self.shutdown_button.setText(_translate("MainWindow", "Shutdown"))

        self.keystroke_button = QtWidgets.QPushButton(clicked = lambda:self.keystroke.OnStartGUI())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.keystroke_button.setFont(font)
        self.keystroke_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.keystroke_button.setObjectName("keystroke_button")
        self.keystroke_button.setText(_translate("MainWindow", "Keystroke"))

        self.screenshot_button = QtWidgets.QPushButton(clicked = lambda:self.screenshot.OnStartGUI())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.screenshot_button.setFont(font)
        self.screenshot_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.screenshot_button.setObjectName("screenshot_button")
        self.screenshot_button.setText(_translate("MainWindow", "Screenshot"))

        self.streaming_button = QtWidgets.QPushButton(clicked = lambda:self.screenshot.OnStartGUI())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.streaming_button.setFont(font)
        self.streaming_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.streaming_button.setObjectName("streaming_button")
        self.streaming_button.setText(_translate("MainWindow", "Stream"))

        self.logout_button = QtWidgets.QPushButton(clicked = lambda:self.onLogOut())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.logout_button.setFont(font)
        self.logout_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.logout_button.setObjectName("logout_button")
        self.logout_button.setText(_translate("MainWindow", "Logout"))
        QtCore.QMetaObject.connectSlotsByName(self)

        self.directory_button = QtWidgets.QPushButton(clicked = lambda:self.directory.OnStartGUI())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.directory_button.setFont(font)
        self.directory_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.directory_button.setObjectName("directory_button")
        self.directory_button.setText(_translate("MainWindow", "Directory"))
        QtCore.QMetaObject.connectSlotsByName(self)

        self.test_button = QtWidgets.QPushButton(clicked = lambda: self.close())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.test_button.setFont(font)
        self.test_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.test_button.setObjectName("test_button")
        self.test_button.setText(_translate("MainWindow", "test"))

        self.info_button = QtWidgets.QPushButton(clicked = lambda: self.onShowMACAdress())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.info_button.setFont(font)
        self.info_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.info_button.setObjectName("info_button")
        self.info_button.setText(_translate("MainWindow", "MAC Address"))

        QtCore.QMetaObject.connectSlotsByName(self)

        layout = QVBoxLayout()
        layout.addWidget(self.function_label)
        layout.addWidget(self.keystroke_button)
        layout.addWidget(self.screenshot_button)
        layout.addWidget(self.streaming_button)
        layout.addWidget(self.shutdown_button)
        layout.addWidget(self.logout_button)
        layout.addWidget(self.directory_button)
        layout.addWidget(self.process_button)
        layout.addWidget(self.application_button)
        layout.addWidget(self.info_button)
        layout.addWidget(self.test_button)

        self.setLayout(layout)

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