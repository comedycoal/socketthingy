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


class DirectoryUI(Request):
    def __init__(self, client):
        super().__init__(client, 'DIRECTORY')

    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Directory"))
        self.resize(500,430)

        self.find_label = QLabel()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.find_label.setFont(font)
        self.find_label.setObjectName("find_label")
        self.find_label.setText(QCoreApplication.translate("MainWindow","Find:"))

        self.txtFind = QLineEdit()
        self.txtFind.textChanged[str].connect(self.onFind)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.txtFind.setFont(font)
        self.txtFind.setObjectName("txtFind")

        self.createProcessModel()
        self.treeView = QTreeView()
        self.createProcessTree()

        findLayout = QHBoxLayout()
        findLayout.addWidget(self.find_label)
        findLayout.addSpacing(10)
        findLayout.addWidget(self.txtFind)

        self.thumbnail = QLabel()
        self.thumbnail.setText("Dir: ")

        mainLayout = QVBoxLayout()
        mainLayout.addItem(findLayout)
        mainLayout.addWidget(self.thumbnail)
        mainLayout.addWidget(self.treeView)

        self.setLayout(mainLayout)

    def createProcessModel(self):
        state, rawdata = self.client.MakeRequest("VIEW \"D:\\\"")
        if state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Không thể tải dữ liệu")
            return

        self.model = QStandardItemModel(0, 1)

        itemlist = json.loads(rawdata)
        for item in itemlist:
            self.model.insertRow(0)
            node = QStandardItem(item) 
            self.model.setItem(0, node)

        self.proxyModel = QSortFilterProxyModel(recursiveFilteringEnabled = True)
        self.proxyModel.invalidateFilter()
        self.proxyModel.setSourceModel(self.model)

    def createProcessTree(self):
        self.treeView.setModel(self.proxyModel)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setSortingEnabled(True)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.showContextMenu)
        self.treeView.clicked.connect(self.onTreeViewClicked)

    def addItemToModel(self, index):
        folderName = index.data()
        state, rawdata = self.client.MakeRequest("VIEW " + "\"" + folderName.upper() + "\"")
        if state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Không thể tải dữ liệu")
            return

        itemlist = json.loads(rawdata)
        root = self.model.itemFromIndex(index)
        print(root)
        for item in itemlist:
            node = QStandardItem(item)
            root.appendRow(node)
            print(node.row(), node.column())

    def onTreeViewClicked(self, index):
        print(index.row(), index.column())
        source_index = self.proxyModel.mapToSource(index)
        print(source_index.row(), source_index.column())
        self.addItemToModel(source_index)

    def onFind(self):
        self.proxyModel.setFilterWildcard("*{}*".format(self.txtFind.text()))
        pass

    def showContextMenu(self, point):
        ix = self.treeView.indexAt(point)
        if ix.column() == 0:
            menu = QMenu(self.treeView)
            menu.addAction("Copy")
            menu.addAction("Cut")
            menu.addAction("Patse")
            menu.addAction("Rename")
            menu.addAction("Delete")
            action = menu.exec_(self.treeView.mapToGlobal(point))
            request = ""
            if action:
                if action.text() == "Copy":
                    request = "COPY"
                    self.addRequest(request)
                    pass
                if action.text() == "Cut":
                    request = "CUT"
                    pass
                if action.text() == "Patse":
                    self.RequestCopy_Cut(request)
                    pass
                if action.text() == "Rename":
                    request = "RENAME"
                    self.RequestRename()
                    pass
                if action.text() == "Delete":
                    self.RequestDelete()
                    pass

    def addRequest(self, request):
        index = self.treeView.selectedIndexes()[0]
        item = self.model.itemData(index)
        return request
        pass

    def RequestCopy_Cut(self, request):
        state, _ = self.client.MakeRequest("COPY " + request)
        if state != client.ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Error")

    def RequestDelete(self, path):
        state, _ = self.client.MakeRequest("DELETE " + path)
        if state != client.ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Error")

    def RequestRename(self, path, name):
        state, _ = self.client.MakeRequest("RENAME " + path + " " + name)
        if state != client.ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Error")

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
    demo = DirectoryUI(None)
    demo.setupUI()
    demo.ShowWindow() 
    sys.exit(app.exec_())