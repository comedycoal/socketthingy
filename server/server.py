
import socket
import concurrent.futures

HEADER = 64
FORMAT = "utf-8"

HOST = "0.0.0.0"
PORT = 6666
BACKLOG = 10

class ServerProgram:
    def __init__(self, host, port, backlog):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(backlog)
        self.currHandler = None

        # Only accepts one client
        self.clientSocket, self.address = self.serverSocket.accept()
        self.connected = True
        print(f'Connected to {self.address}')

    def __del__(self):
        self.serverSocket.close()
        self.clientSocket.close()

    def Run(self):
        while True:
            req = self.ReceiveMessage()
            if not req:
                print("No messages sent")
                break
            self.HandleRequest(req)


    def ReceiveMessage(self):
        message_length = self.clientSocket.recv(HEADER).decode(FORMAT)
        if message_length:
            length = int(message_length)
            message = self.clientSocket.recv(length).decode(FORMAT)
            return message
        return None

    def SendMessage(self, string):
        req = string.encode(FORMAT)
        length = len(req)
        length = str(length).encode(FORMAT)
        length += b' ' * (HEADER - len(length))
        bytes_sent = self.clientSocket.send(length)
        self.clientSocket.send(req)

    def HandleRequest(self, request):
        if not self.currHandler:
            if request == 'SHUTDOWN':
                self.currHandler = ShutdownHandler()
                

        #     elif request == 'PROCESS':
        #         self.currHandler = ProcessHandler()
        #     elif request == 'APPLICATION':
        #         self.currHandler = ApplicationHandler()
        #     elif request == 'SCREENSHOT':
        #         self.currHandler = ScreenshotHandler()
        #     elif request == 'REGISTRY':
        #         self.currHandler = RegistryHandler()
        #     elif request == 'KEYSTROKE':
        #         self.currHandler = KeyStrokeHandler()
        #     elif request == 'EXIT':
        #         self.currHandler = ExitHandler()

        




if __name__ == "__main__":
    program = ServerProgram(HOST, PORT, BACKLOG)
    program.Run()