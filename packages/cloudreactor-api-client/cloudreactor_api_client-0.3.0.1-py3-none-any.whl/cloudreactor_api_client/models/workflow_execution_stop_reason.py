from enum import Enum


class WorkflowExecutionStopReason(str, Enum):
    MANUAL = "MANUAL"
    MAX_EXECUTION_TIME_EXCEEDED = "MAX_EXECUTION_TIME_EXCEEDED"

    def __str__(self) -> str:
        return str(self.value)
