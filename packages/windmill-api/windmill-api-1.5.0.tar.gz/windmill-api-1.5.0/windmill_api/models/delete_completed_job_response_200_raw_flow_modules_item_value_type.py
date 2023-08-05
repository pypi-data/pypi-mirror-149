from enum import Enum


class DeleteCompletedJobResponse200RawFlowModulesItemValueType(str, Enum):
    SCRIPT = "script"
    FLOW = "flow"

    def __str__(self) -> str:
        return str(self.value)
