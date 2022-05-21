from .Utils import *
from . import Utils
import pygame as pg

CAMERA_X = 0
CAMERA_Y = 0
CAMERA_W = ScreenWidth
CAMERA_H = ScreenHeight

def rectInCamera(r):
    collideX = False
    collideY = False
    if (r.x >= CAMERA_X) and (r.x <= (CAMERA_X+CAMERA_W)):
        collideX = True
    elif (CAMERA_X >= r.x) and (CAMERA_X <= (r.x+r.w)):
        collideX = True
    if (r.y >= CAMERA_Y) and (r.y <= (CAMERA_Y+CAMERA_H)):
        collideY = True
    elif (CAMERA_Y >= r.y) and (CAMERA_Y <= (r.y+r.h)):
        collideY = True
    return collideX and collideY

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
        
    def update(self):
        global CAMERA_X, CAMERA_Y, CAMERA_W, CAMERA_H
        self.h = Utils.ScreenHeight
        self.w = Utils.ScreenWidth
        CAMERA_W = self.w
        CAMERA_H = self.h

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
        
    def setSize(self, w, h):
        global CAMERA_W, CAMERA_H
        self.h = h
        self.w = w
        CAMERA_W = w
        CAMERA_H = h

    def moverArriba(self):
        global CAMERA_Y
        if self.y - CAMERA_SPEED >= 0:
            self.y = self.y - CAMERA_SPEED
            CAMERA_Y = self.y

    def moverAbajo(self, mapHeight):
        global CAMERA_Y
        if (self.y + self.h) + CAMERA_SPEED <= mapHeight + 350:
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
