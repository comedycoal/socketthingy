# The main program
import socket
from tkinter.constants import E, TRUE
from enum import Enum

HEADER = 64
FORMAT = "utf-8"

HOST = "127.0.0.1"
PORT = 6666

class ClientState(Enum):
    SUCCEEDED = 0,
    FAILED = 1,
    INVALID = 2,
    BADMESSAGE = 3,
    NOCONNECTION = 4,
    BADCONNECTION = 5

class ClientProgram:
    States = {
        "SUCCEEDED": ClientState.SUCCEEDED,
        "FAILED": ClientState.FAILED,
        "INVALID": ClientState.INVALID,
        "BADMESSAGE": ClientState.BADMESSAGE,
        "NOCONNECTION": ClientState.NOCONNECTION,
        "BADCONNECTION": ClientState.BADCONNECTION
    }

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.requestID = 0
        
    def __del__(self):
        self.sock.close()

    def Run(self):
        try:
            assert self.connected, "No connection is made"
        except AssertionError as e: 
            print(e)
            return
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
        try:
            self.sock.connect((host, port))
            self.requestID = 0
            self.connected = True
            return True
        except Exception as e:
            print(e)
            return False

    def Disconnect(self):
        self.connected = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pass

    def MakeRequest(self, request):
        try:
            assert self.connected, "No connection established"
        except Exception as e:
            print(e)
            return ClientState.NOCONNECTION, None

        self.requestID += 1
        # Send message
        status = self.SendMessage(request) 
        if not status:
            #Connection is faulty, quit
            return ClientState.BADCONNECTION, None
        # Hold for DONE

        reply = self.ReceiveMessage()
        state, rawdata = self.ProcessReply(reply)
        return ClientProgram.States[state], rawdata if rawdata else None
            
    def SendMessage(self, string):
        try:
            req = string.encode(FORMAT)
            length = len(req)
            length = str(length).encode(FORMAT)
            length += b' ' * (HEADER - len(length))
            bytes_sent = self.sock.send(length)
            assert bytes_sent == length, "Length of sent message does not match that of the actual message"
            self.sock.send(req)

            return True
        except OSError as e:
            print(e)
            return False
        except AssertionError as e:
            print(e)
            return False

    def ReceiveMessage(self):
        try:
            message_length = self.sock.recv(HEADER).decode(FORMAT)
            if message_length:
                length = int(message_length)
                message = self.sock.recv(length)
                return message
            return None
        except Exception as e:
            print(e)
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


if __name__ == '__main__':
    program = ClientProgram()
    program.Connect()
    program.Run()