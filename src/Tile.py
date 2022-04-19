

import math
from . import Utils
import pygame


def mismoId(list, tileB):
    tileReturn = Tile(-1,0,0,0,0,0,0)
    #print("AAAAAAAAAAAAAAAAAAAAAAA")
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
        
    
    def getRect(self):
        return (int(self.centerx - self.w/2) ,int(self.centery - self.h/2), self.w, self.h)
        
    def heur(self,  tfin):
    #print(math.sqrt(int((tfin.centerx - self.centerx))/40*int((tfin.centerx - self.centerx)/40) + int((tfin.centery - self.centery))/40*int((tfin.centery - self.centery)/40)))
        return math.sqrt(int(((tfin.centerx - self.centerx)/40))**2 + int((tfin.centery - self.centery)/40)**2)
    
    def draw(self, screen, camera):
        screen.blit(self.image, [self.x - camera.x, self.y - camera.y])