from enum import Enum

class WorkStatus(str, Enum):
    PENDING = "pending"
    MANAGING= "managing"
    PLANNING = "planning"
    REVIEWING = "reviewing"
    WRITING = "writing"
    FINALIZING = "finalizing"
    DONE = "done"
    FAILED = "failed"
