import ctypes, ctypes.wintypes

from handler_state import HandlerState
from process_handler import ProcessHandler


pids = set()
def WindowEnumCallback(hwindow, param):
    length = GetWindowLength(hwindow)
    if length > 0 and not IsIconic(hwindow):
        processID = ctypes.c_ulong()
        a = GetWindowThreadProcessId(hwindow, ctypes.byref(processID))
        pids.add(processID.value)
    return True

kernel32 = ctypes.WinDLL("Kernel32.dll")
psapi = ctypes.WinDLL('Psapi.dll')
user32 = ctypes.WinDLL("user32.dll")

EnumWindows = user32.EnumWindows
EnumWindows.restype = ctypes.wintypes.BOOL

GetWindowLength = user32.GetWindowTextLengthA
GetWindowLength.restype = ctypes.c_int

GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.restype = ctypes.wintypes.DWORD

IsIconic = user32.IsIconic
IsIconic.restype = ctypes.wintypes.BOOL

WNDENUMPROC = ctypes.CFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
FUNC = WNDENUMPROC(WindowEnumCallback)


class ApplicationHandler(ProcessHandler):
    def __int__(self):
        super().__init__()
        self.pids = None

    def FetchAndUpdate(self):
        self.processes = self.FetchWithPIDs(self.FetchAppPIDSet())
        return self.processes

    def FetchAppPIDSet(self):
        EnumWindows(FUNC, 0)
        return pids

if __name__ == '__main__':
    a = ApplicationHandler()
    state, m = a.Execute("FETCH", "")
    print(m)
