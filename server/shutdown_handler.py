import os
from handler_state import HandlerState

class ShutdownHandler:
    def __init__(self):
        # super().__init__()
        pass

    def Shutdown(self):
        #super().Handle()

        try:
            os.system("shutdown /s /t 3")
        except:
            return HandlerState.FAILED

        return HandlerState.SUCCEEDED
    
if __name__ == '__main__':
    a = ShutdownHandler()
    a.Handle()