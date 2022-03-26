
class Camera():
    def __init__(self, x, y, h, w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
    
    def move(self, x, y, h, w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w