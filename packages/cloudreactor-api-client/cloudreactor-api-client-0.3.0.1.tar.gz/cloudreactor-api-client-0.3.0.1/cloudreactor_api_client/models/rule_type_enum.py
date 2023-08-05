from enum import Enum


class RuleTypeEnum(str, Enum):
    ALWAYS = "always"
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    EXIT_CODE = "exit_code"
    THRESHOLD = "threshold"
    CUSTOM = "custom"
    DEFAULT = "default"

    def __str__(self) -> str:
        return str(self.value)
