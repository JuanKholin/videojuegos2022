import pygame as pg
from .. import Utils

SPRITE_PIXEL_ROWS = 96
WEIGHT_PADDING =    0
HEIGHT_PADDING =    85
X_PADDING =         65
Y_PADDING =         55

class Cristal():
    def __init__(self, capacidad, tipo, x, y):
        self.x = x
        self.y = y
        self.capacidad = capacidad
        self.tipo = tipo
        self.interval = capacidad/4
        spritesheet = pg.image.load("./SPRITE/Cristal/min0" + str(tipo) + ".bmp").convert()
        spritesheet.set_colorkey((Utils.BLACK))
        self.sprites = self.divideSpritesheetByRows(spritesheet, SPRITE_PIXEL_ROWS)
        #self.image = self.sprites[4 - int(float(capacidad)/float(self.interval) + 0.5)]
        self.image = self.sprites[0]
        self.clicked = False
    
    def divideSpritesheetByRows(self,spritesheet, rows):
        totalRows = spritesheet.get_height()
        maxCol = spritesheet.get_width()
        sprites = []
        for i in range(int(totalRows / rows)):
            aux = pg.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows))
            aux = pg.transform.scale2x(aux)
            
            sprites.append(aux)
        return sprites
    def __del__(self):
        print("destruction")

    def getMined(self, cantidad):
        self.capacidad -= cantidad
        print("Me han minado: ", self.capacidad)
        if(self.capacidad < 0):
            del self
        else:
            self.image = self.sprites[3 - int(float(self.capacidad)/float(self.interval))]

    def getPosition(self):
        r = self.getRect()
        return(r.x + r.w/2, r.y + r.h)
    def getDrawPosition(self):
        return(self.x - self.image.get_width()/2,  self.y - self.image.get_height()/2)
    # Devuelve el rectangulo que conforma su imagen, creo, esto lo hizo otro
    def getRect(self):
        rectAux = pg.Rect(self.x - X_PADDING, 
                self.y - Y_PADDING, self.image.get_width() - WEIGHT_PADDING, self.image.get_height()  - HEIGHT_PADDING)
        return rectAux