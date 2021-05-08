import ctypes
from ctypes import windll,byref,c_int,c_void_p, POINTER, CFUNCTYPE
from ctypes.wintypes import WPARAM, LPARAM, MSG, DWORD
import threading
from handler_state import HandlerState


user32 = windll.user32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
VK_CONTROL = [0x11,0xa2,0xa3]
msg = MSG()

hook = None
stop = False

FILE_PATH = "temp.txt"
file = None

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("vkCode", DWORD),
                ("scanCode", DWORD),
                ("flags", DWORD),
                ("time", DWORD),
                ("dwExtraInfo", DWORD)]  

LLKP_decl = CFUNCTYPE(c_int, c_int, WPARAM, POINTER(KBDLLHOOKSTRUCT))

def LowLevelKeyboardProc(nCode, wParam, lParam):
    global file, stop

    assert file != None

    vkCode = lParam.contents.vkCode
    if wParam == WM_KEYDOWN:
        file.write(str(vkCode))
        pass

    if stop:
        user32.UnhookWindowsHookEx(hook)
        ctypes.windll.user32.PostQuitMessage(0)
    return user32.CallNextHookEx(hook, nCode, wParam, lParam)

def Record():
    global hook
    callback = LLKP_decl(LowLevelKeyboardProc)
    hook = user32.SetWindowsHookExA(WH_KEYBOARD_LL, callback, 0,0)
    print(hook)
    while user32.GetMessageA(ctypes.byref(msg),None, 0,0):
        pass

def RecordWrapper():
    a = threading.Thread(target = Record)
    return a

class KeystrokeHandler:
    def __init__(self, filepath):
        self.a = None
        self.filepath = filepath
        pass

    def Handle(self):
        pass

    def Hook(self):
        global stop, file
        file = open(self.filepath, "w")
        self.a = RecordWrapper()
        stop = False
        self.a.start()
        pass

    def Unhook(self):
        global stop, file
        stop = True
        self.a.join()
        file.close()
        pass

    def __del(self):
        self.Unhook()
        pass

if __name__ == "__main__":
    a = KeystrokeHandler(FILE_PATH)
    a.Hook()
    time.sleep(30)
    a.Unhook()
