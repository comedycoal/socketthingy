from enum import Enum

class HandlerState(Enum):
    INVALID = 0,
    SUCCEEDED = 1,
    FAILED = -1