from enum import Enum


class UpdateFlowJsonBodyValueFailureModuleValueType(str, Enum):
    SCRIPT = "script"
    FLOW = "flow"

    def __str__(self) -> str:
        return str(self.value)
