import psutil
import subprocess
from handler_state import HandlerState

class ProcessHandler():
    def __init__(self):
        self.processes = None
        pass

    def Handle(self):
        pass

    def FetchAndUpdate(self):
        self.processes = psutil.process_iter(['pid', 'name', 'num_threads'])
        list_processes = [x.info for x in self.processes]
        return list_processes

    def FetchWithPIDs(self, pids):
        list_processes = []
        for pid in pids:
            try:
                pr = psutil.Process(pid)
                list_processes.append(pr.as_dict(['pid', 'name', 'num_threads']))
            except psutil.NoSuchProcess:
                pass
        return list_processes

    def KillProcess(self, id):
        try:
            to_kill = psutil.Process(id)
            to_kill.kill()
        except psutil.NoSuchProcess:
            pass

    def StartProcess(self, name):
        process = name + ".exe"
        try:
            subprocess.Popen(process)
        except FileNotFoundError:
            print("File not found")
        



if __name__ == "__main__":
    a = ProcessHandler()
    li = a.FetchAndUpdate()
    for item in li:
        print(item)

    a.StartProcess("notepad")