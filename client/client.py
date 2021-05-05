# The main program
import socket
import time

HEADER = 64
FORMAT = "utf-8"

HOST = "127.0.0.1"
PORT = 6666

class ClientProgram:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        self.requestID = 0
        
    def __del__(self):
        self.sock.close()

    def Run(self):
        while True:
            self.MakeRequest("PROCESS")
            print(self.requestID)
            time.sleep(3)


    def MakeRequest(self, request):
        self.requestID += 1
        # Send message
        self.SendMessage(request)   
        # Hold for DONE
        while True:
            reply = self.ReceiveMessage()
            if reply == "DONE" or reply == "INVALID":
                break


    def SendMessage(self, string):
        req = string.encode(FORMAT)
        length = len(req)
        length = str(length).encode(FORMAT)
        length += b' ' * (HEADER - len(length))
        bytes_sent = self.sock.send(length)
        self.sock.send(req)

    def ReceiveMessage(self):
        message_length = self.sock.recv(HEADER).decode(FORMAT)
        if message_length:
            length = int(message_length)
            message = self.sock.recv(length).decode(FORMAT)
            return message
        return None


if __name__ == '__main__':
    program = ClientProgram(HOST, PORT)
    program.Run()