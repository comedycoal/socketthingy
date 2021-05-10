import tkinter
import tkinter.ttk as ttk
from client import ClientProgram

client_sv = ClientProgram()

def remove_text(event):
        event.widget.delete(0, "end")

class ProcessRunning:

    def __init__(self):
        pass

    def on_kill(self, id):
        self.on_kill = tkinter.Tk()
        self.on_kill.title("")
        self.on_kill.geometry("250x100")

        if client_sv.MakeRequest():
            self.text = tkinter.Label(self.on_kill, text = 'Đã diệt process').place(x = 20, y = 20)
        else:
            self.text = tkinter.Label(self.on_kill, text = 'Không tìm thấy process').place(x = 20, y = 20)

        self.on_kill_button = tkinter.Button(self.on_kill, command = self.on_kill.destroy, text = 'OK').place (x = 100, y = 50)
        
        self.on_kill.mainloop()

    def kill(self):
        self.kill = tkinter.Tk()
        self.kill.title("Kill")
        self.kill.geometry("250x50")

        self.kill_textbox = tkinter.Entry(self.kill)
        self.kill_textbox.insert(0, "Nhập ID")
        self.kill_textbox.bind("<Button-1>", remove_text)
        self.kill_textbox.place(x = 15, y = 15, height = 25, width = 150)
        self.id = self.kill_textbox.get()
        self.kill_button = tkinter.Button(self.kill, text = "Kill", command = self.on_kill).place(x = 180, y = 15, height = 25, width = 60)

        self.kill.mainloop()

    def view(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        for item in itemlist:
            self.process_tree.insert('', 'end', values = item)

    def erase(self):
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)

    def on_start(self):
        self.on_start = tkinter.Tk()
        self.on_start.title("")
        self.on_start.geometry("250x100")

        self.text = tkinter.Label(self.on_start, text = 'Không tìm thấy process').place(x = 20, y = 20)
        self.text = tkinter.Label(self.on_start, text = 'Process đã được bật').place(x = 20, y = 20)

        self.on_start_button = tkinter.Button(self.on_start, command = self.on_start.destroy, text = 'OK').place (x = 100, y = 50)
        
        self.on_start.mainloop()

    def start(self):
        self.start = tkinter.Tk()
        self.start.title("Start")
        self.start.geometry("250x50")

        self.start_textbox = tkinter.Entry(self.start)
        self.start_textbox.insert(0, "Nhập tên")
        self.start_textbox.bind("<Button-1>", remove_text)
        self.start_textbox.place(x = 15, y = 15, height = 25, width = 150)

        self.start_button = tkinter.Button(self.start, text = "Start", command = self.on_start).place(x = 180, y = 15, height = 25, width = 60)

        self.start.mainloop()


    def process(self):
        self.process = tkinter.Tk()
        self.process.title("process")

        self.process.geometry("470x400")
        
        self.process_tree = ttk.Treeview(self.process, columns = ('Name Process', 'ID Process', 'Count Thread'), show = 'headings')
        self.process_tree.heading('Name Process', text = "Name Process")
        self.process_tree.column("Name Process", width = 140)
        self.process_tree.heading('ID Process', text = "ID Process")
        self.process_tree.column("ID Process", width = 80)
        self.process_tree.heading('Count Thread', text = "Count Thread")
        self.process_tree.column("Count Thread", width = 100)
        self.tree_scrollbar = ttk.Scrollbar(orient = "vertical", command = self.process_tree.yview)
        self.process_tree.config(yscrollcommand = self.tree_scrollbar.set)
        self.process_tree.place(x = 30, y = 80, height = 300, width = 420)
        self.tree_scrollbar.place(x = 435, y = 80, height = 300, width = 15)

        self.process_button1 = tkinter.Button(self.process, text = 'Kill', command = self.kill)
        self.process_button1.place(x = 30, y = 10, height = 60, width = 100)

        self.process_button2 = tkinter.Button(self.process, text = 'Xem', command = self.view)
        self.process_button2.place(x = 140, y = 10, height = 60, width = 90)

        self.process_button3 = tkinter.Button(self.process, text = 'Xóa', command = self.erase)
        self.process_button3.place(x = 240, y = 10, height = 60, width = 100)

        self.process_button4 = tkinter.Button(self.process, text = 'Start', command = self.start)
        self.process_button4.place(x = 350, y = 10, height = 60, width = 100)

        self.process.mainloop()



itemlist = [
('Hyundai', 'brakes', '1') ,
('Honda', 'light', '2') ,
('Lexus', 'battery', '3') ,
('Benz', 'wiper', '4') ,
('Ford', 'tire', '5') ,
('Chevy', 'air', '6') ,
('Chrysler', 'piston', '1') ,
('Toyota', 'brake pedal', '2') ,
('BMW', 'seat', '3')
]


if __name__ == "__main__":
    a = ProcessRunning()
    a.process()
    