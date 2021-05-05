class ApplicationHandler:
    pass
class RegistryHandler:
    pass
class KeyStrokeHandler:
    pass
class ScreenshotHandler:
    pass
class ExitHandler:
    pass

class HandlerState(Enum):
    UNKNOWN
    CREATED
    PROCESSING
    FAILED
    SUCCEEDED

class Handler:
    def __init__(self):
        self.state = HandlerState.CREATED
        pass

    def Handle(self):
        self.state = HandlerState.PROCESSING
        pass

    def StopHandle(self, isSuccessful):
        if isSuccessful:
            self.state = HandlerState.SUCCEEDED
        else:
            self.state = HandlerState.FAILED

    def State(self):
        return self.state

    