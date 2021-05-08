from handler_state import HandlerState
from PIL import ImageGrab
from PIL import Image

class ScreenshotHandler():
    def __init__(self):
        pass

    def Execute(self, reqCode:str, data:str):
        try:
            width, height, byte_data = self.TakeScreenshotAsBytes()
            res = (str(width) + " " + str(height) + " ").encode("utf-8") + byte_data
            return HandlerState.SUCCEEDED, res
        except Exception as e:
            print(e)
            return HandlerState.FAILED, None

    def TakeScreenshotAsBytes(self):
        image = ImageGrab.grab()
        byte_data = image.tobytes()
        width, height = image.size
        image.close()
        return width, height, byte_data

if __name__ == "__main__":
    a = ScreenshotHandler()
    m, n = a.Execute("", "")
    
