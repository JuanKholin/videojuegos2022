WHITE   = (255,255,255)
BLACK   = (0,0,0)

class path():
    def __init__(self, angle, dist, posFin):
        self.angle = angle
        self.dist = dist
        self.posFin = posFin
class rect():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h