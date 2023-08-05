from enum import Enum


class QueuedJobRawFlowModulesItemValueType(str, Enum):
    SCRIPT = "script"
    FLOW = "flow"

    def __str__(self) -> str:
        return str(self.value)
