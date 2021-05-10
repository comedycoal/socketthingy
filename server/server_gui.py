import server
import tkinter as tk


HOST = "0.0.0.0"
PORT = 6666
BACKLOG = 10

def func():
    program = server.ServerProgram(HOST, PORT, BACKLOG)
    program.Run()

tmp = tk.Tk()
tmp.title("Server")

button = tk.Button(tmp, text = "Mở Server", command = func)
button.config(height = 2, width = 10)
button.grid(padx = 10, pady = 20)

tk.mainloop()