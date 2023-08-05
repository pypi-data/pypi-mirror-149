from enum import Enum


class QueuedJobJobKind(str, Enum):
    SCRIPT = "script"
    PREVIEW = "preview"
    DEPENDENCIES = "dependencies"
    FLOW = "flow"
    FLOWPREVIEW = "flowpreview"

    def __str__(self) -> str:
        return str(self.value)
