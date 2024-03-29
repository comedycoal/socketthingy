from PySide2.QtCore import *
from PySide2 import QtGui, QtWidgets
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PIL import Image, ImageQt

import sys
import threading
import socket
from queue import Queue
import traceback
import time

from client import ClientState
from request_gui import RequestUI

HEADER = 64
FORMAT = 'utf-8'

def ReceiveMessage(sock):
    '''
    Receive messages send through client socket, blocking the program/thread.
    Returns:
        str: if any message is received.
        None: if any errors occur or no message is received
    '''
    try:
        message_length = sock.recv(HEADER).decode(FORMAT)
        if message_length:
            length = int(message_length)
            bytesReceived = 0
            chunks =[]
            while bytesReceived < length:
                message = sock.recv(length - bytesReceived)
                bytesReceived += len(message)
                chunks.append(message)

            message = b''.join(chunks)
            return message
    except Exception as e:
        traceback.print_exc()
    
        return None

class LivestreamUI(RequestUI):
    def __init__(self, parent, client):
        super().__init__(parent, client, 'LIVESTREAM')
        self.clientProgram = client
        self.renderThread = None
        self.captureThread = None
        self.imageQueue = None
        self.stopStreamEvent = None


    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "ScreenShot"))
        self.setFixedSize(1000,600)
        
        self.streaming_button = QPushButton(clicked = lambda:self.onLivestream())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.streaming_button.setFont(font)
        self.streaming_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.streaming_button.setObjectName("streaming_button")
        self.streaming_button.setText(QCoreApplication.translate("MainWindow", "Xem"))

        self.stop_button = QPushButton(clicked = lambda: self.onStopLivestream())
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(12)
        self.stop_button.setFont(font)
        self.stop_button.setStyleSheet("background-color: rgb(224, 237, 255)")
        self.stop_button.setObjectName("stop_button")
        self.stop_button.setText(QCoreApplication.translate("MainWindow", "Dừng"))

        self.imageView = QLabel()
        self.imageView.setObjectName("imageView")

        button_layout = QHBoxLayout()
        button_layout.addSpacing(300)
        button_layout.addWidget(self.streaming_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(self.stop_button)
        button_layout.addSpacing(300)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.imageView)
        mainLayout.addItem(button_layout)
        self.setLayout(mainLayout)

    def onStartGUI(self):
        self.ShowWindow()

    def BytesToQImageAndFrame(self, rawdata:bytes):
        split = rawdata.split(b' ', 3)
        w = int(split[0].decode("utf-8"))
        h = int(split[1].decode("utf-8"))
        f = int(split[2].decode("utf-8"))
        pixels = split[3]
        qimage = ImageQt.ImageQt(Image.frombytes("RGBA", (w, h), pixels))

        return f, qimage

    def onLivestream(self):
        state, rawdata = self.client.MakeRequest('START')

        if state == ClientState.NOCONNECTION:
            QMessageBox.about(self, "", "Chưa kết nối đến server")
            return False
        elif state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Thao tác thất bại")
            return False

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.clientProgram.host, self.clientProgram.port))

        self.renderThread = threading.Thread(target=self.RenderToImageView)
        self.captureThread = threading.Thread(target=self.CaptureImages, args=(sock,))
        self.imageQueue = Queue()
        self.stopStreamEvent = threading.Event()
        self.captureThread.start()
        self.renderThread.start()

    def RenderToImageView(self):
        TARGET_FPS = 30
        TIME_FRAME = 1 / TARGET_FPS

        target_frame = 1
        f = None
        image = None

        start = time.perf_counter()
        while not self.stopStreamEvent.is_set():
            elapsed = time.perf_counter() - start
            if elapsed >= (target_frame - 1) * TIME_FRAME:
                if image == None and not self.imageQueue.empty():
                    f, image = self.imageQueue.get()
                    if f < target_frame:
                        f, image = None, None
                        continue
                elif image != None and f != None:
                    if f == target_frame:
                        self.imageView.setPixmap(QPixmap.fromImage(image))
                        target_frame += 1
                        image, f = None, None
                    elif f > target_frame:
                        target_frame, f = None, None
                        continue

    def CaptureImages(self, sock):
        while not self.stopStreamEvent.is_set():
            rawdata = ReceiveMessage(sock)
            frame, image = self.BytesToQImageAndFrame(rawdata)
            self.imageQueue.put((frame, image))
        pass

    def onStopLivestream(self):
        state, _ = self.client.MakeRequest('STOP')
        if state == ClientState.NOCONNECTION:
            QMessageBox.about(self, "", "Chưa kết nối đến server")
            return False
        elif state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Thao tác không thành công")
            return False

        self.stopStreamEvent.set()
        if self.renderThread:
            self.renderThread.join()
        if self.captureThread:
            self.captureThread.join()
        self.imageQueue = None
        self.renderThread = None
        self.captureThread = None

    def ShowWindow(self):
        self.setupUI()
        self.show()

    def CleanUp(self):
        self.onStopLivestream()
        return super().CleanUp()

if __name__ == '__main__':
    from os import environ

    def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"

    suppress_qt_warnings()

    app = QtWidgets.QApplication(sys.argv)
    demo = LivestreamUI(None)
    demo.setupUI()
    demo.ShowWindow() 
    sys.exit(app.exec_())