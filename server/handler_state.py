from enum import Enum

class HandlerState(Enum):
    SUCCEEDED = 1,
    FAILED = -1

if __name__ == "__main__":
    a = HandlerState.SUCCEEDED
    print(a)