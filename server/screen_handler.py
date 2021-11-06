from handler_state import HandlerState
from PIL import ImageGrab
from PIL import Image
import traceback

HORZRES = 8
VERTRES = 10
SRCCOPY = 0x00CC0020
CAPTUREBLT = 0x00000000

DEBUG = False
DEBUG_FRAME_COUNT = 0

class ScreenHandler():
    def __init__(self):
        pass

    def Execute(self, reqCode, data):
        try:
            width, height, byte_data = self.TakeScreenshotAsBytes()
            res = (str(width) + " " + str(height) + " ").encode("utf-8") + byte_data
            return HandlerState.SUCCEEDED, res
        except Exception as e:
            traceback.print_exc()
            return HandlerState.FAILED, None

    def TakeScreenshotAsBytes(self, w=None, h=None):
        image = ImageGrab.grab()
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        if w != None and h != None:
            image = image.resize((w, h), Image.ANTIALIAS)
        byte_data = image.tobytes("raw", "RGBA")
        width, height = image.size
        image.close()
        return width, height, byte_data


if __name__ == "__main__":
    DEBUG = True
    a = ScreenHandler()
    m, n = a.Execute("", "")

