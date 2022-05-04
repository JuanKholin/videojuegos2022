from ..Utils import *

class Resource():
    def __init__(self, x, y, resourceType, capacity):
        self.x = x
        self.y = y
        self.capacity = capacity
        self.type = resourceType
        self.interval = capacity / 4
        self.enable = True
        
    def disable(self):
        self.enable = False