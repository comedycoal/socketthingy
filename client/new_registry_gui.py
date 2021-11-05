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

class RegistryUI(Request):
    def __init__(self, client):
        super().__init__(client, 'REGISTRY')

    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Registry"))
        self.resize(400,400)

        self.regFileView = QTextEdit()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.regFileView.setFont(font)
        self.regFileView.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.regFileView.setObjectName("regFileView")
        self.regFileView.setReadOnly(True)
        self.regFileView.setText(QCoreApplication.translate("MainWindow", "regFileView"))

        self.dir_box = QLineEdit()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.dir_box.setFont(font)
        self.dir_box.setObjectName("dir_box")
        self.dir_box.setText(QCoreApplication.translate("MainWindow", "Input file path"))

        self.subkey_box = QLineEdit()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.subkey_box.setFont(font)
        self.subkey_box.setObjectName("subkey_box")
        self.subkey_box.setText(QCoreApplication.translate("MainWindow", "Input subkey"))

        self.type_box = QLineEdit()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.type_box.setFont(font)
        self.type_box.setObjectName("type_box")
        self.type_box.setText(QCoreApplication.translate("MainWindow", "Input type"))

        self.value_box = QLineEdit()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.value_box.setFont(font)
        self.value_box.setObjectName("hook_button")
        self.value_box.setText(QCoreApplication.translate("MainWindow", "Input value"))

        self.insert_button = QPushButton(clicked = lambda:self.onInsert())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.insert_button.setFont(font)
        self.insert_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.insert_button.setObjectName("insert_button")
        self.insert_button.setText(QCoreApplication.translate("MainWindow", "Insert"))

        self.clear_button = QPushButton(clicked = lambda:self.onClear())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.clear_button.setFont(font)
        self.clear_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.clear_button.setObjectName("clear_button")
        self.clear_button.setText(QCoreApplication.translate("MainWindow", "Clear"))

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.regFileView)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.dir_box)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.subkey_box)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.type_box)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.type_box)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.type_box)

        self.setLayout(mainLayout)

    def onInsert(self):
        pass

    def onClear(self):
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
    tmp = client.ClientProgram()
    demo = RegistryUI(None)
    demo.setupUI()
    demo.ShowWindow() 
    sys.exit(app.exec_())