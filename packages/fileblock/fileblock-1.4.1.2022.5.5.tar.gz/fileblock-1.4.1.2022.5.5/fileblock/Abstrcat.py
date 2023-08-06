from .btype import __BaseType__

class Abstract:

    def __init__(self, type:__BaseType__, path:str) -> None:
        self.type = type
        self.path = path

    @property
    def __dict__(self):
        return {
            "type": str(self.type),
            "path": self.path
        }