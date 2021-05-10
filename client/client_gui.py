import tkinter
import client
import ProcessRunning_gui
import AppRunning_gui
import Keystroke_gui
import ScreenCapture_gui

def remove_text(event):
    event.widget.delete(0, "end")

program = None

def send():
    if not program:
        client.MakeRequest()
    

def check_connection():
    tmp = tkinter.Tk()
    tmp.geometry("250x100")
    tmp.title("")

    text = tkinter.Label(tmp, text = 'Chưa kết nối đến server').place(x = 20, y = 20)
    text = tkinter.Label(tmp, text = 'Lỗi kết nối đến server').place(x = 20, y = 20)
    text = tkinter.Label(tmp, text = 'Kết nối đến server thành công').place(x = 20, y = 20)

    button = tkinter.Button(tmp, command = tmp.destroy, text = 'OK').place (x = 100, y = 50)
    tmp.mainloop()


def tmp4():
    print('thu 4')

def connect():
    host = textbox.get()
    port = 6666
    program = client.ClientProgram(host, port)
    #program.Run()

def tmp6():
    print('thu 6')

if __name__ == "__main__":
    clientgui = tkinter.Tk()
    clientgui.title("Client")

    clientgui.geometry("470x400")

    clientgui_textbox = tkinter.Entry(clientgui)
    clientgui_textbox.insert(0, "Nhập IP")
    clientgui_textbox.bind("<Button-1>", remove_text)
    clientgui_textbox.place(x = 10, y = 20, height = 25, width = 300)
    
    clientgui_button1 = tkinter.Button(clientgui, text = 'Kết nối', bg = 'lightgray', command = connect)
    clientgui_button1.place(x = 320, y = 20, height = 25, width = 120)

    clientgui_button2 = tkinter.Button(clientgui, text = 'Process Running', wraplength = 60, command = ProcessRunning_gui.process)
    clientgui_button2.place(x = 10, y = 65, height = 300, width = 100)

    clientgui_button3 = tkinter.Button(clientgui, text = 'App Running', command = AppRunning_gui.appRunning)
    clientgui_button3.place(x = 120, y = 65, height = 100, width = 190)

    clientgui_button4 = tkinter.Button(clientgui, text = 'Tắt máy', wraplength = 30, command = tmp3)
    clientgui_button4.place(x = 120, y = 175, height = 80, width = 70)

    clientgui_button5 = tkinter.Button(clientgui, text = 'Chụp màn hình', command = ScreenCapture_gui.pic)
    clientgui_button5.place(x = 200, y = 175, height = 80, width = 110)

    clientgui_button6 = tkinter.Button(clientgui, text = 'Sửa registry', command = tmp3)
    clientgui_button6.place(x = 120, y = 265, height = 100, width = 250)

    clientgui_button7 = tkinter.Button(clientgui, text = 'Keystroke', command = Keystroke_gui.keystroke)
    clientgui_button7.place(x = 320, y = 65, height = 190, width = 120)

    clientgui_button8 = tkinter.Button(clientgui, text = 'Thoát', command = clientgui.destroy)
    clientgui_button8.place(x = 380, y = 265, height = 100, width = 60)

    clientgui.mainloop()