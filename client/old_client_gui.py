import tkinter
from tkinter.messagebox import showinfo

from client import ClientState
from client import ClientProgram

from ProcessRunning_gui import ProcessRunning, ApplicationRunning
from Keystroke_gui import Keystroke
from Registry_gui import Registry
from ScreenCapture_gui import Screenshot

class ClientGUI():
    def __init__(self):   
        self.clientProgram = ClientProgram()
        self.process_gui = ProcessRunning(self.clientProgram)
        self.app_gui = ApplicationRunning(self.clientProgram)
        self.keystroke_gui = Keystroke(self.clientProgram)
        self.registry_gui = Registry(self.clientProgram)
        self.screenshot_gui = Screenshot(self.clientProgram)
        pass

    def Connect(self, host):
        state = self.clientProgram.Connect(host)
        if state == True:
            showinfo(title = '', message = 'Kết nối đến server thành công')
        else:
            showinfo(title = '', message = 'Lỗi kết nối đến server')

    def Disconnect(self):
        self.clientProgram.Disconnect()

    def OnShutdownButton(self):
        state, _ = self.clientProgram.MakeRequest("SHUTDOWN")
        if state == ClientState.SUCCEEDED:
            showinfo(title = '', message = 'Thực hiện thành công')
            self.Disconnect()
        else:
            showinfo(title = '', message = 'Lỗi kết nối đến server')

    def OnExitButton(self):
        state, _ = self.clientProgram.MakeRequest("EXIT")
        if state == ClientState.SUCCEEDED:
            self.Disconnect()
            showinfo(title = '', message = 'Thực hiện thành công')
            pass
        else:
            showinfo(title = '', message = 'Lỗi kết nối đến server')
            pass
        #self.ClientWindow.destroy()

    def ShowWindow(self):
        self.ClientWindow = tkinter.Tk()
        self.ClientWindow.title("Client")

        self.ClientWindow.geometry("470x400")

        IPBox = tkinter.Entry(self.ClientWindow)
        IPBox.insert(0, "Nhập IP")
        IPBox.place(x = 10, y = 20, height = 25, width = 300)
        
        clientgui_button1 = tkinter.Button(self.ClientWindow, text = 'Kết nối', command = lambda: self.Connect(IPBox.get()))
        clientgui_button1.place(x = 320, y = 20, height = 25, width = 120)

        clientgui_button2 = tkinter.Button(self.ClientWindow, text = 'Process Running', wraplength = 60, command = self.process_gui.OnStartGUI)
        clientgui_button2.place(x = 10, y = 65, height = 300, width = 100)

        clientgui_button3 = tkinter.Button(self.ClientWindow, text = 'App Running', command = self.app_gui.OnStartGUI)
        clientgui_button3.place(x = 120, y = 65, height = 100, width = 190)

        clientgui_button4 = tkinter.Button(self.ClientWindow, text = 'Tắt máy', wraplength = 30, command = self.OnShutdownButton)
        clientgui_button4.place(x = 120, y = 175, height = 80, width = 70)

        clientgui_button5 = tkinter.Button(self.ClientWindow, text = 'Chụp màn hình', command = self.screenshot_gui.OnStartGUI)
        clientgui_button5.place(x = 200, y = 175, height = 80, width = 110)

        clientgui_button6 = tkinter.Button(self.ClientWindow, text = 'Sửa registry', command = self.registry_gui.OnStartGUI)
        clientgui_button6.place(x = 120, y = 265, height = 100, width = 250)

        clientgui_button7 = tkinter.Button(self.ClientWindow, text = 'Keystroke', command = self.keystroke_gui.OnStartGUI)
        clientgui_button7.place(x = 320, y = 65, height = 190, width = 120)

        clientgui_button8 = tkinter.Button(self.ClientWindow, text = 'Thoát', command = self.OnExitButton)
        clientgui_button8.place(x = 380, y = 265, height = 100, width = 60)

        self.ClientWindow.mainloop()

if __name__ == '__main__':
    a = ClientGUI()
    a.ShowWindow()