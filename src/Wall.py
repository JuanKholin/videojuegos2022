import pygame as pg

from .Utils import *


# Constantes
HP = 60
MINE_POWER = 8
MINERAL_COST = 50
TIME_TO_MINE = 2000
GENERATION_TIME = 2
speed = 2
FRAMES_TO_REFRESH = 10
SPRITES = "wall.png"
SCALE = 1.5
SPRITE_PIXEL_ROWS = 72
FACES = 8
FRAME = 0
#Esto es mentira, salen 220 frames no 296
TOTAL_FRAMES = 296  # [0:15] MOVERSE Y STILL
                    # [16:31] MOVER ORE
                    # [32:47] MOVER BARRIL
                    # [48:217] ATACAR Y MINAR
                    # [289:295] MORICION
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(205, 221)), [221] * 16, [222] * 16, [223] * 16, [224] * 16,
          [225] * 16, [226] * 16, [227] * 16, [228] * 16, [229] * 16, [230] * 16]
STILL_FRAMES = [0]
ORE_TRANSPORTING_FRAMES = [3]
BARREL_TRANSPORTING_FRAMES = [2]
ATTACK_FRAMES = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
MOVE_FRAMES = [0]
DIE_FRAMES = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

INVERSIBLE_FRAMES = len(FRAMES) - len(DIE_FRAMES) # los die frames no se invierten
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-flist(range(289, 296))rame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
WEIGHT_PADDING =    60
HEIGHT_PADDING =    60
X_PADDING =         25
Y_PADDING =         30
PADDING = 110

class Wall():
    
    
    def __init__(self, type , xIni, yIni, mapa):
        #print(self.speed)
        if type == 1:
            spritesheet = pg.image.load("./sprites/Muro/wallTerran.png").convert()
        else:
            spritesheet = pg.image.load("./sprites/Muro/wallZerg.png").convert()
        self.type = type
        spritesheet.set_colorkey(BLACK)
        self.image = pg.transform.scale(spritesheet, [spritesheet.get_rect().w * 1.4, spritesheet.get_rect().h * 1.1])
        self.x = xIni 
        self.y = yIni
        self.mapa = mapa
        self.xPadding = 21
        self.yPadding = 0
        self.wPadding = 60
        self.hPadding = 60
        drawPos = self.getPos()
        r = self.getRect()
        self.tile = self.mapa.getTile(drawPos[0] + r.w/2, drawPos[1])

        self.mapa.setObstacle(self.tile)
        self.tile = self.mapa.getTile(drawPos[0] - r.w/2, drawPos[1])

        self.mapa.setObstacle(self.tile)

        

    def draw(self, screen, camera):
        r = self.getRect()

        if DEBBUG:
            pg.draw.rect(screen, BLACK, pg.Rect(r.x - camera.x, r.y  - camera.y, r.w, r.h), 1)
        if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
            r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
            drawPos = self.getDrawPosition()
            #screen.blit(unit.image, [r.x - camera.x, r.y - camera.y])
            screen.blit(self.image, [drawPos[0] - camera.x, drawPos[1] - camera.y])
    
    def getRect(self):
        rectAux = pg.Rect(self.x - self.xPadding, self.y - self.yPadding,
                self.image.get_width() - self.wPadding, self.image.get_height()  - self.hPadding)
        return rectAux

    def getDrawPosition(self):
        return (self.x - self.image.get_width()/2,  self.y - self.image.get_height()/2)

    def getPos(self):
        r = self.getRect()
        return (r.x + r.w/2, r.y + r.h)

    def toDictionary(self):
        sonDictionary = {
            "clase": "Muro",
            "xIni": self.x,
            "yIni": self.y,
            "type": self.type
        }
        return sonDictionary
