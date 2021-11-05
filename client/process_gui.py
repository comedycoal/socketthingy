from os import close
from posixpath import expanduser
import sys
from tkinter.constants import S
from PySide2.QtCore import *
from PySide2 import QtGui, QtWidgets
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from client import ClientState
import json
from request_gui import Request
import client

class ProcessUI(Request):
    def __init__(self, parent, client):
        super().__init__(parent, client, 'PROCESS')
        self.windowName = "Process"
        self.headings = ('Process Name', 'Process ID', 'Thread Count')

    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", self.windowName))
        self.resize(500,500)

        self.find_label = QLabel()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.find_label.setFont(font)
        # self.find_label.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.find_label.setObjectName("find_label")
        self.find_label.setText(QCoreApplication.translate("MainWindow","Find:"))

        self.txtFind = QLineEdit()
        self.txtFind.textChanged[str].connect(self.onFind)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.txtFind.setFont(font)
        # self.txtFind.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.txtFind.setObjectName("txtFind")

        # self.model = QStandardItemModel(0, 3, self)
        # self.model.setHeaderData(0, Qt.Horizontal, self.headings[0])
        # self.model.setHeaderData(1, Qt.Horizontal, self.headings[1])
        # self.model.setHeaderData(2, Qt.Horizontal, self.headings[2])
        # self.model.insertRow(0)
        # self.model.setData(self.model.index(0, 0), "a")
        # self.model.setData(self.model.index(0, 1), "1")
        # self.model.setData(self.model.index(0, 2),"test1")
        # self.model.insertRow(0)
        # self.model.setData(self.model.index(0, 0), "c")
        # self.model.setData(self.model.index(0, 1), "3")
        # self.model.setData(self.model.index(0, 2),"test2")
        # self.model.insertRow(0)
        # self.model.setData(self.model.index(0, 0), "b")
        # self.model.setData(self.model.index(0, 1), "0")
        # self.model.setData(self.model.index(0, 2),"test3")

        self.model = self.createProcessModel(self)
        self.proxy_model = QSortFilterProxyModel(recursiveFilteringEnabled = True)
        self.proxy_model.setSourceModel(self.model)
        self.treeView = self.createProcessTree(self.proxy_model)

        self.kill_button = QtWidgets.QPushButton(clicked = lambda:self.onKill())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.kill_button.setFont(font)
        self.kill_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.kill_button.setObjectName("kill_button")
        self.kill_button.setText(QCoreApplication.translate("MainWindow", "Kill"))

        self.start_button = QtWidgets.QPushButton(self, clicked = lambda:self.onStart())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.start_button.setFont(font)
        self.start_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.start_button.setObjectName("start_button")
        self.start_button.setText(QCoreApplication.translate("MainWindow", "Start"))

        findLayout = QHBoxLayout()
        findLayout.addWidget(self.find_label)
        findLayout.addSpacing(10)
        findLayout.addWidget(self.txtFind)
        findLayout.addSpacing(10)
        findLayout.addWidget(self.kill_button)
        findLayout.addSpacing(10)
        findLayout.addWidget(self.start_button)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(findLayout)
        mainLayout.addWidget(self.treeView)

        self.setLayout(mainLayout)

    def createProcessTree(self, model):
        treeView = QTreeView()
        treeView.setModel(model)
        treeView.setColumnWidth(0, 300)
        treeView.setColumnWidth(1, 100)
        treeView.setAlternatingRowColors(True)
        treeView.setSortingEnabled(True)
        treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        treeView.customContextMenuRequested.connect(self.showContextMenu)
        return treeView

    def createProcessModel(self, parent):
        state, rawdata = self.client.MakeRequest('FETCH')
        if state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Không thể tải dữ liệu")
            return

        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(0, Qt.Horizontal, self.headings[0])
        model.setHeaderData(1, Qt.Horizontal, self.headings[1])
        model.setHeaderData(2, Qt.Horizontal, self.headings[2])

        itemlist = json.loads(rawdata)
        self.addItem(model, itemlist)

        return model

    def addItem(self, model, itemlist):
        for item in itemlist:
            model.insertRow(0)
            model.setData(model.index(0, 0), item["name"])
            model.setData(model.index(0, 1), item["pid"])
            model.setData(model.index(0, 2), item["num_threads"])

    def viewProcessTree(self):
        if self.treeView.selectedIndexes():
            items = self.treeView.selectedIndexes()[0]
        else:
            items = []
        for item in items:
            self.model.removeRow(item.row())

        self.model = self.createProcessModel(self)
        self.proxy_model.setSourceModel(self.model)
        self.treeView = self.createProcessTree(self.proxy_model)

    def onKill(self):
        index = self.treeView.selectedIndexes()[0]
        item = self.proxy_model.itemData(index)
        print(item)
        self.RequestKill(item)
        
        self.model.removeRow(index.row())
        self.viewProcessTree()

    def onStart(self):
        item = self.txtFind.text()
        self.RequestStart(item)
        self.viewProcessTree()

    def onFind(self):
        self.proxy_model.setFilterWildcard("*{}*".format(self.txtFind.text()))
        # index = self.treeView.selectedIndexes()
        # if index:
        #     self.kill_button.setText(QCoreApplication.translate("MainWindow", "Kill"))
        #     self.kill_button.clicked.disconnect()
        #     self.kill_button.clicked.connect(self.onKill)
        # else:
        #     self.kill_button.setText(QCoreApplication.translate("MainWindow", "Start"))
        #     self.kill_button.clicked.disconnect()
        #     self.kill_button.clicked.connect(self.onStart)

    def showContextMenu(self, point):
        ix = self.treeView.indexAt(point)
        if ix.column() == 0 or ix.column() == 1 or ix.column() == 2:
            menu = QMenu(self.treeView)
            menu.addAction("Kill")
            action = menu.exec_(self.treeView.mapToGlobal(point))
            if action:
                if action.text() == "Kill":
                    self.onKill()

    def RequestKill(self, id_to_kill):
        state, _ = self.client.MakeRequest('KILL ' + id_to_kill)
        if state == client.ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Đã diệt process")
        else:
            QMessageBox.about(self, "", "Không tìm thấy process")

    def RequestStart(self, name_to_start):
            state, _ = self.client.MakeRequest('START ' + name_to_start)
            if state == client.ClientState.SUCCEEDED:
                QMessageBox.about(self, "", "Process đã được bật")
            else:
                QMessageBox.about(self, "", "Không tìm thấy process")

    def ShowWindow(self):
        self.setupUI()
        self.show()
        pass


class ApplicationUI(ProcessUI):
    def __init__(self, parent, client):
        super().__init__(parent, client)
        self.baseRequest = "APPLICATION"
        self.windowName = "Application"
        self.headings = ('Application Name', 'Process ID', 'Thread Count')

if __name__ == '__main__':
    from os import environ

    def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"

    suppress_qt_warnings()

    app = QtWidgets.QApplication(sys.argv)
    demo = ApplicationUI(None)
    demo.setupUI()
    demo.ShowWindow() 
    sys.exit(app.exec_())