from enum import Enum


class ListCompletedJobsResponse200ItemRawFlowFailureModuleValueType(str, Enum):
    SCRIPT = "script"
    FLOW = "flow"

    def __str__(self) -> str:
        return str(self.value)
