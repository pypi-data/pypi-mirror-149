from enum import Enum


class StartTransitionConditionEnum(str, Enum):
    ALL = "all"
    ANY = "any"
    COUNT_AT_LEAST = "count_at_least"
    RATIO_AT_LEAST = "ratio_at_least"

    def __str__(self) -> str:
        return str(self.value)
