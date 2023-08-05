from enum import Enum


class AwsEcsLaunchType(str, Enum):
    FARGATE = "FARGATE"
    EC2 = "EC2"

    def __str__(self) -> str:
        return str(self.value)
