from .Utils import *

class Camera():
    def __init__(self, x, y, h, w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w

    def setCamera(self, x, y, h, w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w

    def moverArriba(self):
        if self.y > 0:
            self.y = self.y - CAMERA_SPEED

    def moverAbajo(self, mapHeight):
        if (self.y + self.h) + CAMERA_SPEED <= mapHeight + 176:
            self.y = self.y + CAMERA_SPEED

    def moverIzquierda(self):
        if self.x > 0:
            self.x = self.x - CAMERA_SPEED

    def moverDerecha(self, mapWidth):
        if (self.x + self.w) < mapWidth-CAMERA_SPEED:
            self.x = self.x + CAMERA_SPEED
        
    def setX(self, x, mapWidth):
        if x + self.w > mapWidth:
            self.x = mapWidth-self.w
        elif x < 0:
            self.x = 0
        else:
            self.x = x
            
    def setY(self, y, mapHeight):
        if y + self.h > mapHeight:
            self.y = mapHeight-self.h
        elif y < 0:
            self.y = 0
        else:
            self.y = y

    def toDictionary(self):
        return {
            "x": self.x,
            "y": self.y,
            "h": self.h,
            "w": self.w,
        }
