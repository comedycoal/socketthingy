import os

class ShutdownHandler:
    def __init__(self):
        # super().__init__()
        pass

    def Handle(self):
        #super().Handle()

        try:
            os.system("shutdown /s /t 2")
        except:
            print("Can't shutdown")
            return

        print("Shutting Down")
    
if __name__ == '__main__':
    a = ShutdownHandler()
    a.Handle()