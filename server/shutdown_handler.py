import os
from handler_state import HandlerState

class ShutdownHandler:
    def __init__(self):
        pass

    def Execute(self, reqCode:str, data:str):
        try:
            if (data == "S"):
                os.system("shutdown /s /t 3")
                return HandlerState.SUCCEEDED, None
            elif (data == "L"):
                os.system("shutdown /l /t 3")
                return HandlerState.SUCCEEDED, None
            else:
                assert False
        except:
            return HandlerState.FAILED, None

if __name__ == '__main__':
    a = ShutdownHandler()
    a.Execute()