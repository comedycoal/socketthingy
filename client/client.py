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
        '''
        A console-based loop to communicate with the server
        '''
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
        '''
        Connects to a server listening at (host, port)

        Parameters:
            host (str): host part
            port (int): port part

        return:
            True: if connection is successful
            False: if not
        '''
        try:
            if not self.sock:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.requestID = 0
            self.connected = True
            return True
        except Exception as e:
            print(e)
            return False

    def Disconnect(self):
        '''
        Disconnect from server
        '''
        self.sock.close()
        self.connected = False
        self.sock = None
        
    def MakeRequest(self, request):
        '''
        A wrapper for sending requests and receiving replies for each.
        Sends a message corresponding to 'request', then wait and receive for a reply from server

        Parameters:
            request (str): request in string form

        Returns:
            state (ClientState): the state of the connection or the message itself
            rawdata (bytes | None): is any data the server sent back
        '''
        # Try for connection:
        try:
            assert self.connected, "No connection established"
        except Exception as e:
            print(e)
            return ClientState.NOCONNECTION, None

        # Send message
        self.requestID += 1
        succeeded = self.SendMessage(request) 
        if not succeeded:
            # Connection is faulty, quit
            return ClientState.BADCONNECTION, None

        # Hold for reply from server
        try:
            reply = self.ReceiveMessage()
            assert reply, "No reply received"
        except Exception as e:
            print(e)
            return ClientState.BADCONNECTION, None

       # Process reply from server 
        try:
            stateStr, rawdata = self.ProcessReply(reply)
            print(stateStr, len(rawdata) if rawdata else None)
            return ClientProgram.States[stateStr], rawdata if rawdata else None
        except Exception as e:
            print(e)
            return ClientState.BADMESSAGE, None
            
    def SendMessage(self, string, binaryData=None):
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

            bytes_sent = self.sock.send(header)
            assert bytes_sent == HEADER, "Length of sent message does not match that of the actual message"
            
            bytes_sent = self.sock.send(req)
            assert bytes_sent == length, "Length of sent message does not match that of the actual message"

            return True
        except Exception as e:
            print(e)
        return False

    def ReceiveMessage(self):
        '''
        Receive messages send through client socket, blocking the program/thread.

        Returns:
            str: if any message is received.
            None: if any errors occur or no message is received
        '''
        try:
            message_length = self.sock.recv(HEADER).decode(FORMAT)
            if message_length:
                length = int(message_length)
                bytesReceived = 0
                chunks =[]
                while bytesReceived < length:
                    message = self.sock.recv(length - bytesReceived)
                    bytesReceived += len(message)
                    chunks.append(message)

                message = b''.join(chunks)
                return message
        except Exception as e:
            print(e)
        
        return None

    def ProcessReply(self, reply):
        '''
        Split reply string into 2 parts to process by the client

        Parameters:
            reply (str): a reply string from server

        Returns:
            stateStr (str): a string starting the message, indicating a corresponding ClientState
            rawdata (bytes): is any data attached to the reply

        '''
        try:
            splitted = reply.split(b' ',1)
            stateStr = splitted[0].decode(FORMAT)
            rawdata = None
            if len(splitted) == 2:
                rawdata = splitted[1]
            return stateStr, rawdata
        except Exception as e:
            return "BADMESSAGE", None


if __name__ == '__main__':
    program = ClientProgram()
    program.Connect()
    program.Run()