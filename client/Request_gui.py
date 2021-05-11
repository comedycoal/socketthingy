import client

class Request_GUI:
    def __init__(self, clientProgram:client.ClientProgram, baseRequest:str):
        self.client = clientProgram
        self.baseRequest = baseRequest

    #Override this if Screenshot_GUI since extraData needs processing
    def OnStartGUI(self):
        state, _ = self.MakeBaseRequest()
        if state != client.ClientState.SUCCEEDED:
            #Error box
            return

        self.ShowWindow()

    def OnExitGUI(self):
        state = self.MakeFinishRequest()
        if state != client.ClientState.SUCCEEDED:
            # Error box: server is not responding
            return

        # Đóng cửa sổ :v? đk ko nhỉ

    def MakeBaseRequest(self):
        state, extraData = self.client.MakeRequest(self.baseRequest)
        return state, extraData

    def MakeFinishRequest(self):
        state, _ = self.client.MakeRequest("FINISH")
        return state

    def ShowWindow(self):
        # Override this in children class
        pass