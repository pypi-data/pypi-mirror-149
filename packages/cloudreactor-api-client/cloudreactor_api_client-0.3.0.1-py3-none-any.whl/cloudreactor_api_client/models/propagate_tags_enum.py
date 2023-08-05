from enum import Enum


class PropagateTagsEnum(str, Enum):
    TASK_DEFINITION = "TASK_DEFINITION"
    SERVICE = "SERVICE"

    def __str__(self) -> str:
        return str(self.value)
