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
        
        self.KeyBox = tkinter.Text(self.MainWindow)
        self.KeyBox.place(x = 30 , y = 80, height = 300, width = 420)
        self.KeyBox.configure(state='disabled')

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
            self.PutTextWithNewLine('Hook đã được cài')
        else:
            self.PutTextWithNewLine('Lỗi')
        
        return None

    def OnUnhookButton(self):
        state, _ = self.client.MakeRequest("UNHOOK")
        if state == ClientState.SUCCEEDED:
            self.PutTextWithNewLine('Hook đã được gỡ')
        else:
            self.PutTextWithNewLine('Lỗi')
        return None

    def OnPrintButton(self):
        state, data = self.client.MakeRequest("FETCH")
        try:
            assert state == ClientState.SUCCEEDED, "KEYLOG FETCH request failed"
            assert data, "No data retrieved"
            data = data.decode("utf-8")
            self.PutTextWithNewLine(data)
        except Exception as e:
            self.PutTextWithNewLine(e)

    def OnClearButton(self):
        state, _ = self.client.MakeRequest("CLEAR")
        self.ClearText()

    def PutTextWithNewLine(self, text):
        self.KeyBox.configure(state="normal")
        self.KeyBox.insert(tkinter.END, text + '\n')
        self.KeyBox.configure(state='disabled')

    def ClearText(self):
        self.KeyBox.configure(state='normal')
        self.KeyBox.delete("1.0", tkinter.END)
        self.KeyBox.configure(state='disabled')



if __name__ == "__main__":
    a = Keystroke(None)
    a.ShowWindow()
