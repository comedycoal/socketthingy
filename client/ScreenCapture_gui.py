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

    def OnStartGUI(self):
        state = self.CapScreen()

        self.ShowWindow()

    def OnExitGUI(self):
        if self.MainWindow:
           self.MainWindow.destroy()
        pass
    
    def ShowWindow(self):
        self.MainWindow = tkinter.Tk()
        self.MainWindow.geometry("500x420")
        self.MainWindow.title("pic")

        pic_canvas = tkinter.Canvas(self.MainWindow)
        pic_canvas.place(x = 15, y = 25, height = 380, width = 380)

        pic_button1 = tkinter.Button(self.MainWindow, text = "Chụp", command = self.CapScreen)
        pic_button1.place(x = 400, y = 25 , height = 260, width = 90)

        pic_button2 = tkinter.Button(self.MainWindow, text = "Lưu", command = self.SavePic)
        pic_button2.place(x = 400, y = 310 , height = 95, width = 90)

        self.MainWindow.protocol('WM_DELETE_WINDOW', self.OnExitGUI)
        self.MainWindow.mainloop()

    def BytesToImage(self, bytesData:bytes):
        #để t handle
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
