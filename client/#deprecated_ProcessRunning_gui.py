from client import ClientState
import tkinter
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
import json
from Request_gui import Request
import client

class ProcessRunning(Request):
    def __init__(self, client):
        super().__init__(client, 'PROCESS')
        self.windowName = "Process"
        self.headings = ('Process Name', 'Process ID', 'Thread Count')
        pass
    
    def ShowWindow(self):
        self.MainWindow = tkinter.Tk()
        self.MainWindow.title(self.windowName)
        self.MainWindow.geometry("470x400")

        self.process_tree = ttk.Treeview(self.MainWindow, columns = self.headings, show = 'headings')
        self.process_tree.heading(self.headings[0], text = self.headings[0])
        self.process_tree.column(self.headings[0], width = 140)
        self.process_tree.heading(self.headings[1], text = self.headings[1])
        self.process_tree.column(self.headings[1], width = 80)
        self.process_tree.heading(self.headings[2], text = self.headings[2])
        self.process_tree.column(self.headings[2], width = 100)
        self.tree_scrollbar = ttk.Scrollbar(self.MainWindow, orient = "vertical", command = self.process_tree.yview)
        self.process_tree.config(yscrollcommand = self.tree_scrollbar.set)
        self.process_tree.place(x = 30, y = 80, height = 300, width = 420)
        self.tree_scrollbar.place(x = 435, y = 80, height = 300, width = 15)

        process_button1 = tkinter.Button(self.MainWindow, text = 'Kill', command = self.OnKillButton)
        process_button1.place(x = 30, y = 10, height = 60, width = 100)

        process_button2 = tkinter.Button(self.MainWindow, text = 'Xem', command = self.OnViewButton)
        process_button2.place(x = 140, y = 10, height = 60, width = 90)

        process_button3 = tkinter.Button(self.MainWindow, text = 'Xóa', command = self.OnEraseButton)
        process_button3.place(x = 240, y = 10, height = 60, width = 100)

        process_button4 = tkinter.Button(self.MainWindow, text = 'Start', command = self.OnStartButton)
        process_button4.place(x = 350, y = 10, height = 60, width = 100)

        self.MainWindow.protocol('WM_DELETE_WINDOW', self.OnExitGUI)

        self.MainWindow.mainloop()
    
    def RequestKill(self, id_to_kill):
        state, _ = self.client.MakeRequest('KILL ' + id_to_kill)
        if state == client.ClientState.SUCCEEDED:
            showinfo(title = '', message = 'Đã diệt process')
        else:
            showinfo(title = '', message = 'Không tìm thấy process')

    def OnKillButton(self):
        killbutton = tkinter.Tk()
        killbutton.title("Kill")
        killbutton.geometry("250x50")

        kill_entry = tkinter.Entry(killbutton)
        kill_entry.insert(0, "Nhập ID")
        kill_entry.place(x = 15, y = 15, height = 25, width = 150)

        kill_button = tkinter.Button(killbutton, text = "Kill", command = lambda:self.RequestKill(kill_entry.get()))
        kill_button.place(x = 180, y = 15, height = 25, width = 60)

        killbutton.mainloop()

    def OnViewButton(self):
        state, rawdata = self.client.MakeRequest('FETCH')
        if state != ClientState.SUCCEEDED:
            # Hộp thoại lỗi
            return
    
        itemlist = json.loads(rawdata)
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        for item in itemlist:
            self.process_tree.insert('', 'end', values = (item["name"], item["pid"], item["num_threads"]))

    def OnEraseButton(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

    def RequestStart(self, name_to_start):
            state, _ = self.client.MakeRequest('START ' + name_to_start)
            if state == client.ClientState.SUCCEEDED:
                showinfo(title = '', message = 'Process đã được bật')
            else:
                showinfo(title = '', message = 'Không tìm thấy process')

    def OnStartButton(self):
        start = tkinter.Tk()
        start.title("Start")
        start.geometry("250x50")

        start_entry = tkinter.Entry(start)
        start_entry.insert(0, "Nhập tên")
        start_entry.place(x = 15, y = 15, height = 25, width = 150)
        
        start_button = tkinter.Button(start, text = "Start", command = lambda: self.RequestStart(start_entry.get()))
        start_button.place(x = 180, y = 15, height = 25, width = 60)

        start.mainloop()

class ApplicationRunning(ProcessRunning):
    def __init__(self, client):
        super().__init__(client)
        self.baseRequest = "APPLICATION"
        self.windowName = "Application"
        self.headings = ('Application Name', 'Process ID', 'Thread Count')

if __name__ == "__main__":
    tmp = client.ClientProgram()
    a = ApplicationRunning(tmp)
    a.ShowWindow()