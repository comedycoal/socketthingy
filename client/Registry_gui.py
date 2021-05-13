import tkinter
from tkinter import ttk
from tkinter import filedialog

import codecs
from tkinter.messagebox import showinfo

from Request_gui import Request
from client import ClientState


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
        self.regFilePathInputBox.place(x = 10, y = 20, height = 30, width = 380)

        self.browseButton = tkinter.Button(self.MainWindow, text = 'Browse...', command = self.Browser)
        self.browseButton.place(x = 400, y = 20, height = 30, width = 90)

        self.regFileContent = tkinter.Text(self.MainWindow)
        self.regFileContent.insert(tkinter.END, "Nội dung")
        self.regFileContent.place(x = 10 , y = 60, height = 100, width = 380)
        regFileContent_scrollbar = ttk.Scrollbar(self.MainWindow)
        self.regFileContent.config(yscrollcommand = regFileContent_scrollbar.set)
        regFileContent_scrollbar.config(command = self.regFileContent.yview)

        sendRegFileButton = tkinter.Button(self.MainWindow, text = 'Gởi nội dung', command = self.OnFileRegContentSend)
        sendRegFileButton.place(x = 400, y = 60, height = 100, width = 90)

        # Phân gửi trực tiếp
        directChangeFrame = tkinter.Frame(self.MainWindow, highlightbackground = "grey", bd = 1, highlightthickness = 0.5)
        directChangeFrame.place(x = 10, y = 180, height = 300, width = 480)

        directChangeFrameName = tkinter.Label(self.MainWindow, text = 'Sửa giá trị trực tiếp')
        directChangeFrameName.place(x = 20, y = 170, height = 20)
        
        function = ('Get value', 'Set value', 'Delete value', 'Create key', 'Delete key')
        n1 = tkinter.StringVar()
        self.registry_FunctionBox = ttk.Combobox(self.MainWindow, textvariable = n1, values = function, state = 'normal')
        self.registry_FunctionBox.insert(tkinter.END, 'Chọn chức năng')
        self.registry_FunctionBox.place(x = 20, y = 200, height = 25, width = 460)
        self.registry_FunctionBox.bind('<<ComboboxSelected>>', self.onFunction)

        self.registry_entry = tkinter.Entry(self.MainWindow)
        self.registry_entry.insert(0, "Đường dẫn")
        self.registry_entry.place(x = 20, y = 235, height = 25, width = 460)

        self.createNameValueBox()

        self.createValueBox()
        
        self.createDatatypeBox()

        self.registry_listbox = tkinter.Listbox(self.MainWindow)
        self.registry_listbox.place(x = 20, y = 305, height = 130, width = 460)

        registry_sendButton = tkinter.Button(self.MainWindow, text = 'Gởi', command = self.onSending)
        registry_sendButton.place(x = 140, y = 445, height = 25, width = 80)

        registry_clearButton = tkinter.Button(self.MainWindow, text = 'Xóa', command = self.onClearing)
        registry_clearButton.place(x = 270, y = 445, height = 25, width = 80)

        self.MainWindow.protocol('WM_DELETE_WINDOW', self.OnExitGUI)
        self.MainWindow.mainloop()

    def createNameValueBox(self):
        self.registry_ValueNameBox = tkinter.Entry(self.MainWindow)
        self.registry_ValueNameBox.insert(0, "Name value")
        self.registry_ValueNameBox.place(x = 20, y = 270, height = 25, width = 140)

    def createValueBox(self):
        self.registry_ValueBox = tkinter.Entry(self.MainWindow)
        self.registry_ValueBox.insert(0, "Value")
        self.registry_ValueBox.place(x = 170, y = 270, height = 25, width = 150)

    def createDatatypeBox(self):
        datatype = ('String', 'Binary', 'DWORD', 'QWORD', 'Multi-String', 'Expandable String')
        n2 = tkinter.StringVar()
        self.registry_DatatypeBox = ttk.Combobox(self.MainWindow, textvariable = n2, values = datatype, state = 'normal')
        self.registry_DatatypeBox.insert(tkinter.END, "Kiểu dữ liệu")
        self.registry_DatatypeBox.place(x = 330, y = 270, height = 25, width = 150)

    def Browser(self):
        filename = filedialog.askopenfilename(initialdir = 'C:', title = 'Open', 
            filetypes = (('reg files', '*.reg'), ('all files', '*.*')))
        self.regFilePathInputBox.delete(0, tkinter.END)
        self.regFilePathInputBox.insert(0, filename)
        
        regFile = codecs.open(filename, encoding = 'utf_8')
        regContent = regFile.read()
        regFile.close()
        self.regFileContent.delete('1.0', tkinter.END)
        self.regFileContent.insert(tkinter.END, regContent)
        

    def OnFileRegContentSend(self):
        data = self.regFileContent.get('1.0', tkinter.END)
        state, _ = self.client.MakeRequest("REGFILE " + data)
        if state == ClientState.SUCCEEDED:
            showinfo(title = '', message = 'Sửa thành công')
        else:
            showinfo(title = '', message = 'Sửa thất bại')
            pass

    def onFunction(self, event):
        try:
            msg = self.registry_FunctionBox.get()
            path = self.registry_entry.get()
            valuename = None
            value = None
            type = None
            if msg == 'Get value':
                if self.registry_ValueNameBox == None:
                    self.createNameValueBox()
                if self.registry_ValueBox:
                    self.registry_ValueBox.destroy()
                    self.registry_ValueBox = None
                if self.registry_DatatypeBox:
                    self.registry_DatatypeBox.destroy()
                    self.registry_DatatypeBox = None

            elif msg == 'Set value':
                if self.registry_ValueNameBox == None:
                    self.createNameValueBox()
                if self.registry_ValueBox == None:
                    self.createValueBox()
                if self.registry_DatatypeBox == None:
                    self.createDatatypeBox()

            elif msg == 'Delete value':
                if self.registry_ValueNameBox == None:
                    self.createNameValueBox()
                if self.registry_ValueBox:
                    self.registry_ValueBox.destroy()
                    self.registry_ValueBox = None
                if self.registry_DatatypeBox:
                    self.registry_DatatypeBox.destroy()
                    self.registry_DatatypeBox = None

            elif msg == 'Create key':
                if self.registry_ValueNameBox:
                    self.registry_ValueNameBox.destroy()
                    self.registry_ValueNameBox = None
                if self.registry_ValueBox:
                    self.registry_ValueBox.destroy()
                    self.registry_ValueBox = None
                if self.registry_DatatypeBox:
                    self.registry_DatatypeBox.destroy()
                    self.registry_DatatypeBox = None

            elif msg == 'Delete key':
                if self.registry_ValueNameBox:
                    self.registry_ValueNameBox.destroy()
                    self.registry_ValueNameBox = None
                if self.registry_ValueBox:
                    self.registry_ValueBox.destroy()
                    self.registry_ValueBox = None
                if self.registry_DatatypeBox:
                    self.registry_DatatypeBox.destroy()
                    self.registry_DatatypeBox = None
        except Exception as e:
            showinfo(title = '', message = e)
        pass

    def RequestGetValue(self, path, valuename):
        if self.registry_ValueNameBox == None:
            self.createNameValueBox()
        if self.registry_ValueBox:
            self.registry_ValueBox.destroy()
            self.registry_ValueBox = None
        if self.registry_DatatypeBox:
            self.registry_DatatypeBox.destroy()
            self.registry_DatatypeBox = None

        valuename = self.registry_ValueNameBox.get()
        state, data = self.client.MakeRequest("GETVALUE " + path + ' ' + valuename)

        if state == ClientState.SUCCEEDED:
            self.registry_listbox.insert(tkinter.END, data)
        else:
            self.registry_listbox.insert(tkinter.END, 'Lỗi')
        pass

    def RequestSetValue(self, path, valuename, type, value):
        valuename = self.registry_ValueNameBox.get()
        value = self.registry_ValueBox.get()
        type = self.registry_DatatypeBox.get()
        
        dtype = ['STRING', 'BINARY', 'DWORD', 'QWORD', 'MULTISTRING', 'EXPANDABLESTRING']
        if type == 'String':
            datatype = dtype[0]
        elif type == 'Binary':
            datatype = dtype[1]
        if type == 'DWORD':
            datatype = dtype[2]
        elif type == 'QWORD':
            datatype = dtype[3]
        elif type == 'Multi-String':
            datatype = dtype[4]
        elif type == 'Expdandable String':
            datatype = dtype[5]

        state, _ = self.client.MakeRequest("SETVALUE " + path + " " + valuename + " " + datatype + " " + value)
        if state != ClientState.SUCCEEDED or datatype not in dtype:
            self.registry_listbox.insert(tkinter.END, 'Lỗi')
        else:
            self.registry_listbox.insert(tkinter.END, 'Set value thành công')

        pass

    def RequestDeleteValue(self, path, valuename):
        valuename = self.registry_ValueNameBox.get()
        state, _ = self.client.MakeRequest("DELETEVALUE " + path + " " + valuename)
        if state == ClientState.SUCCEEDED:
            self.registry_listbox.insert(tkinter.END, 'Xóa value thành công')
        else:
            self.registry_listbox.insert(tkinter.END, 'Lỗi')

        pass

    def RequestCreateKey(self, path):
        state, _ = self.client.MakeRequest("CREATEKEY " + path)
        if state == ClientState.SUCCEEDED:
            self.registry_listbox.insert(tkinter.END, 'Tạo key thành công')
        else:
            self.registry_listbox.insert(tkinter.END, 'Lỗi')
        
        pass

    def RequestDeleteKey(self, path):
        state, _ = self.client.MakeRequest("DELETEKEY " + path)
        if state == ClientState.SUCCEEDED:
            self.registry_listbox.insert(tkinter.END, 'Xóa key thành công')
        else:
            self.registry_listbox.insert(tkinter.END, 'Lỗi')
        
        pass
    
    def onSending(self):
        try:
            msg = self.registry_FunctionBox.get()
            path = self.registry_entry.get()
            valuename = None
            value = None
            type = None
            if msg == 'Get value':  
                self.RequestGetValue(path, valuename)
            elif msg == 'Set value':
                self.RequestSetValue(path, valuename, type, value)
            elif msg == 'Delete value':
                self.RequestDeleteValue(path, valuename)
            elif msg == 'Create key':
                self.RequestCreateKey(path)
            elif msg == 'Delete key':
                self.RequestDeleteKey(path)
        except Exception as e:
            showinfo(title = '', message = e)
        
        pass

    def onClearing(self):
        self.registry_listbox.delete(0, tkinter.END)
        pass

if __name__ == "__main__":
    a = Registry(None)
    a.ShowWindow()
    