import tkinter

program = None

def remove_text(event):
        event.widget.delete(0, "end")

class Keystroke:

    def hook(self):
        return None

    def unhook(self):
        return None

    def printkey(self):
        for item in texttest:
            self.keystroke_listbox.insert('end', item)

    def erase(self):
        for item in range (len(texttest)):
            self.keystroke_listbox.delete(0)

    def keystroke(self):
        self.keystroke = tkinter.Tk()
        self.keystroke.title("Keystroke")

        self.keystroke.geometry("470x400")
        
        self.keystroke_listbox = tkinter.Listbox(self.keystroke)
        self.keystroke_listbox.place(x = 30 , y = 80, height = 300, width = 420)

        self.keystroke_button1 = tkinter.Button(self.keystroke, text = 'Hook', command = self.hook)
        self.keystroke_button1.place(x = 30, y = 10, height = 60, width = 100)

        self.keystroke_button2 = tkinter.Button(self.keystroke, text = 'Unhook', command = self.unhook)
        self.keystroke_button2.place(x = 140, y = 10, height = 60, width = 90)

        self.keystroke_button3 = tkinter.Button(self.keystroke, text = 'In phím', command = self.printkey)
        self.keystroke_button3.place(x = 240, y = 10, height = 60, width = 100)

        self.keystroke_button4 = tkinter.Button(self.keystroke, text = 'Xóa', command = self.erase)
        self.keystroke_button4.place(x = 350, y = 10, height = 60, width = 100)

        self.keystroke.mainloop()


texttest = []
for i in range(20):
    texttest.append("hi" + str(i))


if __name__ == "__main__":
    a = Keystroke()
    a.keystroke()
