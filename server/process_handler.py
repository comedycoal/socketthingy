import wmi

class ProcessHandler():
    def __init__(self):
        self.conn = wmi.WMI()
        self.processes = []
        pass

    def Handle(self):
        pass

    def FetchAndUpdate(self):
        list_processes = None
        if self.conn:
            self.processes = self.conn.Win32_Process()
            list_processes = [(x.ProcessID, x.Name, x.ThreadCount) for x in processes]
        else:
            # Raise exception
            pass
        
        return list_processes

    def KillProcess(self, id):
        to_kill = [x for x in self.processes if x.ProcessID == id]
        for item in to_kill:
            item.Terminate()

    def StartProcess(self, name):
        process = name + ".exe"
        processID, result = self.conn.Win_32Process.Create(
            CommandLine=process,
            ProcessStartupInformation=process_startup
        )

        if result == 0:
            #Success
            pass
        else:
            #Failure
            pass



if __name__ == "__main__":
    a = ProcessHandler()