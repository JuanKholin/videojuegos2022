import pygame as pg
from ..Utils import *
from .Resource import *

WEIGHT_PADDING =    40
HEIGHT_PADDING =    20
X_PADDING =         80
Y_PADDING =         20

class Geyser(Resource):
    def __init__(self, x, y, capacidad):
        Resource.__init__(self, x, y, CRYSTAL, capacidad)

        sprites = Utils.GEYSER_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]

        self.image = self.sprites[0]
        self.shadow = self.shadows[0]
        self.clicked = False

        self.render = pg.transform.scale(pg.image.load(GEYSER_RENDER), RENDER_SIZE)

    def draw(self, screen, camera):
        if self.enable:
            Resource.draw(self, screen, camera)

    def divideSpritesheetByRows(self,spritesheet, rows, scale = 1.5):
        totalRows = spritesheet.get_height()
        maxCol = spritesheet.get_width()
        sprites = []
        for i in range(int(totalRows / rows)):
            aux = pg.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows))
            aux = pg.transform.scale(aux, [aux.get_rect().w * scale, aux.get_rect().h * scale])

            sprites.append(aux)
        return sprites

    def __del__(self):
        #print("destruction")
        pass

    def getMined(self, cantidad):
        if (self.capacity <= 0):
            return 2
        self.capacity -= cantidad
        #print("Me han minado: ", self.capacity)
        if (self.capacity <= 0):
            return cantidad + self.capacity
        else:
            self.image = self.sprites[3 - int(float(self.capacity)/float(self.interval))]
            return cantidad

    # Devuelve el rectangulo que conforma su imagen, creo, esto lo hizo otro
    def getRect(self):
        rectAux = pg.Rect(self.x - X_PADDING + 10,
                self.y - Y_PADDING + 5, self.image.get_width() - WEIGHT_PADDING + 10, self.image.get_height()  - HEIGHT_PADDING)
        return rectAux

    def getDrawPosition(self):
        return(self.x - self.image.get_width()/2 + 10,  self.y - self.image.get_height()/2)

    def getType(self):
        return GEYSER

    def toDictionary(self):
        return {
            "clase": "geyser",
            "capacidad": self.capacity,
            "x": self.xTile,
            "y": self.yTile,
            "nombre": "Geyser",
            "funcion": "Recurso para construccion"
        }
