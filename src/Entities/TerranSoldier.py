import pygame as pg


from .. import Command

from .Entity import *
from ..Utils import *
from .Soldier import *

# Constantes
HP = 40
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 6
ATTACK_INFO[COOLDOWN_IND] = 7
ATTACK_INFO[RANGE_IND] = 4
MINE_POWER = 0
MINERAL_COST = 50
TIME_TO_MINE = 1000
GENERATION_TIME = 2
SPEED = 2
FRAMES_TO_REFRESH = 5
SPRITES = "terran_soldier_sheet.bmp"
SPRITE_PIXEL_ROWS = 64
FACES = 8
FRAME = 0
SCALE = 1.5
#Esto es mentira, salen 220 frames no 296
TOTAL_FRAMES = 13*17# 1     STILL
                    # 2     GUARDIA
                    # 3-4   ATACAR
                    # 5-13  MOVE
                    # 14    DIE
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(205, 221)), [221] * 16, [222] * 16, [223] * 16, [224] * 16,
          [225] * 16, [226] * 16, [227] * 16, [228] * 16]
STILL_FRAMES = [0]
GUARD_FRAMES = [1]
ATTACK_FRAMES = [2, 3]
MOVE_FRAMES = [4, 5, 6, 7, 8, 9, 10, 11, 12]
DIE_FRAMES = [13, 14, 15, 16, 17, 18, 19, 20]

INVERSIBLE_FRAMES = len(FRAMES) - len(DIE_FRAMES) # los die frames no se invierten
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-flist(range(289, 296))rame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
WEIGHT_PADDING =    65
HEIGHT_PADDING =    65
X_PADDING =         15
Y_PADDING =         15
PADDING = 110

class TerranSoldier(Soldier):
    def __init__(self, xIni, yIni, player):
        Soldier.__init__(self, HP, xIni * 40 + 20, yIni * 40 + 20, MINERAL_COST,
                                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME,
                                    PADDING,  takeID(), player, MINE_POWER, TIME_TO_MINE, INVERSIBLE_FRAMES,
                                        FRAMES, DIR_OFFSET, ATTACK_FRAMES, STILL_FRAMES, MOVE_FRAMES, DIE_FRAMES, X_PADDING,
                                            Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ATTACK_INFO)


        spritesheet = pg.image.load("./sprites/" + self.spritesName).convert()
        spritesheet.set_colorkey((WHITE))
        self.sprites = Entity.divideSpritesheetByRows(spritesheet,
                SPRITE_PIXEL_ROWS, SCALE)
        self.mirrorTheChosen()
        self.dir = 8
        self.changeToStill()
        #self.imageRect = rect(self.x, self.y, self.image.get_width() - WEIGHT_PADDING,
                #self.image.get_height() - HEIGHT_PADDING)
        #self.imageRect = rect(self.x - self.image.get_width()/2, self.y -self.image.get_height() , self.image.get_width(), self.image.get_height())
        #self.imageRect = rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.render = pygame.transform.scale(pygame.image.load(SOLDIER_RENDER), UNIT_RENDER_SIZE)

    def toDictionary(self, map):
        x, y = map.getTileIndex(self.x, self.y)
        return {
            "clase": "terranSoldier",
            "x": x,
            "y": y,
        }
