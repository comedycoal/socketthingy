from client import ClientState
import tkinter
from Request_gui import Request
program = None

def remove_text(event):
        event.widget.delete(0, "end")

class Keystroke(Request):
    def __init__(self, client):
        super().__init__(client, "KEYLOG")

    def ShowWindow(self):
        self.MainWindow = tkinter.Tk()
        self.MainWindow.title("Keystroke")

        self.MainWindow.geometry("470x400")
        
        self.keystroke_listbox = tkinter.Listbox(self.MainWindow)
        self.keystroke_listbox.place(x = 30 , y = 80, height = 300, width = 420)

        self.HookButton = tkinter.Button(self.MainWindow, text = 'Hook', command = self.OnHookButton)
        self.HookButton.place(x = 30, y = 10, height = 60, width = 100)

        self.UnHookButton = tkinter.Button(self.MainWindow, text = 'Unhook', command = self.OnUnhookButton)
        self.UnHookButton.place(x = 140, y = 10, height = 60, width = 90)

        self.PrintButton = tkinter.Button(self.MainWindow, text = 'In phím', command = self.OnPrintButton)
        self.PrintButton.place(x = 240, y = 10, height = 60, width = 100)

        self.ClaerButton = tkinter.Button(self.MainWindow, text = 'Xóa', command = self.OnClearButton)
        self.ClaerButton.place(x = 350, y = 10, height = 60, width = 100)

        self.MainWindow.protocol('WM_DELETE_WINDOW', self.OnExitGUI)
        self.MainWindow.mainloop()

    def OnHookButton(self):
        state, _ = self.client.MakeRequest("HOOK")
        if state == ClientState.SUCCEEDED:
            # In "Hook đã được cài" ra cái ô to to
            pass
        else:
            # In "Lỗi"
            pass
        
        return None

    def OnUnhookButton(self):
        state, _ = self.client.MakeRequest("UNHOOK")
        if state == ClientState.SUCCEEDED:
            # In "Hook đã được gỡ"
            pass
        else:
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
            
        except Exception as e:
            print(e)
            #In lỗi
            pass

        # for item in texttest:
        #     self.keystroke_listbox.insert('end', item)

    def OnClearButton(self):
        state, _ = self.client.MakeRequest("CLEAR")

        # Xóa chữ

        # for item in range (len(texttest)):
        #     self.keystroke_listbox.delete(0)



texttest = []
for i in range(20):
    texttest.append("hi" + str(i))


if __name__ == "__main__":
    a = Keystroke(None)
    a.ShowWindow()
