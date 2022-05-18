import pygame as pg

from ..Utils import *
from .. import Utils

class Resource():
    def __init__(self, x, y, resourceType, capacity):
        self.x = x * TILE_WIDTH
        self.y = y * TILE_HEIGHT + 20
        self.xTile = x
        self.yTile = y
        self.capacity = capacity
        self.type = resourceType
        self.interval = capacity / 4
        self.enable = True
        self.id = takeID()
        self.shadow = []

    def disable(self):
        self.enable = False
        #print("Diableado", self.id)
        
    def setEnable(self):
        self.enable = True

    def setClicked(self, click):
        self.clicked = click

    def getCapacity(self):
        return self.capacity

    def draw(self, screen, camera):
        if self.enable:
            r = self.getRect()
            #pg.draw.rect(screen, BLACK, pg.Rect(r.x - camera.x, r.y  - camera.y, r.w, r.h),1)
            if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
            r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
                drawPos = self.getDrawPosition()
                if self.clicked:
                    pg.draw.ellipse(screen, YELLOW, [r.x - camera.x - 10, r.y - camera.y, r.w + 20, r.h], 2)
                #screen.blit(unit.image, [r.x - self.camera.x, r.y - self.camera.y])
                

                screen.blit(self.image, [drawPos[0] - camera.x, drawPos[1] - camera.y])

    def drawInfo(self, screen, color):
        dic = self.toDictionary()
        muestra_texto(screen, str('monotypecorsiva'), dic['nombre'], color, 25, [Utils.ScreenWidth/2 - GUI_INFO_X2 + 30, Utils.ScreenHeight - GUI_INFO_Y2 + 10])
        muestra_texto(screen, str('monotypecorsiva'), dic['funcion'], color, 20, [Utils.ScreenWidth/2 - GUI_INFO_X2 + 10, Utils.ScreenHeight - GUI_INFO_Y2 + 60])

    def getMined(self, cantidad):
        if (self.capacity <= 0):
            return 0
        self.capacity -= cantidad
        #print("Me han minado: ", self.capacity)
        if (self.capacity <= 0):
            return cantidad + self.capacity
        else:
            self.image = self.sprites[3 - int(float(self.capacity)/float(self.interval))]
            return cantidad

    def getPosition(self):
        r = self.getRect()
        return (r.x + r.w/2, r.y + r.h)

    def getCenter(self):
        rect = self.getRect()
        return rect.x + rect.w/2, rect.y + rect.h/2

    def getDrawPosition(self):
        return(self.x - self.image.get_width()/2,  self.y - self.image.get_height()/2)

    def getRender(self):
        return self.render

    def getType(self):
        return RESOURCE

    def getInfo(self):
        return "None"
