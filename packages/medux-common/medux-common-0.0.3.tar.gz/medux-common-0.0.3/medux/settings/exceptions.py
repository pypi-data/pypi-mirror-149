class SettingDoesNotExist(LookupError):
    def __init__(self, name: str):
        self.message = f"setting '{name}' does not exist."

    def __str__(self) -> str:
        return self.message
