from enum import Enum


class GlobalWhoamiLoginType(str, Enum):
    PASSWORD = "password"
    GITHUB = "github"

    def __str__(self) -> str:
        return str(self.value)
