from handler_state import HandlerState
import uuid
import traceback

class InfoHandler():
    def __init__(self):
        pass

    def Execute(self, reqCode:str, data:str):
        try:
            if data=="MACADDRESS":
                mac = '{:0>2X}'.format(uuid.getnode())
                chunks = [mac[i:i+2] for i in range(0, len(mac), 2)]
                mac = ':'.join(chunks)
                return HandlerState.SUCCEEDED, mac.encode("utf-8")
            else:
                return HandlerState.INVALID, None

        except Exception as e:
            traceback.print_exc()
            return HandlerState.FAILED, None