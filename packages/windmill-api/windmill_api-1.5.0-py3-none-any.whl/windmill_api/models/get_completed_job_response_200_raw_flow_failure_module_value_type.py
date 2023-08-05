from enum import Enum


class GetCompletedJobResponse200RawFlowFailureModuleValueType(str, Enum):
    SCRIPT = "script"
    FLOW = "flow"

    def __str__(self) -> str:
        return str(self.value)
