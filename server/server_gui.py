import server
import tkinter as tk

HOST = "0.0.0.0"
PORT = 6666
BACKLOG = 10

def openServer():
    program = server.ServerProgram()
    program.OpenServer()
    program.Run()

if __name__ == '__main__':
    sv = tk.Tk()
    sv.title("Server")

    button = tk.Button(sv, text = "Mở Server", command = openServer)
    button.config(height = 2, width = 10)
    button.grid(padx = 10, pady = 20)

    tk.mainloop()