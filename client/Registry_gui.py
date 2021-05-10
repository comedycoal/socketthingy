import tkinter

def remove_text(event):
        event.widget.delete(0, "end")

class Registry:

    def browser(self):
        print('browser')

    def dosth(self):
        for item in itemlist:
            self.registry_tree.insert('', 'end', values = item)

    def erase(self):
        for item in self.registry_tree.get_children():
            self.registry_tree.delete(item)

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


    def registry(self):
        self.registry = tkinter.Tk()
        self.registry.title("Registry")

        self.registry.geometry("500x500")
        
        self.registry_entry1 = tkinter.Entry(self.registry)
        self.registry_entry1.insert(0, "Đường dẫn…")
        self.registry_entry1.bind("<Button-1>", remove_text)
        self.registry_entry1.place(x = 10, y = 20, height = 30, width = 380)

        self.registry_button1 = tkinter.Button(self.registry, text = 'Browser...', command = self.browser)
        self.registry_button1.place(x = 400, y = 20, height = 30, width = 90)

        self.registry_listbox1 = tkinter.Listbox(self.registry)
        self.registry_listbox1.insert(0, "Nội dung")
        self.registry_listbox1.bind("<Button-1>", remove_text)
        self.registry_listbox1.place(x = 10 , y = 60, height = 100, width = 380)
        self.listbox1_scrollbar = tkinter.Scrollbar(self.registry)
        self.registry_listbox1.config(yscrollcommand = self.listbox1_scrollbar.set)
        self.listbox1_scrollbar.config(command = self.registry_listbox1.yview)



        self.registry_button2 = tkinter.Button(self.registry, text = 'Gởi nội dung', command = self.dosth)
        self.registry_button2.place(x = 400, y = 60, height = 100, width = 90)



        # self.registry_button2 = tkinter.Button(self.registry, text = 'Xem', command = self.view)
        # self.registry_button2.place(x = 140, y = 10, height = 60, width = 90)

        # self.registry_button3 = tkinter.Button(self.registry, text = 'Xóa', command = self.erase)
        # self.registry_button3.place(x = 240, y = 10, height = 60, width = 100)

        # self.registry_button4 = tkinter.Button(self.registry, text = 'Start', command = self.start)
        # self.registry_button4.place(x = 350, y = 10, height = 60, width = 100)

        self.registry.mainloop()



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
    a = Registry()
    a.registry()
    