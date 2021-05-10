# The main program
import socket
import time
from enum import Enum

HEADER = 64
FORMAT = "utf-8"

HOST = "127.0.0.1"
PORT = 6666

class ClientState(Enum):
    SUCCEEDED = 0,
    FAILED = 1,
    INVALID = 2,
    BADMESSAGE = 3

class ClientProgram:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.requestID = 0
        
    def __del__(self):
        self.sock.close()

    def Run(self):
        a = 0
        while True:
            a += 1
            req = input("Enter request:")
            state, data = self.MakeRequest(req)
            m = 0
            if data:
                m = len(data)
            print(state, m)
            if req == "EXIT" and state == ClientState.SUCCEEDED:
                break
    
    def Connect(self, host=HOST, port=PORT):
        self.sock.connect((host, port))
        self.requestID = 0
        pass

    def Disconnect(self):
        self.connected = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pass

    def MakeRequest(self, request):
        self.requestID += 1
        # Send message
        self.SendMessage(request)   
        # Hold for DONE
        reply = self.ReceiveMessage()
        state, rawdata = self.ProcessReply(reply)
        if state == "SUCCEEDED":
            return ClientState.SUCCEEDED, rawdata
        elif state == "FAILED":
            return ClientState.FAILED, None
        elif state == "INVALID":
            return ClientState.INVALID, None
        elif state == "BADMESSAGE":
            return ClientState.BADMESSAGE, None
            
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
            message = self.sock.recv(length)
            return message
        return None

    def ProcessReply(self, reply):
        try:
            splitted = reply.split(b' ',1)
            state = splitted[0].decode(FORMAT)
            rawdata = None
            if len(splitted) == 2:
                rawdata = splitted[1]
            return state, rawdata

        except Exception as e:
            return "BADMESSAGE", None
            pass


if __name__ == '__main__':
    program = ClientProgram()
    program.Connect()
    program.Run()