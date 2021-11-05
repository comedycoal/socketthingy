from handler_state import HandlerState
from pathlib import Path, WindowsPath, PosixPath
import os
import string
import socket
import shutil
import json
import traceback

def PerformWalk(path):
    children = None
    for _, dirs, files in os.walk(path):
        children = [(x, 1) for x in dirs]  + [(x, 0) for x in files]
        break
    return children

def Split(s: str):
    items = s.split('\" \"')
    assert len(items) > 0
    return [x.strip('\"') for x in items]

class DirectoryHandler():
    def __init__(self):
        self.root = None
        pass

    def SetRoot(self, path: Path):
        self.root = path

    def Init(self):
        return ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]

    def View(self, path: Path):
        if not os.path.isabs(path):
            path = self.root / path
        else:
            self.root = path

        if path.exists():
            return PerformWalk(path)

    def Validate(self, paths, keep_list = True):
        if type(paths) != list:
            paths = [paths]
        paths = [self.root / x if not os.path.isabs(x) else x for x in paths]

        paths = [x for x in paths if x.exists()]

        if len(paths) == 0: return None
        return paths[0] if not keep_list and len(paths) == 1 else paths


    def Copy(self, src, dest: Path):
        src = self.Validate(src)
        dest = self.Validate(dest, keep_list=False)
        assert src != None, "Invalid path(s) are presented in pathSrc"
        assert dest != None, "Invalid path(s) are presented in pathDest"

        for path in src:
            i = 1
            ides = dest / path.name
            while ides.exists():
                ides = dest / (path.stem + "_" + str(i) + path.suffix)
                i += 1
            if (path.is_dir()):
                shutil.copytree(path, ides)
            else:
                shutil.copy2(path, ides)

    def Cut(self, src, dest: Path):
        src = self.Validate(src)
        dest = self.Validate(dest, keep_list=False)
        assert src != None, "Invalid path(s) are presented in pathSrc"
        assert dest != None, "Invalid path(s) are presented in pathDest"
        for path in src:
            i = 1
            ides = dest / path.name
            while ides.exists():
                ides = dest / (path.stem + "_" + str(i) + path.suffix)
                i += 1
            
            os.rename(path, ides)

    def Delete(self, src):
        '''
        Please use with caution.
        '''
        src = self.Validate(src)
        assert src != None, "Invalid path(s) are presented in pathSrc"

        for path in src:
            if (path.is_dir()):
                shutil.rmtree(path, True)
            else:
                os.remove(path)

    def Rename(self, src: Path, name: str):
        src = self.Validate(src, keep_list=False)
        assert src != None, "Invalid path is presented in src"

        dest = src.parent / name
        print(dest)
        assert not dest.exists(), str(dest) + " already exists."
        os.rename(src, dest)

    def ReceiveFile(self, dest: Path, data):
        with open(dest, "wb") as f:
            f.write(data)

    def Execute(self, reqCode, data):
        try:
            extraData = ""
            if reqCode == "INIT":
                l = self.Init()
                extraData = json.dumps(l)
            elif reqCode == "VIEW":
                data = data.strip('\"')
                l = self.View(Path(data))
                extraData = json.dumps(l)
            elif reqCode == "COPY":
                src = Split(data)
                assert len(src) >= 2
                dest = src.pop()
                self.Copy([Path(x) for x in src], Path(dest))
            elif reqCode == "CUT":
                src = Split(data)
                assert len(src) >= 2
                dest = src.pop()
                self.Cut([Path(x) for x in src], Path(dest))
            elif reqCode == "RENAME":
                src = Split(data)
                assert len(src) == 2
                name = src.pop()
                self.Rename(Path(src[0]), name)
            elif reqCode == "DELETE":
                src = Split(data)
                assert len(src) >= 1
                self.Delete([Path(x) for x in src])
            elif reqCode == "TRANSFER":
                dest_start = data.find(b'"')
                assert dest_start == 0, "Wrong data format"
                dest_end = data.find(b'"', dest_start + 1)
                assert dest_end != -1, "Wrong data format"
                dest = Split(data[dest_start: dest_end+1].decode('utf-8'))[0]
                data = data[dest_end+1+1:]
                self.ReceiveFile(Path(dest), data)
                pass
            else:
                return HandlerState.INVALID, None

            return HandlerState.SUCCEEDED, extraData.encode("utf-8")

        except Exception as e:
            traceback.print_exc()
            return HandlerState.FAILED, None
        pass

if __name__ == "__main__":
    a = DirectoryHandler()
    b = None
    with open("README.docx", "rb") as f:
        f.seek(0,2)
        l = f.tell()
        f.seek(0,0)
        b = f.read(l)
    b = b'"README2.docx" ' + b
    a.Execute("TRANSFER", b)