from enum import IntEnum

class CommandId(IntEnum):
    MOVER = 1


class Command:
    def __init__(self, id):
        self.id = id
        self.params = []


    def addParameter(self, par):
        self.params.append(par)
    def setId(self, id):
        self.id = id