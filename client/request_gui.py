from PySide2 import QtGui, QtWidgets
from client import ClientState
from typing import Text
import client

class Request(QtWidgets.QWidget):
    def __init__(self, parentWindow, clientProgram:client.ClientProgram, baseRequest:str):
        super().__init__()
        self.parentWindow = parentWindow
        self.client = clientProgram
        self.baseRequest = baseRequest

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        close = QtWidgets.QMessageBox.question(self, "Thoát", "Bạn chắc chắn muốn thoát?", 
                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            self.OnExitGUI()
        else:
            event.ignore()

    #Override this if Screenshot_GUI since extraData needs processing
    def OnStartGUI(self):
        state, _ = self.MakeBaseRequest()

        if state == ClientState.NOCONNECTION:
            QtWidgets.QMessageBox.about(self, "", "Chưa kết nối đến server")
            return False
        elif state != ClientState.SUCCEEDED:
            QtWidgets.QMessageBox.about(self, "", "Thao tác thất bại")
            return False

        self.parentWindow.hide()
        self.ShowWindow()

        return True

    def OnExitGUI(self):
        state = self.MakeFinishRequest()
        if self:
            self.CleanUp()
            self.close()
            self.parentWindow.HandleChildUIClose(self.baseRequest)
            self.parentWindow.show()

    def MakeBaseRequest(self):
        state, _ = self.client.MakeRequest(self.baseRequest)
        return state, _

    def MakeFinishRequest(self):
        state, _ = self.client.MakeRequest("FINISH")
        return state

    def ShowWindow(self):
        pass

    def CleanUp(self):
        pass