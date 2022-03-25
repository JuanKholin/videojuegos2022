from enum import Enum, auto

class CommandId(Enum):
    MOVER = auto()

class Command:
    def __init__(self, id):
        self.id = id
        self.params = []


    def addParameter(self, par):
        self.params.append(par)