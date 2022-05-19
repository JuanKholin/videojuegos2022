import pygame as pg
from ..Utils import *
from .Resource import *
from random import randint

WEIGHT_PADDING =    0
HEIGHT_PADDING =    85
X_PADDING =         65
Y_PADDING =         55

class Crystal(Resource):
    def __init__(self, x, y, capacidad):
        Resource.__init__(self, x, y, CRYSTAL, capacidad)
        
        crystalType = randint(0,2) # Mete un cristal aleatorio de los 3 que tenemos
        sprites = Utils.CRYSTAL_SPRITES
        self.sprites = sprites[crystalType]
        self.shadows = sprites[crystalType + 3]
        self.image = self.sprites[0]
        self.shadow = self.shadows[0]

        self.clicked = False

        self.render = pg.transform.scale(pg.image.load(CRYSTAL_RENDER), RENDER_SIZE)

    def divideSpritesheetByRows(self,spritesheet, rows):
        totalRows = spritesheet.get_height()
        maxCol = spritesheet.get_width()
        sprites = []
        for i in range(int(totalRows / rows)):
            aux = pg.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows))
            #aux = pg.transform.scale2x(aux)
            aux = pg.transform.scale(aux, [aux.get_rect().w * 2.2, aux.get_rect().h * 2])
            sprites.append(aux)
        return sprites

    def __del__(self):
        #print("destruction")
        pass

    # Devuelve el rectangulo que conforma su imagen, creo, esto lo hizo otro
    def getRect(self):
        rectAux = pg.Rect(self.x - X_PADDING,
                self.y - Y_PADDING, self.image.get_width() - WEIGHT_PADDING, self.image.get_height()  - HEIGHT_PADDING)
        return rectAux

    def getType(self):
        return RESOURCE

    def toDictionary(self):
        return {
            "clase": "cristal",
            "capacidad": self.capacity,
            "x": self.xTile,
            "y": self.yTile,
            "nombre": "Cristal",
            "funcion": "Esencial para todo"
        }
