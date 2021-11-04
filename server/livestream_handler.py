from handler_state import HandlerState
from screen_handler import ScreenHandler

from pathlib import Path
import socket
import timeit
import time
import threading
import traceback

HEADER = 64
FORMAT = "utf-8"

def SendMessage(sock, string, binaryData=None):
    '''
    Send a message to client

    Parameters:
        string (str): the request
        binaryData (bytes, None): additional data in binary form, will be attatched to the request, separate by a single b' '

    Returns:
        True: if the message is sent properly
        False: if any errors occurs
    '''
    try:
        req = string.encode(FORMAT)
        if binaryData:
            req += b' ' + binaryData

        length = len(req)
        header = str(length).encode(FORMAT)
        header += b' ' * (HEADER - len(header))

        bytes_sent = sock.send(header)
        assert bytes_sent == HEADER, "Length of message sent does not match that of the actual message"

        bytes_sent = sock.send(req)
        assert bytes_sent == length, "Length of message sent does not match that of the actual message"

        return True
    except Exception as e:
        traceback.print_exc()

    return False

class LivestreamHandler():
    def __init__(self, serverProgram, hostSocket: socket.socket, scrHandler: ScreenHandler):
        self.screenHandler = scrHandler
        self.hostSocket = hostSocket
        self.livestreamThread = None
        self.livestreamEvent = None
        self.serverProgram = serverProgram
        pass

    def HandleMessageFault(self):
        pass

    def Execute(self, reqCode:str, data:str):
        try:
            if reqCode == "START":
                self.livestreamThread = threading.Thread(target=self.Livestream, args=(self.hostSocket,))
                self.livestreamEvent = threading.Event()
                self.livestreamThread.start()
                return HandlerState.SUCCEEDED, None
            elif reqCode == "STOP":
                self.livestreamEvent.set()
                self.livestreamThread.join()
                self.livestreamThread = None
                self.livestreamEvent = None
                return HandlerState.SUCCEEDED, None
            else:
                return HandlerState.INVALID, None
        except Exception as e:
            traceback.print_exc()
            return HandlerState.FAILED, None

    def Livestream(self, hostSocket: socket.socket):
        # accept the coming connection from client
        liveSocket, address = hostSocket.accept()

        TARGET_FPS = 24
        TIME_FRAME = 1 / TARGET_FPS

        frame = 0
        elapsed = 0

        while not self.livestreamEvent.is_set():
            start = timeit.default_timer()
            w, h, data = self.screenHandler.TakeScreenshotAsBytes()
            state = SendMessage(liveSocket, str(w) + " " + str(h), data)
            if not state:
                self.HandleMessageFault()
                break

            targetTime = frame * TIME_FRAME
            frame += 1
            end = timeit.default_timer()
            elapsed += (end - start)

            waitTime = targetTime - elapsed if targetTime >= elapsed else 0.0
            time.sleep(waitTime)

        liveSocket.close()

if __name__ == "__main__":
    DEBUG = True
    a = ScreenHandler()
    m, n = a.Execute("", "")

