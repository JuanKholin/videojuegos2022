from .Utils import *

CAMERA_X = 0
CAMERA_Y = 0
CAMERA_W = SCREEN_WIDTH
CAMERA_H = SCREEN_HEIGHT

def inCamera(pos):
    if (pos[0] >= CAMERA_X and pos[0] <= CAMERA_X + CAMERA_W and
        pos[1] >= CAMERA_Y and pos[1] <= CAMERA_Y + CAMERA_H):
        return True
    else:
        return False

class Camera():
    def __init__(self, x, y, h, w):
        global CAMERA_X, CAMERA_Y, CAMERA_W, CAMERA_H
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        CAMERA_X = x
        CAMERA_Y = y
        CAMERA_W = w
        CAMERA_H = h

    def setCamera(self, x, y, h, w):
        global CAMERA_X, CAMERA_Y, CAMERA_W, CAMERA_H
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        CAMERA_X = x
        CAMERA_Y = y
        CAMERA_W = w
        CAMERA_H = h

    def moverArriba(self):
        global CAMERA_Y
        if self.y - CAMERA_SPEED >= 0:
            self.y = self.y - CAMERA_SPEED
            CAMERA_Y = self.y

    def moverAbajo(self, mapHeight):
        global CAMERA_Y
        if (self.y + self.h) + CAMERA_SPEED <= mapHeight + 170:
            self.y = self.y + CAMERA_SPEED
            CAMERA_Y = self.y

    def moverIzquierda(self):
        global CAMERA_X
        if self.x - CAMERA_SPEED >= 0:
            self.x = self.x - CAMERA_SPEED
            CAMERA_X = self.x

    def moverDerecha(self, mapWidth):
        global CAMERA_X
        if (self.x + self.w) < mapWidth - CAMERA_SPEED:
            self.x = self.x + CAMERA_SPEED
            CAMERA_X = self.x
        
    def setX(self, x, mapWidth):
        global CAMERA_X
        if x + self.w > mapWidth:
            self.x = mapWidth-self.w
        elif x < 0:
            self.x = 0
        else:
            self.x = x
        CAMERA_X = self.x
            
    def setY(self, y, mapHeight):
        global CAMERA_Y
        if y + self.h > mapHeight:
            self.y = mapHeight-self.h
        elif y < 0:
            self.y = 0
        else:
            self.y = y
        CAMERA_Y = self.y

    def toDictionary(self):
        return {
            "x": self.x,
            "y": self.y,
            "h": self.h,
            "w": self.w,
        }
    
    def setSelf(self, camera):
        global CAMERA_X, CAMERA_Y, CAMERA_W, CAMERA_H
        self.x = camera.x
        self.y = camera.y
        self.h = camera.h
        self.w = camera.w
        CAMERA_X = self.x
        CAMERA_Y = self.y
        CAMERA_W = self.w
        CAMERA_H = self.h
