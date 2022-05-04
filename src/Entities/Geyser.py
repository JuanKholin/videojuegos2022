import pygame as pg
from ..Utils import *
from .Resource import *

SPRITE_PIXEL_ROWS = 64
WEIGHT_PADDING =    40
HEIGHT_PADDING =    20
X_PADDING =         80
Y_PADDING =         20

class Geyser(Resource):
    def __init__(self, x, y, capacidad):
        Resource.__init__(self, x * TILE_WIDTH, y * TILE_HEIGHT + 20, CRYSTAL, capacidad)
        spritesheet = pg.image.load("./sprites/geyser.bmp").convert()
        spritesheet.set_colorkey((BLACK))
        self.sprites = self.divideSpritesheetByRows(spritesheet, SPRITE_PIXEL_ROWS)
        #self.image = self.sprites[4 - int(float(capacidad)/float(self.interval) + 0.5)]
        self.image = self.sprites[0]
        self.clicked = False
        
        self.render = pygame.transform.scale(pygame.image.load(CRYSTAL_RENDER), RENDER_SIZE)
        
    def draw(self, screen, camera):
        if self.enable:
            r = self.getRect()
            pg.draw.rect(screen, BLACK, pg.Rect(r.x - camera.x, r.y  - camera.y, r.w, r.h),1)
            if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
            r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
                drawPos = self.getDrawPosition()
                if self.clicked:
                    pg.draw.ellipse(screen, YELLOW, [r.x - camera.x, r.y + (0.7*r.h)- camera.y,r.w , 0.3*r.h], 2)
                #screen.blit(unit.image, [r.x - self.camera.x, r.y - self.camera.y])
                screen.blit(self.image, [drawPos[0] - camera.x, drawPos[1] - camera.y])

    def divideSpritesheetByRows(self,spritesheet, rows):
        totalRows = spritesheet.get_height()
        maxCol = spritesheet.get_width()
        sprites = []
        for i in range(int(totalRows / rows)):
            aux = pg.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows))
            aux = pg.transform.scale(aux, [aux.get_rect().w * 1.5, aux.get_rect().h * 1.5])

            sprites.append(aux)
        return sprites

    def __del__(self):
        print("destruction")
        
    def setClicked(self, click):
        self.clicked = click

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

    def getPosition(self):
        r = self.getRect()
        return (r.x + r.w/2, r.y + r.h)

    def getDrawPosition(self):
        return(self.x - self.image.get_width()/2 + 20,  self.y - self.image.get_height()/2)

    # Devuelve el rectangulo que conforma su imagen, creo, esto lo hizo otro
    def getRect(self):
        rectAux = pg.Rect(self.x - X_PADDING,
                self.y - Y_PADDING, self.image.get_width() - WEIGHT_PADDING, self.image.get_height()  - HEIGHT_PADDING)
        return rectAux
    
    def getRender(self):
        return self.render
    
    def getType(self):
        return GEYSER

    def toDictionary(self, map):
        print("x e y del cristal ", self.x, self.y)
        x, y = map.getTileIndex(self.x, self.y)
        print("x e y de la tile del cristal ", x, y)
        return {
            "clase": "geyser",
            "capacidad": self.capacity,
            "tipo": self.tipo,
            "x": self.x,
            "y": self.y,
        }

    def getCenter(self):
        rect = self.getRect()
        return rect.x + rect.w/2, rect.y + rect.h/2

    def getCapacity(self):
        return self.capacity