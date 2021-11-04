import server
import ctypes
import sys
import tkinter as tk

HOST = "0.0.0.0"
PORT = 6666
BACKLOG = 10

SW_SHOWNORMAL = 1
SW_SHOWMINIMIZED = 2

def openServer():
    program = server.ServerProgram()
    program.OpenServer()
    program.Run()

def MakeWindow():
    sv = tk.Tk()
    sv.title("Server")

    button = tk.Button(sv, text = "Mở Server", command = openServer)
    button.config(height = 2, width = 10)
    button.grid(padx = 10, pady = 20)

    tk.mainloop()

if __name__ == '__main__':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        hinstance = ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, sys.argv[0], None, SW_SHOWMINIMIZED)
        if hinstance <= 32:
            raise RuntimeError("Cannot relaunch script with elevated privilege")
    else:
        MakeWindow()