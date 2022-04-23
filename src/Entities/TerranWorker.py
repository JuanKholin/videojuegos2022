import pygame as pg

from .. import Command

from . import Entity
from .. import Utils
from .Worker import *

# Constantes
HP = 40
MINE_POWER = 8
MINERAL_COST = 20
TIME_TO_MINE = 1000
GENERATION_TIME = 2
SPEED = 4
FRAMES_TO_REFRESH = 10
SPRITES = "scvJusto.bmp"
SPRITE_PIXEL_ROWS = 72
FACES = 8
FRAME = 0
TOTAL_FRAMES = 296  # [0:15] MOVERSE Y STILL
                    # [16:31] MOVER ORE
                    # [32:47] MOVER BARRIL
                    # [48:217] ATACAR Y MINAR
                    # [289:295] MORICION
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)), 
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)), 
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)), 
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(205, 221)), list(range(289, 296))]
STILL_FRAMES = 0
ORE_TRANSPORTING_FRAMES = 3
BARREL_TRANSPORTING_FRAMES = 4
ATTACK_FRAMES = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
MOVE_FRAMES = [0]
DIE_FRAMES = 13
DIE_OFFSET = [0, 1, 2, 3, 4, 5, 6]

INVERSIBLE_FRAMES = len(FRAMES) - 1 # los die frames no se invierten
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-flist(range(289, 296))rame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
WEIGHT_PADDING =    64
HEIGHT_PADDING =    60
X_PADDING =         40
Y_PADDING =         47
PADDING = 110

class TerranWorker(Worker):
    def __init__(self, xIni, yIni, player):
        Worker.__init__(self, HP, xIni * 40 + 20, yIni * 40 + 20, MINERAL_COST, 
                                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME, 
                                    PADDING,  Utils.takeID(), player, MINE_POWER, TIME_TO_MINE, DIE_OFFSET, INVERSIBLE_FRAMES, 
                                        FRAMES, DIR_OFFSET, ATTACK_FRAMES, STILL_FRAMES, MOVE_FRAMES, DIE_FRAMES, X_PADDING,
                                            Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING)


        spritesheet = pg.image.load("./sprites/" + self.spritesName).convert()
        spritesheet.set_colorkey((Utils.BLACK))
        self.sprites = Entity.Entity.divideSpritesheetByRows(spritesheet, 
                SPRITE_PIXEL_ROWS)
        self.mirrorTheChosen()
        self.dir = 0
        self.changeToStill()
        #self.imageRect = Utils.rect(self.x, self.y, self.image.get_width() - WEIGHT_PADDING, 
                #self.image.get_height() - HEIGHT_PADDING)
        #self.imageRect = Utils.rect(self.x - self.image.get_width()/2, self.y -self.image.get_height() , self.image.get_width(), self.image.get_height())
        #self.imageRect = Utils.rect(self.x, self.y, self.image.get_width(), self.image.get_height())