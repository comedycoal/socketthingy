from os import close
from posixpath import expanduser
import sys
import re
from tkinter.constants import S
from PySide2 import QtGui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from client import ClientState
import json
from request_gui import RequestUI
import client


class MySortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, source_left, source_right):
        if source_left.child(0,0).data() is None:
            if source_right.child(0,0).data() is not None:
                return False
        if source_left.child(0,0).data() is not None:
            if source_right.child(0,0).data() is None:
                return True
        data_left = source_left.data()
        data_right = source_right.data()
        print("left data: " ,data_left)
        print("right data: " ,data_right)
        if type(data_left) == type(data_right) == str:
            return self.fname(data_left) < self.fname(data_right)
        return super(MySortFilterProxyModel, self).lessThan(source_left, source_right)

    # def greaterThan(self, source_left, source_right):
    #     if source_left.child(0,0).data() is None:
    #         if source_right.child(0,0).data() is not None:
    #             return True
    #     data_left = source_left.data()
    #     data_right = source_right.data()
    #     if type(data_left) == type(data_right) == str:
    #         return self.fname(data_left) > self.fname(data_right)
    #     return super(MySortFilterProxyModel, self).greaterThan(source_left, source_right)

    @staticmethod
    def fname(key):
        parts = re.split(r'(\d*\.\d+|\d+)', key)
        parts[0] = parts[0].upper()
        return tuple((e.swapcase() if i % 2 == 0 else float(e))
                for i, e in enumerate(parts))

class DirectoryUI(RequestUI):
    def __init__(self, parentWindow, client):
        super().__init__(parentWindow, client, 'DIRECTORY')
        self.listIndex = []
        self.request_cut = "CUT"
        self.request_copy = "COPY"
        self.cut_index = []
        self.copy_index = []
        self.cur_index = None

    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Directory"))
        self.resize(800,600)

        # self.find_label = QLabel()
        # font = QtGui.QFont()
        # font.setFamily("Helvetica")
        # font.setPointSize(12)
        # self.find_label.setFont(font)
        # self.find_label.setObjectName("find_label")
        # self.find_label.setText(QCoreApplication.translate("MainWindow","Find:"))

        # self.txtFind = QLineEdit()
        # self.txtFind.textChanged[str].connect(self.onFind)
        # font = QtGui.QFont()
        # font.setFamily("Helvetica")
        # font.setPointSize(12)
        # self.txtFind.setFont(font)
        # self.txtFind.setObjectName("txtFind")

        # self.thumbnail = QLabel()
        # self.thumbnail.setText("Dir: ")
        # self.find_label.hide()
        # self.txtFind.hide()
        self.leftTree = QTreeView()
        self.createLeftTree()
        self.treeView = QTreeView()

        self.client_request_label = QLabel()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.client_request_label.setFont(font)
        self.client_request_label.setAlignment(Qt.AlignCenter)
        self.client_request_label.setObjectName("client_request_label")
        self.client_request_label.setText(QCoreApplication.translate("MainWindow","Client Request:"))

        self.transfer_button = QPushButton(clicked = self.onTransfer)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.transfer_button.setFont(font)
        self.transfer_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.transfer_button.setObjectName("transfer_button")
        self.transfer_button.setText(QCoreApplication.translate("MainWindow", "Chuyển file"))

        # self.copy_button = QPushButton(clicked = lambda: self.onCopy())
        # font = QtGui.QFont()
        # font.setFamily("Helvetica")
        # font.setPointSize(12)
        # self.copy_button.setFont(font)
        # self.copy_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        # self.copy_button.setObjectName("copy_button")
        # self.copy_button.setText(QCoreApplication.translate("MainWindow", "Copy"))

        # self.cut_button = QPushButton(clicked = lambda: self.onCut())
        # font = QtGui.QFont()
        # font.setFamily("Helvetica")
        # font.setPointSize(12)
        # self.cut_button.setFont(font)
        # self.cut_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        # self.cut_button.setObjectName("cut_button")
        # self.cut_button.setText(QCoreApplication.translate("MainWindow", "Cut"))

        # self.paste_button = QPushButton()
        # font = QtGui.QFont()
        # font.setFamily("Helvetica")
        # font.setPointSize(12)
        # self.paste_button.setFont(font)
        # self.paste_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        # self.paste_button.setObjectName("paste_button")
        # self.paste_button.setText(QCoreApplication.translate("MainWindow", "Paste"))

        # findLayout = QHBoxLayout()
        # findLayout.addWidget(self.find_label)
        # findLayout.addSpacing(10)
        # findLayout.addWidget(self.txtFind)

        mainLayout = QGridLayout()
        mainLayout.setHorizontalSpacing(15)
        mainLayout.setVerticalSpacing(10)
        # mainLayout.addItem(findLayout)
        # mainLayout.addWidget(self.thumbnail)
        mainLayout.addWidget(self.leftTree, 0, 0, Qt.AlignLeft| Qt.AlignTop)
        mainLayout.addWidget(self.transfer_button, 1, 0, Qt.AlignCenter | Qt.AlignTop)
        mainLayout.addWidget(QLabel(), 2, 0)
        mainLayout.addWidget(QLabel(), 3, 0)
        mainLayout.addWidget(self.treeView, 0, 1, 4, 3)

        # mainLayout = QVBoxLayout()

        # splitterHLeft = QSplitter(Qt.Vertical)
        # splitterHLeft.addWidget(self.leftTree)

        # buttonLayoutFrame = QFrame()
        # buttonLayoutFrame.setFrameShape(QFrame.StyledPanel)
        # buttonLayout = QVBoxLayout()
        # buttonLayout.addWidget(self.transfer_button)
        # buttonLayoutFrame.setLayout(buttonLayout)
        # splitterHLeft.addWidget(buttonLayoutFrame)

        # splitterVMid = QSplitter(Qt.Horizontal)
        # splitterVMid.addWidget(splitterHLeft)
        # splitterVMid.addWidget(self.treeView)

        # # mainLayout.addItem(findLayout)
        # # mainLayout.addWidget(self.thumbnail)
        # mainLayout.addWidget(self.client_request_label)
        # mainLayout.addWidget(splitterVMid)

        self.setLayout(mainLayout)

    def createLeftTree(self):
        self.leftmodel = QStandardItemModel(0, 1)
        self.leftmodel.setHeaderData(0,Qt.Horizontal, "Disk:")
        listdisk = []
        for disk in range(ord('A'), ord('Z') + 1, 1):
            disk = str(chr(disk))
            state, rawdata = self.client.MakeRequest("VIEW " + "\"" + disk + ":\\\"")
            if state == ClientState.SUCCEEDED:
                listitem = json.loads(rawdata)
                if listitem:
                    path = disk + ":\\"
                    listdisk.append(path)

        while listdisk:
            self.leftmodel.insertRow(0)
            self.leftmodel.setItem(0, QStandardItem(listdisk.pop()))
        self.leftTree.setModel(self.leftmodel)
        self.leftTree.setMinimumWidth(70)
        self.leftTree.clicked.connect(self.onleftTreeClick)

    def onleftTreeClick(self, index):
        path = index.data()
        self.createDirectoryModel(path)
        return index

    def createDirectoryModel(self, path):
        state, rawdata = self.client.MakeRequest("VIEW " + "\"" + path + "\"")
        if state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Không thể tải dữ liệu")
            return

        self.model = QStandardItemModel(0, 1)
        self.model.setHeaderData(0,Qt.Horizontal, path)
        # self.thumbnail.setText("Dir:    D:")

        self.listIndex.clear()
        itemlist = json.loads(rawdata)
        for item, ftype in itemlist:
            self.model.insertRow(0)
            node = QStandardItem(item)
            if ftype == 1:
                node.appendRow(QStandardItem(None))
            self.model.setItem(0, node)

        self.proxyModel = MySortFilterProxyModel(recursiveFilteringEnabled = True)
        self.proxyModel.invalidateFilter()
        self.proxyModel.setSourceModel(self.model)
        self.createDirectoryTree()

    def createDirectoryTree(self):
        self.treeView.setModel(self.proxyModel)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setSortingEnabled(True)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.showContextMenu)
        self.treeView.clicked.connect(self.onTreeViewClicked)

    def addItemToModel(self, index):
        filePath = self.findFilePath(index)
        state, rawdata = self.client.MakeRequest("VIEW " + filePath)
        if state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Không thể tải dữ liệu")
            return

        nameList = json.loads(rawdata)
        root = self.model.itemFromIndex(index)
        # print("root:", root.row(),root.column())
        # if root.parent():
        #     print("root_parent:", root.parent().row(),root.parent().column())
        if nameList:
            if not root.child(0,0).index().data():
                root.removeRow(0)

        for item, ftype in nameList:
            node = QStandardItem(item)
            if ftype == 1:
                node.appendRow(QStandardItem(None))
            root.appendRow(node)
            root.setChild(node.row(), node)
            # print("node:", node.column(), node.row())
            # print("parent_node:", node.parent().column(), node.parent().row())

    def findFilePath(self, index):
        tmp_index = index
        filePath = "\""
        folderList = []
        while tmp_index.row() != -1 and tmp_index.column() != -1:
            # print("index truyen vao:", index.row(),index.column())
            # print("tmp_index:", tmp_index.row(),tmp_index.column())
            folderList.append(tmp_index.data())
            # print("folderList:", folderList)
            tmp_index = tmp_index.parent()
        while folderList:
            cur = folderList.pop()
            filePath = filePath + cur
            if folderList:
                filePath = filePath + "\\"
            # print("filePath:", filePath)
        filePath = filePath + "\""
        # print("filePath:", filePath)
        return filePath

    def onTreeViewClicked(self, index):
        # print("index: ", index.row(), index.column())
        source_index = self.proxyModel.mapToSource(index)
        self.cur_index = source_index
        # print("source index:", source_index.row(), source_index.column())
        # print("source_parent_index:", source_index.parent().row(), source_index.parent().column())
        self.treeView.expand(index)
        self.treeView.expand(source_index)
        # path = self.findFilePath(source_index)
        # self.thumbnail.setText("Dir:    D:\\" + path.strip("\""))
        if source_index not in self.listIndex:
            self.listIndex.append(source_index)
            self.addItemToModel(source_index)
        return source_index

    # def onFind(self):
    #     self.proxyModel.setFilterWildcard("*{}*".format(self.txtFind.text()))
    #     pass

    def showContextMenu(self, point):
        ix = self.treeView.indexAt(point)
        if ix.column() == 0:
            menu = QMenu(self.treeView)
            menu.addAction("Copy")
            menu.addAction("Cut")
            menu.addAction("Patse")
            # menu.addAction("Rename")
            menu.addAction("Delete")
            action = menu.exec_(self.treeView.mapToGlobal(point))
            tmp_index = self.treeView.indexAt(point)
            index = self.proxyModel.mapToSource(tmp_index)
            if action:
                if action.text() == "Copy":
                    self.request_copy = self.request_copy + " " + self.findFilePath(index)
                    self.copy_index.append(index)
                    # print("self.request_copy:", self.request_copy)
                    pass
                if action.text() == "Cut":
                    self.request_cut = self.request_cut + " " + self.findFilePath(index)
                    self.cut_index.append(index)
                    # print("self.request_cut:", self.request_cut)
                    pass
                if action.text() == "Patse":
                    # print("self.request_copy", self.request_copy)
                    # print("self.request_cut:", self.request_cut)

                    self.RequestCopy_Cut(self.request_copy, index)
                    self.RequestCopy_Cut(self.request_cut, index)
                    self.request_cut = "CUT"
                    self.request_copy = "COPY"

                    root = self.model.itemFromIndex(index)
                    while self.copy_index:
                        ix = self.copy_index.pop()
                        it = ix.data()
                        newitem = QStandardItem(it)
                        root.appendRow(newitem)
                        root.setChild(newitem.row(), newitem)
                    while self.cut_index:
                        ix = self.cut_index.pop()
                        it = ix.data()
                        newitem = QStandardItem(it)
                        root.appendRow(newitem)
                        root.setChild(newitem.row(), newitem)
                        self.model.removeRow(ix.row(), ix.parent())

                if action.text() == "Rename":
                    filePath = self.findFilePath(index)
                    # print("filePath:", filePath)
                    self.treeView.edit(index)
                    newName = index.data()
                    newName = "\"" + newName + "\""
                    self.RequestRename(filePath, newName)

                if action.text() == "Delete":
                    filepath = self.findFilePath(index)
                    self.model.removeRow(index.row(), index.parent())
                    # print("filepath:", filepath)
                    self.RequestDelete(filepath)

    def RequestCopy_Cut(self, request:str, index:QModelIndex):
        if len(request) > 4:
            endPath = self.findFilePath(index)
            request = request + " " + endPath
            # print("request:", request)

            state, _ = self.client.MakeRequest(request)
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

    def onTransfer(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "Choose file", r"C:", "All files(*)", options=options
        )
        bytes_data = None
        if filename:
            with open(filename, "rb") as f:
                f.seek(0,2)
                l = f.tell()
                f.seek(0,0)
                bytes_data = f.read(l)
            f.close()
        fileName = filename.split('/').pop()

        index = self.cur_index
        tmp_index = index
        filePath = "\""
        folderList = []
        while tmp_index.row() != -1 and tmp_index.column() != -1:
            print(folderList)
            folderList.append(tmp_index.data())
            tmp_index = tmp_index.parent()

        while len(folderList) > 1:
            cur = folderList.pop()
            filePath = filePath + cur
            print(folderList)
            filePath = filePath + "\\"
            print(filePath)
        filePath = filePath + fileName + "\""
        print(filePath)

        self.RequestTransfer(filePath, bytes_data)

        index = index.parent()
        root = self.model.itemFromIndex(index)
        root.appendRow(QStandardItem(fileName))

        pass

    def RequestTransfer(self, path, bytes_data):
        state, _ = self.client.MakeRequest("TRANSFER " + path + " " + bytes_data.decode("utf-8"))
        if state != client.ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Error")
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

    app = QApplication(sys.argv)
    demo = DirectoryUI(None, client.ClientProgram())
    demo.setupUI()
    demo.ShowWindow() 
    sys.exit(app.exec_())