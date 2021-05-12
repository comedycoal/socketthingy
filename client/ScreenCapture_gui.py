import tkinter
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo

from PIL import Image

from client import ClientState
from Request_gui import Request

class Screenshot(Request):
    def __init__(self, client):
        super().__init__(client, "SCREENSHOT")
        self.capturedScreen = None

    def BytesToImage(self, bytesData:bytes):
        #để t handle
        pass

    def OnStartGUI(self):
        state = self.CapScreen()

        self.ShowWindow()

    def OnExitGUI(self):
        pass

    def CapScreen(self):
        state, rawdata = self.MakeBaseRequest()
        if state != ClientState.SUCCEEDED:
            showinfo(title = '', message = 'Lỗi kết nối đến server')
            return False

        try:
            self.capturedScreen = self.BytesToImage(rawdata)
            return True
        except Exception as e:
            print(e)
            return False

    def SavePic(self):
        # Làm cái lưu hình đi :v
        pass

    def ShowWindow(self):
        self.mainWindow = tkinter.Tk()
        self.mainWindow.geometry("500x420")
        self.mainWindow.title("pic")

        pic_canvas = tkinter.Canvas(self.mainWindow)
        pic_canvas.place(x = 15, y = 25, height = 380, width = 380)

        pic_button1 = tkinter.Button(self.mainWindow, text = "Chụp", command = self.CapScreen)
        pic_button1.place(x = 400, y = 25 , height = 260, width = 90)

        pic_button2 = tkinter.Button(self.mainWindow, text = "Lưu", command = self.SavePic)
        pic_button2.place(x = 400, y = 310 , height = 95, width = 90)

        self.mainWindow.mainloop()
