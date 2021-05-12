import tkinter

from Request_gui import Request
from client import ClientState

def remove_text(event):
        event.widget.delete(0, "end")

class Registry(Request):
    def __init__(self, client):
        super().__init__(client, "REGISTRY")

    def ShowWindow(self):
        self.MainWindow = tkinter.Tk()
        self.MainWindow.title("Registry")

        self.MainWindow.geometry("500x500")
        
        # Phần file registry
        self.regFilePathInputBox = tkinter.Entry(self.MainWindow)
        self.regFilePathInputBox.insert(0, "Đường dẫn…")
        self.regFilePathInputBox.bind("<Button-1>", remove_text)
        self.regFilePathInputBox.place(x = 10, y = 20, height = 30, width = 380)

        self.browseButton = tkinter.Button(self.MainWindow, text = 'Browse...', command = self.Browse)
        self.browseButton.place(x = 400, y = 20, height = 30, width = 90)

        self.regFileContent = tkinter.Listbox(self.MainWindow)
        self.regFileContent.insert(0, "Nội dung")
        self.regFileContent.bind("<Button-1>", remove_text)
        self.regFileContent.place(x = 10 , y = 60, height = 100, width = 380)
        regFileContent_scrollbar = tkinter.Scrollbar(self.MainWindow)
        self.regFileContent.config(yscrollcommand = regFileContent_scrollbar.set)
        regFileContent_scrollbar.config(command = self.regFileContent.yview)

        self.sendRegFileButton = tkinter.Button(self.MainWindow, text = 'Gởi nội dung', command = self.OnFileRegContentSend)
        self.sendRegFileButton.place(x = 400, y = 60, height = 100, width = 90)

        # Phân gửi trực tiếp
        self.directChangeFrame = tkinter.Frame(self.MainWindow, highlightbackground = "grey", bd = 1, highlightthickness = 0.5)
        self.directChangeFrame.place(x = 10, y = 180, height = 300, width = 480)

        self.directChangeFrameName = tkinter.Label(self.MainWindow, text = 'Sửa giá trị trực tiếp')
        self.directChangeFrameName.place(x = 20, y = 170, height = 20)

        self.registry_entry2 = tkinter.Entry(self.MainWindow)
        self.registry_entry2.insert(0, "Chọn chức năng")
        # self.registry_entry2.bind("<Button-1>", remove_text)
        self.registry_entry2.place(x = 20, y = 200, height = 20, width = 460)

        # down =b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x0e\x00\x00\x00\x07\x08\x06\x00\x00\x008G|\x19\x00\x00\x00\tpHYs\x00\x00\x10\x9b\x00\x00\x10\x9b\x01t\x89\x9cK\x00\x00\x00\x19tEXtSoftware\x00www.inkscape.org\x9b\xee<\x1a\x00\x00\x00OIDAT\x18\x95\x95\xce\xb1\x0e@P\x0cF\xe1\xefzI\x8fc$\x12\x111\x19\xec\x9e\x12\xcb\x95 A\x9d\xa4K\xff\x9e\xb6\t\x13J\xffX \xa1\xc7\x16\xac\x19\xc5\xb1!*\x8fy\xf6BB\xf7"\r_\xff77a\xcd\xbd\x10\xedI\xaa\xa3\xd2\xf9r\xf5\x14\xee^N&\x14\xab\xef\xa9\'\x00\x00\x00\x00IEND\xaeB`\x82'
        # imgDown = tkinter.PhotoImage(self.registry, down)

        # self.registry_button2 = tkinter.Menubutton()
        # self.registry_button2.place(x = 400, y = 20, height = 30, width = 90)

        self.registry_entry3 = tkinter.Entry(self.MainWindow)
        self.registry_entry3.insert(0, "Đường dẫn")
        self.registry_entry3.bind("<Button-1>", remove_text)
        self.registry_entry3.place(x = 20, y = 200, height = 20, width = 460)

        # self.registry_button2 = tkinter.Button(self.registry, text = 'Xem', command = self.view)
        # self.registry_button2.place(x = 140, y = 10, height = 60, width = 90)

        # self.registry_button3 = tkinter.Button(self.registry, text = 'Xóa', command = self.erase)
        # self.registry_button3.place(x = 240, y = 10, height = 60, width = 100)

        # self.registry_button4 = tkinter.Button(self.registry, text = 'Start', command = self.start)
        # self.registry_button4.place(x = 350, y = 10, height = 60, width = 100)
        
        self.MainWindow.protocol('WM_DELETE_WINDOW', self.OnExitGUI)
        self.MainWindow.mainloop()

    def Browse(self):
        # Mở cửa số tìm file (chắc tkinter có lệnh chứ)
        # Mở file đó bằng open
        # đọc content vô s
        # in s ra list_box của cửa sổ (self.regFileContent thì phải)
        pass 

    def OnFileRegContentSend(self):
        # lấy nội dung của cái list_box (self.regFileConent thì phải), cho vô biến data
        state, _ = self.client.MakeRequest("REGFILE " + data)
        if state == ClientState.SUCCEEDED:
            # In Thành công
            pass
        else:
            # In thất bại
            pass

    # Sửa ở trên đi phần này t sửa cho
    def RequestCreateKey(self, path):
        pass

    def RequestDeleteKey(self, path):
        pass

    def RequestGetValue(self, path, valuename):
        pass

    def RequestSetValue(self, path, valuename, type, value):
        pass

    def RequestDeleteValue(self, path, valuename):
        pass


itemlist = [
('Hyundai', 'brakes', '1') ,
('Honda', 'light', '2') ,
('Lexus', 'battery', '3') ,
('Benz', 'wiper', '4') ,
('Ford', 'tire', '5') ,
('Chevy', 'air', '6') ,
('Chrysler', 'piston', '1') ,
('Toyota', 'brake pedal', '2') ,
('BMW', 'seat', '3')
]


if __name__ == "__main__":
    a = Registry(None)
    a.ShowWindow()
    