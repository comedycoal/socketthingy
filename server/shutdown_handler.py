import os

class ShutdownHandler(Handler):
    def __init__(self):
        super().__init__()
        pass

    def Handle(self):
        super().Handle()

        try:
            os.system("shutdown /s /t 2")
        except:
            self.StopHandle(False)
            return

        self.StopHandle(True)
    
