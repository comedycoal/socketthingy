from os import close
from posixpath import expanduser
import sys
from tkinter.constants import S
from PySide2.QtCore import *
from PySide2 import QtGui, QtWidgets
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from client import ClientState
from request_gui import Request

class ReactiveQLineEdit(QLineEdit):
    def __init__(self, normalStyle, forcedEditStyle):
        super().__init__()
        self.justAfterForcedSet = False
        self.normalStyle = normalStyle
        self.forcedEditStyle = forcedEditStyle
        self.setStyleSheet(self.normalStyle)
        self.textChanged[str].connect(self.onChange)

    def onChange(self, text):
        if self.justAfterForcedSet:
            self.setStyleSheet(self.normalStyle)
            self.setText("")
            self.justAfterForcedSet = False

    def ForceSetText(self, text):
        self.setText(text)
        self.setStyleSheet(self.forcedEditStyle)
        self.justAfterForcedSet = True

class ReactiveQComboBox(QComboBox):
    def __init__(self, normalStyle, forcedEditStyle):
        super().__init__()
        self.normalStyle = normalStyle
        self.forcedEditStyle = forcedEditStyle
        self.setStyleSheet(self.normalStyle)
        self.activated.connect(self.onChange)

    def onChange(self, text):
        self.setStyleSheet(self.normalStyle)

    def ForceSetCurrentIndex(self, index):
        self.setCurrentIndex(index)
        self.setStyleSheet(self.forcedEditStyle)

class RegistryUI(Request):
    VALUE_FORCED_EDIT_STYLE = "color: green"
    VALUE_NORMAL_STYLE = "color: black"

    RegistryTypes = {
        "BINARY": 0,
        "DWORD": 1,
        "QWORD": 2,
        "STRING": 3,
        "MULTISTRING": 4,
        "EXPANDABLESTRING": 5
    }

    def __init__(self, parentWindow, client):
        super().__init__(parentWindow, client, 'REGISTRY')

    def setupUI(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Registry"))
        self.resize(500,400)

        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(10)
        style = "background-color: rgb(224, 237, 255)"

        self.sectionFileLabel = QLabel()
        self.sectionFileLabel.setFont(font)
        self.sectionFileLabel.setAlignment(Qt.AlignHCenter)
        self.sectionFileLabel.setObjectName("sectionValueLabel")
        self.sectionFileLabel.setText(QCoreApplication.translate("MainWindow", "Sửa Registry bằng tập tin"))

        self.filePathBox = QLineEdit()
        self.filePathBox.setFont(font)
        self.filePathBox.setDisabled(True)
        self.filePathBox.setObjectName("filePathBox")

        self.openFileButton = QPushButton(clicked = self.onBrowseForFile)
        self.openFileButton.setFont(font)
        self.openFileButton.setStyleSheet(style)
        self.openFileButton.setText(QCoreApplication.translate("MainWindow", 'Browse...'))

        self.fileContentView = QTextEdit()
        self.fileContentView.setFont(font)
        self.fileContentView.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.fileContentView.setObjectName("regFileView")
        self.fileContentView.setReadOnly(True)
        self.fileContentView.setText(QCoreApplication.translate("MainWindow", ""))

        self.fileSendButton = QPushButton(clicked = self.onSendFileButton)
        self.fileSendButton.setFont(font)
        self.fileSendButton.setStyleSheet(style)
        self.fileSendButton.setText(QCoreApplication.translate("MainWindow", 'Gửi'))

        self.sectionValueLabel = QLabel()
        self.sectionValueLabel.setFont(font)
        self.sectionValueLabel.setAlignment(Qt.AlignHCenter)
        self.sectionValueLabel.setObjectName("sectionValueLabel")
        self.sectionValueLabel.setText(QCoreApplication.translate("MainWindow", "Sửa Registry trực tiếp"))

        self.keyBox = ReactiveQLineEdit(RegistryUI.VALUE_NORMAL_STYLE, RegistryUI.VALUE_FORCED_EDIT_STYLE)
        self.keyBox.setFont(font)
        self.keyBox.setObjectName("dir_box")
        self.keyBox.setText(QCoreApplication.translate("MainWindow", "HKEY_CURRENT_USER\\Some_key"))

        self.valueNameBox = ReactiveQLineEdit(RegistryUI.VALUE_NORMAL_STYLE, RegistryUI.VALUE_FORCED_EDIT_STYLE)
        self.valueNameBox.setFont(font)
        self.valueNameBox.setObjectName("subkey_box")
        self.valueNameBox.setText(QCoreApplication.translate("MainWindow", "SomeSubkey"))

        self.valueTypeBox = ReactiveQComboBox(RegistryUI.VALUE_NORMAL_STYLE, RegistryUI.VALUE_FORCED_EDIT_STYLE)
        self.valueTypeBox.setFont(font)
        self.valueTypeBox.setObjectName("type_box")
        self.valueTypeBox.addItems(sorted(RegistryUI.RegistryTypes, key=RegistryUI.RegistryTypes.get))

        self.valueDataBox = ReactiveQLineEdit(RegistryUI.VALUE_NORMAL_STYLE, RegistryUI.VALUE_FORCED_EDIT_STYLE)
        self.valueDataBox.setFont(font)
        self.valueDataBox.setObjectName("value_box")
        self.valueDataBox.setText(QCoreApplication.translate("MainWindow", "DATA"))

        self.getValueButton = QPushButton(clicked = self.onGetValueButton)
        self.getValueButton.setFont(font)
        self.getValueButton.setStyleSheet(style)
        self.getValueButton.setText(QCoreApplication.translate("MainWindow", 'Get Value'))

        self.setValueButton = QPushButton(clicked = self.onSetValueButton)
        self.setValueButton.setFont(font)
        self.setValueButton.setStyleSheet(style)
        self.setValueButton.setText(QCoreApplication.translate("MainWindow", 'Set value'))

        self.deleteValueButton = QPushButton(clicked = self.onDeleteValueButton)
        self.deleteValueButton.setFont(font)
        self.deleteValueButton.setStyleSheet(style)
        self.deleteValueButton.setText(QCoreApplication.translate("MainWindow", 'Delete value'))

        self.createKeyButton = QPushButton(clicked = self.onCreateKeyButton)
        self.createKeyButton.setFont(font)
        self.createKeyButton.setStyleSheet(style)
        self.createKeyButton.setText(QCoreApplication.translate("MainWindow", 'Create key'))

        self.deleteKeyButton = QPushButton(clicked = self.onDeleteKeyButton)
        self.deleteKeyButton.setFont(font)
        self.deleteKeyButton.setStyleSheet(style)
        self.deleteKeyButton.setText(QCoreApplication.translate("MainWindow", 'Delete Key'))


        mainLayout = QVBoxLayout()

        fileLayout = QHBoxLayout()
        fileLayout.addWidget(self.filePathBox)
        fileLayout.addWidget(self.openFileButton)

        mainLayout.addWidget(self.sectionFileLabel)
        mainLayout.addLayout(fileLayout)
        mainLayout.addWidget(self.fileContentView)
        mainLayout.addWidget(self.fileSendButton)
        mainLayout.addSpacing(20)


        def MakeLabel(text):
            label = QLabel(text)
            label.setFont(font)
            label.setObjectName("text"+"_label")
            return label

        valueLayout = QFormLayout()
        valueLayout.addRow(MakeLabel("Key:      "), self.keyBox)
        valueLayout.addRow(MakeLabel("Subkey:   "), self.valueNameBox)
        valueLayout.addRow(MakeLabel("Type:     "), self.valueTypeBox)
        valueLayout.addRow(MakeLabel("Value:    "), self.valueDataBox)

        valueButtonLayout = QHBoxLayout()
        valueButtonLayout.addWidget(self.getValueButton)
        valueButtonLayout.addWidget(self.setValueButton)
        valueButtonLayout.addWidget(self.deleteValueButton)
        valueButtonLayout.addWidget(self.createKeyButton)
        valueButtonLayout.addWidget(self.deleteKeyButton)


        mainLayout.addWidget(self.sectionValueLabel)
        mainLayout.addLayout(valueLayout)
        mainLayout.addLayout(valueButtonLayout)

        self.setLayout(mainLayout)

    def onBrowseForFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open .reg file", r"C:", "Registry Files (*.reg)", options=options
        )
        if filename:
            self.filePathBox.setText(filename)
            with open(filename, "r") as f:
                content = f.read()
                self.fileContentView.setText(QCoreApplication.translate("MainWindow", content))
        pass

    def onSendFileButton(self):
        content = self.fileContentView.toPlainText()
        state, _ = self.client.MakeRequest("REGFILE " + content)
        if state == ClientState.NOCONNECTION:
            QMessageBox.about(self, "", "Chưa kết nối đến server")
        elif state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Thao tác thất bại")
        else:
            QMessageBox.about(self, "", "Sửa thành công")

    def GetKeyAndValueInformation(self):
        return (self.keyBox.text(), self.valueNameBox.text(), str(self.valueTypeBox.currentText()), self.valueDataBox.text())
        pass

    def SetKeyAndValueInformation(self, key=None, valueName=None, valueType=None, valueData=None):
        values = [key, valueName, valueType, valueData]
        affectedBoxes = []
        affectedBoxes.append(self.keyBox if key else None)
        affectedBoxes.append(self.valueNameBox if valueName else None)
        affectedBoxes.append(self.valueTypeBox if valueType else None)
        affectedBoxes.append(self.valueDataBox if valueData else None)

        for i in range(0, len(affectedBoxes)):
            box = affectedBoxes[i]
            if i == 2 and box:
                box.ForceSetCurrentIndex(RegistryUI.RegistryTypes.get(valueType, -1))
            elif box:
                box.ForceSetText(values[i])

    def onGetValueButton(self):
        keypath, name, _, _ = self.GetKeyAndValueInformation()
        state, data = self.client.MakeRequest("GETVALUE " + keypath + ' ' + name)
        try:
            if state == ClientState.NOCONNECTION:
                QMessageBox.about(self, "", "Chưa kết nối đến server")
            elif state != ClientState.SUCCEEDED:
                QMessageBox.about(self, "", "Thao tác thất bại")
            else:
                parts = data.decode('utf-8').rsplit(' ', 1)
                value = parts[0]
                t = parts[1]
                self.SetKeyAndValueInformation(None, None, t, value)
        except Exception as e:
            print(e)
            QMessageBox.about(self, "", "Dữ liệu trả về lỗi")

    def onSetValueButton(self):
        keypath, name, t, value = self.GetKeyAndValueInformation()
        state, _ = self.client.MakeRequest("SETVALUE " + ' '.join([keypath, name, t, value]))
        if state == ClientState.NOCONNECTION:
            QMessageBox.about(self, "", "Chưa kết nối đến server")
        elif state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Thao tác thất bại")
        else:
            QMessageBox.about(self, "", "Sửa thành công")

    def onDeleteValueButton(self):
        keypath, name, t, _ = self.GetKeyAndValueInformation()
        state, _ = self.client.MakeRequest("DELETEVALUE " + ' '.join([keypath, name]))
        if state == ClientState.NOCONNECTION:
            QMessageBox.about(self, "", "Chưa kết nối đến server")
        elif state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Thao tác thất bại")
        else:
            self.SetKeyAndValueInformation(None, None, -1, "")

    def onCreateKeyButton(self):
        keypath, _ , _, _ = self.GetKeyAndValueInformation()
        state, _ = self.client.MakeRequest("CREATEKEY " + keypath)
        if state == ClientState.NOCONNECTION:
            QMessageBox.about(self, "", "Chưa kết nối đến server")
        elif state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Thao tác thất bại")
        else:
            QMessageBox.about(self, "", "Tạo Key thành công")
            self.SetKeyAndValueInformation(None, "", -1, "")
        pass

    def onDeleteKeyButton(self):
        keypath, _ , _, _ = self.GetKeyAndValueInformation()
        state, _ = self.client.MakeRequest("DELETEKEY " + keypath)
        if state == ClientState.NOCONNECTION:
            QMessageBox.about(self, "", "Chưa kết nối đến server")
        elif state != ClientState.SUCCEEDED:
            QMessageBox.about(self, "", "Thao tác thất bại")
        else:
            QMessageBox.about(self, "", "Xoá Key thành công")
            self.SetKeyAndValueInformation(keypath, "", -1, "")

    def ShowWindow(self):
        self.setupUI()
        self.show()
        pass

if __name__ == '__main__':
    from os import environ
    import client

    def suppress_qt_warnings():
        environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        environ["QT_SCALE_FACTOR"] = "1"

    suppress_qt_warnings()

    app = QtWidgets.QApplication(sys.argv)
    tmp = client.ClientProgram()
    demo = RegistryUI(None, tmp)
    demo.ShowWindow()
    sys.exit(app.exec_())