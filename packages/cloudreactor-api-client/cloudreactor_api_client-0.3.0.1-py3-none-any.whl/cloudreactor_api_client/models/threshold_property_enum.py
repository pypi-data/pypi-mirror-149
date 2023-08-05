from enum import Enum


class ThresholdPropertyEnum(str, Enum):
    EXECUTION_TIME = "execution_time"
    SUCCESS_RATIO = "success_ratio"
    FAILURE_RATIO = "failure_ratio"
    SKIPPED_RATIO = "skipped_ratio"

    def __str__(self) -> str:
        return str(self.value)
