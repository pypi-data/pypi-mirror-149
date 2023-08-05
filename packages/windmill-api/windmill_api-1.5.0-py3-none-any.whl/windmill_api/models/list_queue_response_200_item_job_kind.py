from enum import Enum


class ListQueueResponse200ItemJobKind(str, Enum):
    SCRIPT = "script"
    PREVIEW = "preview"
    DEPENDENCIES = "dependencies"
    FLOW = "flow"
    FLOWPREVIEW = "flowpreview"

    def __str__(self) -> str:
        return str(self.value)
