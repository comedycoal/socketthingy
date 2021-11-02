from handler_state import HandlerState
from PIL import ImageGrab
from PIL import Image
from pathlib import Path
import traceback

import ctypes
from ctypes import windll, byref, c_int, c_void_p, POINTER, CFUNCTYPE
from ctypes import wintypes

HORZRES = 8
VERTRES = 10
SRCCOPY = 0x00CC0020
CAPTUREBLT = 0x00000000

DEBUG = False
DEBUG_FRAME_COUNT = 0

class BITMAPFILEHEADER(ctypes.Structure):
    _fields_ = [("bfType", wintypes.WORD),
                ("bfSize", wintypes.DWORD),
                ("bfReserved1", wintypes.WORD),
                ("bfReserved2", wintypes.WORD),
                ("bfOffBits", wintypes.DWORD)
                ]

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wintypes.DWORD),
                ("biWidth", wintypes.LONG),
                ("biHeight", wintypes.LONG),
                ("biPlanes", wintypes.WORD),
                ("biBitCount", wintypes.WORD),
                ("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD),
                ("biXPelsPerMeter", wintypes.LONG),
                ("biYPelsPerMeter", wintypes.LONG),
                ("biClrUsed", wintypes.DWORD),
                ("biClrImportant", wintypes.DWORD)
                ]

class ScreenHandler():
    def __init__(self):
        pass

    def Execute(self, reqCode:str, data:str):
        try:
            if data == "SINGLE":
                width, height, byte_data = self.TakeScreenshotAsBytes()
                res = (str(width) + " " + str(height) + " ").encode("utf-8") + byte_data
                return HandlerState.SUCCEEDED, res
            else:
                return HandlerState.INVALID, None
        except Exception as e:
            traceback.print_exc()
            return HandlerState.FAILED, None

    def TakeScreenshotAsBytes(self):
        image = ImageGrab.grab()
        byte_data = image.tobytes()
        width, height = image.size
        if DEBUG:
            image.save(Path(__file__).parent / ("debug_img" + str(DEBUG_FRAME_COUNT) + ".jpg"), 'JPEG', quality=70)
            pass
        image.close()
        return width, height, byte_data

class ScreenshotHandler():
    def __init__(self):
        pass

    def Execute(self, reqCode:str, data:str):
        try:
            width, height, byte_data = self.TakeScreenshotAsBytes()
            res = (str(width) + " " + str(height) + " ").encode("utf-8") + byte_data
            return HandlerState.SUCCEEDED, res
        except Exception as e:
            traceback.print_exc()
            return HandlerState.FAILED, None

    def TakeScreenshotAsBytes(self):
        # hScreenDC = windll.user32.GetDC(None)
        # hMemoryDC = windll.gdi32.CreateCompatibleDC(hScreenDC)
        # width = windll.gdi32.GetDeviceCaps(hScreenDC, HORZRES)
        # height = windll.gdi32.GetDeviceCaps(hScreenDC, VERTRES)
        # bitmap = windll.gdi32.CreateCompatibleBitmap(hScreenDC, width, height)
        # oldBmp = windll.gdi32.SelectObject(hMemoryDC, bitmap)
        # windll.gdi32.BitBlt(bitmap, 0,0, width, height, hScreenDC, 0,0, SRCCOPY or CAPTUREBLT)
        # bi = BITMAPINFOHEADER()
        # bi.biSize = ctypes.sizeof(BITMAPINFOHEADER);
        # bi.biWidth = width;
        # bi.biHeight = height;
        # bi.biPlanes = 1;
        # bi.biBitCount = 32;
        # bi.biCompression = ctypes.BI_RGB;
        # bi.biSizeImage = 0;
        # bi.biXPelsPerMeter = 0;
        # bi.biYPelsPerMeter = 0;
        # bi.biClrUsed = 0;
        # bi.biClrImportant = 0;
        pass


if __name__ == "__main__":
    DEBUG = True
    a = ScreenshotHandler()
    m, n = a.Execute("", "")

