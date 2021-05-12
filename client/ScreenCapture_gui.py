import tkinter
from tkinter import filedialog
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk
import PIL

from client import ClientState
from Request_gui import Request

class Screenshot(Request):
    def __init__(self, client):
        super().__init__(client, "SCREENSHOT")
        self.capturedScreen = None

    def OnStartGUI(self):
        self.MainWindow = tkinter.Tk()
        self.MainWindow.geometry("500x420")
        self.MainWindow.title("pic")

        state = self.CaptureScreen()
        if state == True:
            self.ShowWindow()
        else:
            self.MainWindow.destroy()


    def OnExitGUI(self):
        if self.MainWindow:
           self.MainWindow.destroy()
        pass
    
    def ShowWindow(self):
        pic_button1 = tkinter.Button(self.MainWindow, text = "Chụp", command = self.CaptureScreen)
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
        state, rawdata = self.MakeBaseRequest()
        if state == ClientState.NOCONNECTION:
            showinfo(title = '', message = 'Chưa kết nối đến server')
            return False
        elif state != ClientState.SUCCEEDED:
            showinfo(title = '', message = 'Lỗi kết nối đến server')
            return False
        try:
            self.capturedScreen = self.BytesToImage(rawdata)
            image = self.capturedScreen.resize((380,380), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image)
            picture = tkinter.Label(self.MainWindow, image = img)
            picture.place(x = 15, y = 25, height = 380, width = 380)
            
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