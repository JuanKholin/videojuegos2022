

import math
from . import Utils
import pygame


def mismoId(list, tileB):
    tileReturn = Tile(-1,0,0,0,0,0,0)
    for tile in list:
        #print("COmparo", tile.tileid, tileB.tileid)
        if tile.tileid == tileB.tileid:
            tileReturn = tile
    return tileReturn

class Tile():
    def __init__(self, tileid, x, y, h, w, image, type, g = 0, padre = None):
        self.x = x
        self.y = y
        self.centerx = int(x + w/2)
        self.centery = int(y + h/2)
        self.h = h
        self.w = w
        self.type = type 
        self.id = 0
        self.g = g
        self.tileid = tileid
        self.padre = padre
        self.image = image
        self.ocupante = None

    def setOcupante(self, ocupante):
        self.ocupante = ocupante
        
    def setOcupada(self, id):
        self.type = Utils.UNIT
        self.id = id
        
    def getRect(self):
        return (int(self.centerx - self.w/2) ,int(self.centery - self.h/2), self.w, self.h)
        
    def heur(self,  tfin):
    #print(math.sqrt(int((tfin.centerx - self.centerx))/40*int((tfin.centerx - self.centerx)/40) + int((tfin.centery - self.centery))/40*int((tfin.centery - self.centery)/40)))
        return math.sqrt(int(((tfin.centerx - self.centerx)/40))**2 + int((tfin.centery - self.centery)/40)**2)
    
    def draw(self, screen, camera):
        if not Utils.DEBBUG:
            screen.blit(self.image, [self.x - camera.x, self.y - camera.y])
        else:
            globalRectCoords = self.getRect()
            cameraRectCoords = (globalRectCoords[0] - camera.x, globalRectCoords[1] - camera.y, globalRectCoords[2], globalRectCoords[3])
            if self.type == 1:
                pygame.draw.rect(screen, Utils.RED, pygame.Rect(cameraRectCoords), 1)
            elif self.type == 0:
                pygame.draw.rect(screen, Utils.GREEN, pygame.Rect(cameraRectCoords), 1)
            elif self.type == 3:
                pygame.draw.rect(screen, Utils.BLUE, pygame.Rect(cameraRectCoords), 1)
            else:
                pygame.draw.rect(screen, Utils.PURPLE, pygame.Rect(cameraRectCoords), 1)