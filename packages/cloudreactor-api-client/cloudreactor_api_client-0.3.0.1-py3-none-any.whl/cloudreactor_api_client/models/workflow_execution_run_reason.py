from enum import Enum


class WorkflowExecutionRunReason(str, Enum):
    EXPLICIT_START = "EXPLICIT_START"
    SCHEDULED_START = "SCHEDULED_START"
    EXPLICIT_RETRY = "EXPLICIT_RETRY"

    def __str__(self) -> str:
        return str(self.value)
