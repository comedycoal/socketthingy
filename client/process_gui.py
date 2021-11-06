from PySide2.QtCore import *
from PySide2 import QtGui, QtWidgets
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from client import ClientState
from request_gui import RequestUI
import json

class ProcessUI(RequestUI):
    def __init__(self, parent, client):
        super().__init__(parent, client, 'PROCESS')
        self.windowName = "Process"
        self.headings = ('Process Name', 'Process ID', 'Thread Count')

    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", self.windowName))
        self.resize(550,500)

        self.find_label = QLabel()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        self.find_label.setFont(font)
        self.find_label.setObjectName("find_label")
        self.find_label.setText(QCoreApplication.translate("MainWindow","Find:"))

        self.txtFind = QLineEdit()
        self.txtFind.textChanged[str].connect(self.onFind)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        self.txtFind.setFont(font)
        self.txtFind.setObjectName("txtFind")

        self.treeView = QTreeView()
        self.model =  self.createProcessModel()
        self.createProcessTree(self.model)

        self.kill_button = QtWidgets.QPushButton(clicked = lambda:self.onKill())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        self.kill_button.setFont(font)
        self.kill_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.kill_button.setObjectName("kill_button")
        self.kill_button.setText(QCoreApplication.translate("MainWindow", "Kill"))

        self.reload_button = QtWidgets.QPushButton(self, clicked = lambda:self.viewProcessTree())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        self.reload_button.setFont(font)
        self.reload_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.reload_button.setObjectName("reload_button")
        self.reload_button.setText(QCoreApplication.translate("MainWindow", "Refresh"))

        self.name_start_label = QLabel()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        self.name_start_label.setFont(font)
        self.name_start_label.setObjectName("name_start_label")
        self.name_start_label.setText(QCoreApplication.translate("MainWindow","Name of Program:"))

        self.name_start_box = QLineEdit()
        self.name_start_box = QLineEdit()
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        self.name_start_box.setFont(font)
        self.name_start_box.setObjectName("name_start_box")

        self.start_button = QtWidgets.QPushButton(self, clicked = lambda:self.onStart())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(11)
        self.start_button.setFont(font)
        self.start_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.start_button.setObjectName("start_button")
        self.start_button.setText(QCoreApplication.translate("MainWindow", "Start"))

        findLayout = QHBoxLayout()
        findLayout.addWidget(self.find_label)
        findLayout.addSpacing(10)
        findLayout.addWidget(self.txtFind)
        # findLayout.addSpacing(10)
        # findLayout.addWidget(self.kill_button)
        # findLayout.addSpacing(10)
        # findLayout.addWidget(self.start_button)

        reloadLayout = QGridLayout()
        reloadLayout.setHorizontalSpacing(5)
        reloadLayout.setVerticalSpacing(10)
        reloadLayout.addWidget(self.reload_button, 0,3)
        reloadLayout.addWidget(self.name_start_label, 1,0)
        reloadLayout.addWidget(self.name_start_box, 1,1)
        reloadLayout.addWidget(self.start_button, 1,3)

        mainLayout = QVBoxLayout()
        mainLayout.addItem(findLayout)
        mainLayout.addWidget(self.treeView)
        mainLayout.addSpacing(5)
        mainLayout.addItem(reloadLayout)

        self.setLayout(mainLayout)

    def createProcessTree(self, model):
        self.treeView.setModel(model)
        self.treeView.setColumnWidth(0, 300)
        self.treeView.setColumnWidth(1, 100)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setSortingEnabled(True)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.showContextMenu)

    def createProcessModel(self):
        state, rawdata = self.client.MakeRequest('FETCH')
        if state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Không thể tải dữ liệu")
            return

        model = QStandardItemModel(0, 3, self.treeView)
        model.setHeaderData(0, Qt.Horizontal, self.headings[0])
        model.setHeaderData(1, Qt.Horizontal, self.headings[1])
        model.setHeaderData(2, Qt.Horizontal, self.headings[2])

        self.itemlist = json.loads(rawdata)
        self.addItem(model)

        proxy_model = QSortFilterProxyModel(recursiveFilteringEnabled = True)
        proxy_model.setSourceModel(model)
        return proxy_model

    def addItem(self, model):
        for item in self.itemlist:
            model.insertRow(0)
            model.setData(model.index(0, 0), item["name"])
            model.setData(model.index(0, 1), item["pid"])
            model.setData(model.index(0, 2), item["num_threads"])

    def viewProcessTree(self):
        self.model = self.createProcessModel()
        self.treeView.setModel(self.model)

    def onKill(self):
        index = self.treeView.selectedIndexes()[0]
        item = self.model.itemData(index)
        id_to_kill = self.findIDbyName(item[0])
        self.RequestKill(id_to_kill)
        self.viewProcessTree()

    def findIDbyName(self, name):
        for item in self.itemlist:
            if name == item["name"]:
                return str(item["pid"])
        return ""

    def onStart(self):
        item = self.name_start_box.text()
        self.RequestStart(item)
        self.viewProcessTree()

    def onFind(self):
        self.model.setFilterWildcard("*{}*".format(self.txtFind.text()))

    def showContextMenu(self, point):
        ix = self.treeView.indexAt(point)
        menu = QMenu(self.treeView)
        menu.addAction("Kill")
        action = menu.exec_(self.treeView.mapToGlobal(point))
        if action:
            if action.text() == "Kill":
                self.onKill()

    def RequestKill(self, id_to_kill):
        state, _ = self.client.MakeRequest("KILL " + id_to_kill)
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
    import sys
    import client

    def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"

    suppress_qt_warnings()

    app = QtWidgets.QApplication(sys.argv)
    demo = ApplicationUI(None, client.ClientProgram())
    demo.ShowWindow() 
    sys.exit(app.exec_())