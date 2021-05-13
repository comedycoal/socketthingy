from client import ClientState
import tkinter
from typing import Text
import client
from tkinter import Tk, ttk
from tkinter.messagebox import showinfo

class Request:
    def __init__(self, clientProgram:client.ClientProgram, baseRequest:str):
        self.MainWindow = None
        self.client = clientProgram
        self.baseRequest = baseRequest

    #Override this if Screenshot_GUI since extraData needs processing
    def OnStartGUI(self):
        state, _ = self.MakeBaseRequest()
        
        if state == ClientState.NOCONNECTION:
            showinfo(title = '', message = 'Chưa kết nối đến server')
            return False
        elif state != ClientState.SUCCEEDED:
            showinfo(title = '', message = 'Lỗi kết nối đến server')
            return False
        
        self.ShowWindow()
        return True

    def OnExitGUI(self):
        state = self.MakeFinishRequest()
        if self.MainWindow:
           self.MainWindow.destroy()

    def MakeBaseRequest(self):
        state, _ = self.client.MakeRequest(self.baseRequest)
        return state, _   

    def MakeFinishRequest(self):
        state, _ = self.client.MakeRequest("FINISH")
        return state

    def ShowWindow(self):
        pass