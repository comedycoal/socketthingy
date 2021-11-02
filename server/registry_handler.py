from handler_state import HandlerState
import winreg
import subprocess
import os
import ctypes
import traceback
from pathlib import Path

TEMP_PATH = os.path.join(Path(__file__).parent.absolute(),"temp\\tempreg.reg")

def StringToBytes(string):
    return bytes([int(i) for i in string])

class RegistryHandler:
    Types = {
        "BINARY": winreg.REG_BINARY,
        "DWORD": winreg.REG_DWORD,
        "QWORD": winreg.REG_QWORD,
        "STRING": winreg.REG_SZ,
        "MULTISTRING": winreg.REG_MULTI_SZ,
        "EXPANDABLESTRING": winreg.REG_EXPAND_SZ,
    }

    def __init__(self):
        pass

    def Execute(self, reqCode:str, data:str):
        try:
            extraData = ""
            if reqCode == "REGFILE":
                with open(TEMP_PATH, "w") as file:
                    file.write(data)
                    file.close()
                    self.UseRegFile(os.path.join(Path().absolute(), TEMP_PATH))

            elif reqCode == "CREATEKEY":
                self.CreateKey(data)

            elif reqCode == "DELETEKEY":
                self.DeleteKey(data)

            elif reqCode == "GETVALUE":
                a = data.split(' ', 1)
                assert len(a) == 2
                extraData = self.GetValue(a[0], a[1])

            elif reqCode == "SETVALUE":
                print(data)
                a = data.split(' ', 3)
                assert len(a) == 4

                typeStr = a[2]
                value = a[3]
                if typeStr in ["DWORD", "QWORD"]:
                    value = int(value)
                elif typeStr == "BINARY":
                    value = bytes.fromhex(value)
                elif typeStr == "MULTISTRING":
                    value = value.split('\n')

                self.SetValue(a[0], a[1], RegistryHandler.Types[typeStr], value)

            elif reqCode == "DELETEVALUE":
                a = data.split(' ', 1)
                assert len(a) == 2
                extraData = self.DeleteValue(a[0], a[1])
            else:
                return HandlerState.INVALID, None

            if type(extraData) is bytes:
                extraData = extraData.hex()
            elif type(extraData) is not str:
                extraData = str(extraData)

            return HandlerState.SUCCEEDED, extraData.encode('utf-8')
        except Exception as e:
            traceback.print_exc()
            return HandlerState.FAILED, None

    def UseRegFile(self, filepath):
        ctypes.windll.shell32.ShellExecuteA
        subprocess.Popen(f"regedit /s \"{filepath}\"")

    def GetValue(self, keyPath, valueName):
        key = self.GetKeyHandle(keyPath, winreg.KEY_QUERY_VALUE)
        info = winreg.QueryValueEx(key, valueName)
        winreg.CloseKey(key)
        return info[0]

    def SetValue(self, keyPath, valueName, typeValue, value):
        key = self.GetKeyHandle(keyPath, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, valueName, 0, typeValue, value)
        winreg.CloseKey(key)

    def DeleteValue(self, keyPath, valueName):
        key = self.GetKeyHandle(keyPath, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, valueName)
        winreg.CloseKey(key)

    def CreateKey(self, keyPath):
        base, sub = self.GetSeperatedBaseAndSubKey(keyPath)
        key = winreg.OpenKeyEx(base, None, 0, winreg.KEY_CREATE_SUB_KEY)
        winreg.CreateKey(key, sub)
        winreg.CloseKey(key)

    def DeleteKey(self, keyPath):
        base, sub = self.GetSeperatedBaseAndSubKey(keyPath)
        key = winreg.OpenKeyEx(base, None, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteKey(key, sub)
        winreg.CloseKey(key)

    def GetKeyHandle(self, keyPath, access):
        base, sub = self.GetSeperatedBaseAndSubKey(keyPath)
        key = None
        key = winreg.OpenKeyEx(base, sub, 0, access)
        return key
    
    def GetSeperatedBaseAndSubKey(self, string):
        print(string)
        splitted = string.split('\\', 1)
        assert len(splitted) == 2

        baseStr = splitted[0]
        base = None
        if baseStr == "HKEY_CLASSES_ROOT":
            base = winreg.HKEY_CLASSES_ROOT
        elif baseStr == "HKEY_CURRENT_USER":
            base = winreg.HKEY_CURRENT_USER
        elif baseStr == "HKEY_LOCAL_MACHINE":
            base = winreg.HKEY_LOCAL_MACHINE
        elif baseStr == "HKEY_USERS":
            base = winreg.HKEY_USERS
        elif baseStr == "HKEY_PERFORMANCE_DATA":
            base = winreg.HKEY_PERFORMANCE_DATA
        elif baseStr == "HKEY_CURRENT_CONFIG":
            base = winreg.HKEY_CURRENT_CONFIG
        elif baseStr == "HKEY_DYN_DATA":
            base = winreg.HKEY_DYN_DATA
        assert base != None

        sub = splitted[1]

        return base, sub


if __name__ == "__main__":
    a = RegistryHandler()
    #state, m = a.Execute("GETVALUE", "HKEY_CURRENT_USER\\Test aaaa")
    a.UseRegFile(TEMP_PATH)
    #print(m)