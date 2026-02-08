from enum import Enum


class WorkStatus(str, Enum):
    PENDING = "pending"
    MANAGING = "managing"
    DESIGNING = "designing"
    REVIEWING = "reviewing"
    WRITING = "writing"
    FINALIZING = "finalizing"
    DONE = "done"
    FAILED = "failed"
    INITIALIZING = "initializing"
