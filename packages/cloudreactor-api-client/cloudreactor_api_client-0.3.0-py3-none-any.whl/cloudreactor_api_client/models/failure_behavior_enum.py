from enum import Enum


class FailureBehaviorEnum(str, Enum):
    ALWAYS_FAIL_WORKFLOW = "always_fail_workflow"
    FAIL_WORKFLOW_IF_UNHANDLED = "fail_workflow_if_unhandled"
    IGNORE = "ignore"

    def __str__(self) -> str:
        return str(self.value)
