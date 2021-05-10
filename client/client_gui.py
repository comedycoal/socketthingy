import tkinter
import client
from ProcessRunning_gui import ProcessRunning
from AppRunning_gui import AppRunning
from Keystroke_gui import Keystroke
from Registry_gui import Registry
from ScreenCapture_gui import Screenshot

def remove_text(event):
    event.widget.delete(0, "end")

program = client.ClientProgram()
process_gui = ProcessRunning()
app_gui = AppRunning()
keystroke_gui = Keystroke()
registry_gui = Registry()
screenshot_gui = Screenshot()

class ClientGUI:

    def __init__(self):
        pass
    # def send():
    #     if not program:
    #         client.MakeRequest()
        

    def check_connection(self):
        self.check_connection = tkinter.Tk()
        self.check_connection.geometry("250x100")
        self.check_connection.title("")

        self.text = tkinter.Label(self.check_connection, text = 'Chưa kết nối đến server').place(x = 20, y = 20)
        self.text = tkinter.Label(self.check_connection, text = 'Lỗi kết nối đến server').place(x = 20, y = 20)
        self.text = tkinter.Label(self.check_connection, text = 'Kết nối đến server thành công').place(x = 20, y = 20)

        self.button = tkinter.Button(self.check_connection, command = self.check_connection.destroy, text = 'OK').place (x = 100, y = 50)
        self.check_connection.mainloop()


    def tmp4(self):
        print('thu 4')

    def connect(self):
        host = self.clientgui_textbox.get()
        program.Connect(host)

    def clientGUI(self):
        self.clientgui = tkinter.Tk()
        self.clientgui.title("Client")

        self.clientgui.geometry("470x400")

        self.clientgui_textbox = tkinter.Entry(self.clientgui)
        self.clientgui_textbox.insert(0, "Nhập IP")
        self.clientgui_textbox.bind("<Button-1>", remove_text)
        self.clientgui_textbox.place(x = 10, y = 20, height = 25, width = 300)
        
        self.clientgui_button1 = tkinter.Button(self.clientgui, text = 'Kết nối', bg = 'lightgray', command = self.connect)
        self.clientgui_button1.place(x = 320, y = 20, height = 25, width = 120)

        self.clientgui_button2 = tkinter.Button(self.clientgui, text = 'Process Running', wraplength = 60, command = process_gui.process)
        self.clientgui_button2.place(x = 10, y = 65, height = 300, width = 100)

        self.clientgui_button3 = tkinter.Button(self.clientgui, text = 'App Running', command = app_gui.application)
        self.clientgui_button3.place(x = 120, y = 65, height = 100, width = 190)

        self.clientgui_button4 = tkinter.Button(self.clientgui, text = 'Tắt máy', wraplength = 30, command = self.tmp4)
        self.clientgui_button4.place(x = 120, y = 175, height = 80, width = 70)

        self.clientgui_button5 = tkinter.Button(self.clientgui, text = 'Chụp màn hình', command = screenshot_gui.pic)
        self.clientgui_button5.place(x = 200, y = 175, height = 80, width = 110)

        self.clientgui_button6 = tkinter.Button(self.clientgui, text = 'Sửa registry', command = registry_gui.registry)
        self.clientgui_button6.place(x = 120, y = 265, height = 100, width = 250)

        self.clientgui_button7 = tkinter.Button(self.clientgui, text = 'Keystroke', command = keystroke_gui.keystroke)
        self.clientgui_button7.place(x = 320, y = 65, height = 190, width = 120)

        self.clientgui_button8 = tkinter.Button(self.clientgui, text = 'Thoát', command = self.clientgui.destroy)
        self.clientgui_button8.place(x = 380, y = 265, height = 100, width = 60)

        self.clientgui.mainloop()

if __name__ == '__main__':
    a = ClientGUI()
    a.clientGUI()