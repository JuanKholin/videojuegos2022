import pygame as pg
from ..Utils import *
from .Resource import *

SPRITE_PIXEL_ROWS = 96
WEIGHT_PADDING =    0
HEIGHT_PADDING =    85
X_PADDING =         65
Y_PADDING =         55

class Crystal(Resource):
    def __init__(self, x, y, capacidad):
        Resource.__init__(self, x * TILE_WIDTH, y * TILE_HEIGHT + 20, CRYSTAL, capacidad)
        spritesheet = pg.image.load("./SPRITE/Cristal/min0" + str(self.type) + ".bmp").convert()
        spritesheet.set_colorkey((BLACK))
        self.sprites = self.divideSpritesheetByRows(spritesheet, SPRITE_PIXEL_ROWS)
        #self.image = self.sprites[4 - int(float(capacidad)/float(self.interval) + 0.5)]
        self.image = self.sprites[0]
        self.clicked = False
        
        self.render = pygame.transform.scale(pygame.image.load(CRYSTAL_RENDER), RENDER_SIZE)

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

    # Devuelve el rectangulo que conforma su imagen, creo, esto lo hizo otro
    def getRect(self):
        rectAux = pg.Rect(self.x - X_PADDING,
                self.y - Y_PADDING, self.image.get_width() - WEIGHT_PADDING, self.image.get_height()  - HEIGHT_PADDING)
        return rectAux
    
    def getType(self):
        return RESOURCE

    def toDictionary(self, map):
        print("x e y del cristal ", self.x, self.y)
        x, y = map.getTileIndex(self.x, self.y)
        print("x e y de la tile del cristal ", x, y)
        return {
            "clase": "cristal",
            "capacidad": self.capacity,
            "tipo": self.tipo,
            "x": self.x,
            "y": self.y,
        }