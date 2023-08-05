from enum import Enum


class ListFlowsResponse200ItemValueFailureModuleValueType(str, Enum):
    SCRIPT = "script"
    FLOW = "flow"

    def __str__(self) -> str:
        return str(self.value)
