from handler_state import HandlerState
from pathlib import Path, WindowsPath, PosixPath
import os
import shutil
import json

def PerformWalk(path):
    children = None
    for _, dirs, files in os.walk(path):
        children = dirs + files
        break
    return children

def MakePath(path):
    if type(path) != Path:
        path = Path(path)
    return path

def Split(s: str):
    items = s.split('\" \"')
    assert len(items) > 0
    items[0] = items[0].split('\"')[1]
    items[-1] = items[-1].split('\"')[0]
    return items

class DirectoryHandler():
    def __init__(self):
        self.root = None
        pass

    def SetRoot(self, path: Path):
        self.root = path

    def View(self, path: Path):
        if not os.path.isabs(path):
            path = self.root / path

        if path.exists():
            return PerformWalk(path)

    def Validate(self, paths):
        if type(paths) == Path:
            paths = [paths]
        
        paths = [self.root / x if os.path.isabs(x) else x for x in paths]

        for i in paths:
            if i.exists():
                return None

        return paths if len(paths) > 1 else paths[0]


    def Copy(self, src, dest: Path):
        src = self.Validate(src)
        dest = self.Validate(dest)
        assert src != None, "Invalid path(s) are presented in pathSrc"
        assert dest != None, "Invalid path(s) are presented in pathDest"

        if (src.is_dir()):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)

    def Cut(self, src, dest: Path):
        src = self.Validate(src)
        dest = self.Validate(dest)
        assert src != None, "Invalid path(s) are presented in pathSrc"
        assert dest != None, "Invalid path(s) are presented in pathDest"

        shutil.move(src, dest)

    def Delete(self, src):
        '''
        Please use with caution.
        '''
        src = self.Validate(src)
        assert src != None, "Invalid path(s) are presented in pathSrc"

        if (src.is_dir()):
            shutil.rmtree(src, True)
        else:
            os.remove(src)

    def Rename(self, src: Path, name: str):
        src = self.Validate(src)
        assert type(src) == Path, "Errornous implementation, src is not a Path object"
        
        dest = src.parent / name
        assert dest.exists(), str(dest) + " already exists."
        os.rename(src, dest)

    def Execute(self, reqCode:str, data:str):
        try:
            extraData = ""
            if reqCode == "VIEW":
                l = self.View(Path(reqCode))
                extraData = json.dumps(l)
            elif reqCode == "COPY":
                src = Split(data)
                assert len(src) >= 2
                dest = src.pop()
                self.Copy(src, dest)
            elif reqCode == "CUT":
                src = Split(data)
                assert len(src) >= 2
                dest = src.pop()
                self.Cut(src, dest)
            elif reqCode == "RENAME":
                src = Split(data)
                assert len(src) == 2
                name = src.pop()
                self.Rename(src, name)
            elif reqCode == "DELETE":
                src = Split(data)
                assert len(src) >= 1
                self.Delete(src)
            else:
                return HandlerState.INVALID, None

            return HandlerState.SUCCEEDED, extraData.encode("utf-8")

        except Exception as e:
            print(e)
            return HandlerState.FAILED, None
        pass

if __name__ == "__main__":
    pass