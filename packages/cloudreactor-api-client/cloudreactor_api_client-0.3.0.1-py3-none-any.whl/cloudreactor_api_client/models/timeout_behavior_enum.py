from enum import Enum


class TimeoutBehaviorEnum(str, Enum):
    ALWAYS_FAIL_WORKFLOW = "always_fail_workflow"
    ALWAYS_TIMEOUT_WORKFLOW = "always_timeout_workflow"
    FAIL_WORKFLOW_IF_UNHANDLED = "fail_workflow_if_unhandled"
    TIMEOUT_WORKFLOW_IF_UNHANDLED = "timeout_workflow_if_unhandled"
    IGNORE = "ignore"

    def __str__(self) -> str:
        return str(self.value)
