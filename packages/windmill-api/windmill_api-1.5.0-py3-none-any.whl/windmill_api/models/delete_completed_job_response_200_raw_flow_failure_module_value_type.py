from enum import Enum


class DeleteCompletedJobResponse200RawFlowFailureModuleValueType(str, Enum):
    SCRIPT = "script"
    FLOW = "flow"

    def __str__(self) -> str:
        return str(self.value)
