import tkinter
import tkinter.ttk as ttk

def remove_text(event):
        event.widget.delete(0, "end")

class AppRunning:

    def kill(self):
        self.kill = tkinter.Tk()
        self.kill.title("Kill")
        self.kill.geometry("250x50")

        self.kill_textbox = tkinter.Entry(self.kill)
        self.kill_textbox.insert(0, "Nhập ID")
        self.kill_textbox.bind("<Button-1>", remove_text)
        self.kill_textbox.place(x = 15, y = 15, height = 25, width = 150)

        self.kill_button = tkinter.Button(self.kill, text = "Kill").place(x = 180, y = 15, height = 25, width = 60)

        self.kill.mainloop()

    def view(self):
        for item in itemlist:
            self.listApp_tree.insert('', 'end', values = item)

    def erase(self):
        for item in self.listApp_tree.get_children():
            self.listApp_tree.delete(item)

    def start(self):
        self.start = tkinter.Tk()
        self.start.title("Start")
        self.start.geometry("250x50")

        self.start_textbox = tkinter.Entry(self.start)
        self.start_textbox.insert(0, "Nhập tên")
        self.start_textbox.bind("<Button-1>", remove_text)
        self.start_textbox.place(x = 15, y = 15, height = 25, width = 150)

        self.start_button = tkinter.Button(self.start, text = "Start").place(x = 180, y = 15, height = 25, width = 60)

        self.start.mainloop()


    def application(self):
        self.listApp = tkinter.Tk()
        self.listApp.title("listApp")

        self.listApp.geometry("470x400")
        
        self.listApp_tree = ttk.Treeview(columns = ('Name Application', 'ID Application', 'Count Thread'), show = 'headings')
        self.listApp_tree.heading('Name Application', text = "Name Application")
        self.listApp_tree.column("Name Application", width = 140)
        self.listApp_tree.heading('ID Application', text = "ID Application")
        self.listApp_tree.column("ID Application", width = 80)
        self.listApp_tree.heading('Count Thread', text = "Count Thread")
        self.listApp_tree.column("Count Thread", width = 100)
        self.tree_scrollbar = ttk.Scrollbar(orient = "vertical", command = self.listApp_tree.yview)
        self.listApp_tree.config(yscrollcommand = self.tree_scrollbar.set)
        self.listApp_tree.place(x = 30, y = 80, height = 300, width = 420)
        self.tree_scrollbar.place(x = 435, y = 80, height = 300, width = 15)

        self.listApp_button1 = tkinter.Button(self.listApp, text = 'Kill', command = self.kill)
        self.listApp_button1.place(x = 30, y = 10, height = 60, width = 100)

        self.listApp_button2 = tkinter.Button(self.listApp, text = 'Xem', command = self.view)
        self.listApp_button2.place(x = 140, y = 10, height = 60, width = 90)

        self.listApp_button3 = tkinter.Button(self.listApp, text = 'Xóa', command = self.erase)
        self.listApp_button3.place(x = 240, y = 10, height = 60, width = 100)

        self.listApp_button4 = tkinter.Button(self.listApp, text = 'Start', command = self.start)
        self.listApp_button4.place(x = 350, y = 10, height = 60, width = 100)

        self.listApp.mainloop()



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
    a = AppRunning()
    a.application()
    