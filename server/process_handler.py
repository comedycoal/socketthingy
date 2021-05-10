import psutil
import json
import subprocess
from handler_state import HandlerState

class ProcessHandler(): 
    def __init__(self):
        self.processes = None
        pass

    def Execute(self, reqCode:str, data:str):
        try:
            print(reqCode)
            newData = None
            if reqCode == "FETCH":
                newData = self.FetchAndUpdate()
            elif reqCode == "KILL":
                self.KillProcess(int(data))
                newData = self.FetchAndUpdate()
            elif reqCode == "START":
                self.StartProcess(data)
                newData = self.FetchAndUpdate()
            else:
                return HandlerState.INVALID, None          
            return HandlerState.SUCCEEDED, json.dumps(newData).encode("utf-8")

        except Exception as e:
            print(e)
            return HandlerState.FAILED, None

    def FetchAndUpdate(self):
        self.processes = psutil.process_iter(['pid', 'name', 'num_threads'])
        list_processes = [x.info for x in self.processes]
        return list_processes

    def FetchWithPIDs(self, pids):
        list_processes = []
        for pid in pids:
            if psutil.pid_exists(pid):
                pr = psutil.Process(pid)
                list_processes.append(pr.as_dict(['pid', 'name', 'num_threads']))
        return list_processes

    def KillProcess(self, id):
        to_kill = psutil.Process(id)
        to_kill.kill()

    def StartProcess(self, name):
        process = name + ".exe"
        subprocess.Popen(process)



if __name__ == "__main__":
    a = ProcessHandler()
    state, m = a.Execute("FETCH", "")
    print(state, m)
    