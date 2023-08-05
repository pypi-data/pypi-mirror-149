from enum import Enum


class GetFlowByPathResponse200ValueFailureModuleValueType(str, Enum):
    SCRIPT = "script"
    FLOW = "flow"

    def __str__(self) -> str:
        return str(self.value)
