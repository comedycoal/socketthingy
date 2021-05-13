import tkinter
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk

from client import ClientState
from Request_gui import Request

class Screenshot(Request):
    def __init__(self, client):
        super().__init__(client, "SCREENSHOT")
        self.capturedScreen = None
        self.a = None

    def __del__(self):
        if self.capturedScreen:
            self.capturedScreen.close()

    def OnStartGUI(self):
        self.OnExitGUI()
        self.ShowWindow()
        pass

    def OnExitGUI(self):
        if self.MainWindow:
           self.MainWindow.destroy()
        if self.capturedScreen:
           self.capturedScreen.close()
        pass
    
    def ShowWindow(self):
        self.MainWindow = tkinter.Toplevel()
        self.MainWindow.geometry("500x420")
        self.MainWindow.title("pic")

        self.CaptureScreen()

        showthis = ImageTk.PhotoImage(self.capturedScreen.resize((380,380), Image.ANTIALIAS))
        self.image = tkinter.Label(self.MainWindow, height = 380, width = 380, image=showthis)
        self.image.place(x = 15, y = 25, height = 380, width = 380)

        pic_button1 = tkinter.Button(self.MainWindow, text = "Chụp", command = self.OnStartGUI)
        pic_button1.place(x = 400, y = 25 , height = 260, width = 90)

        pic_button2 = tkinter.Button(self.MainWindow, text = "Lưu", command = self.SavePicture)
        pic_button2.place(x = 400, y = 310 , height = 95, width = 90)

        self.MainWindow.protocol('WM_DELETE_WINDOW', self.OnExitGUI)
        self.MainWindow.mainloop()

    def BytesToImage(self, rawdata:bytes):
        split = rawdata.split(b' ', 2)
        w = int(split[0].decode("utf-8"))
        h = int(split[1].decode("utf-8"))
        pixels = split[2]
        image = Image.frombytes("RGB", (w, h), pixels)
        return image

    def CaptureScreen(self):
        '''
        Signal server to capture its screen and send back.
        Data is then processed and save into a PIL Image object,
        which in turns is attached to self.captureScreen variable

        Returns:
            True: if everything happened impeccably
            False: if any errors occurs, self.capturedScreen will be None
        '''
        if self.capturedScreen:
            self.capturedScreen.close()
            self.capturedScreen = None

        state = ClientState.SUCCEEDED
        rawdata = None
        state, rawdata = self.MakeBaseRequest()
        if state == ClientState.NOCONNECTION:
            showinfo(title = '', message = 'Chưa kết nối đến server')
            return False
        elif state != ClientState.SUCCEEDED:
            showinfo(title = '', message = 'Lỗi kết nối đến server')
            return False

        try:
            self.capturedScreen = self.BytesToImage(rawdata)
            return True
        except Exception as e:
            showinfo(title = '', message = e)
            return False

    def SavePicture(self):
        imagename = filedialog.asksaveasfilename(initialdir = 'C:', title = 'Save As', 
            filetypes = (('all files', '*.*'), ('png files', '*.png'), ('bmp files', '*.bmp'), ('jpg files', '*.jpg')))
        self.capturedScreen.save(imagename)
        pass


if __name__ == '__main__':
    a = Screenshot(None)
    a.OnStartGUI()