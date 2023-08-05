from enum import Enum


class WorkflowExecutionStatus(str, Enum):
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    TERMINATED_AFTER_TIME_OUT = "TERMINATED_AFTER_TIME_OUT"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    MANUALLY_STARTED = "MANUALLY_STARTED"

    def __str__(self) -> str:
        return str(self.value)
