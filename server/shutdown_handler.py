import os
import traceback
import time
from handler_state import HandlerState

class ShutdownHandler:
    def __init__(self):
        pass

    def Execute(self, reqCode, data):
        try:
            if (data == "S"):
                os.system("shutdown /s /t 3")
                return HandlerState.SUCCEEDED, None
            elif (data == "L"):
                time.sleep(3)
                os.system("shutdown /l")
                return HandlerState.SUCCEEDED, None
            else:
                return HandlerState.INVALID, None
        except:
            return HandlerState.FAILED, None

if __name__ == '__main__':
    a = ShutdownHandler()
    a.Execute()