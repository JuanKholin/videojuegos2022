
class Camera():
    def __init__(self, x, y, h, w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        
    def moverArriba(self):
        if self.y > 0:
            self.y = self.y - 4
    def moverAbajo(self, mapHeight):
        if (self.y + self.h) < mapHeight:
            self.y = self.y + 4
    def moverIzquierda(self):
        if self.x > 0:
            self.x = self.x - 4
    def moverDerecha(self, mapWidth):
        if (self.x + self.w) < mapWidth:
            self.x = self.x + 4