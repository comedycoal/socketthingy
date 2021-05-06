from handler_state import HandlerState
from PIL import ImageGrab
from PIL import Image

class ScreenshotHandler():
    def __init__(self):
        pass

    def Handle(self):
        pass

    def TakeScreenshot(self):
        image = ImageGrab.grab()
        byte_data = image.tobytes()
        image.close()
        return byte_data

if __name__ == "__main__":
    a = ScreenshotHandler()
    m = a.TakeScreenshot()
    image = Image.frombytes("RGB", (1920, 1080), m)
    image.save('shot.png')
    image.close()
