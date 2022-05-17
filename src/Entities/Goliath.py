import pygame as pg


from .. import Command

from .Entity import *
from ..Utils import *
from .Soldier import *
from ..Music import *

# Constantes
HP = 250
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 40
ATTACK_INFO[COOLDOWN_IND] = 5
ATTACK_INFO[RANGE_IND] = 1 * RANGE_UNIT + RANGE_BASIC
MINE_POWER = 0
MINERAL_COST = 100
GAS_COST = 100
TIME_TO_MINE = 1000
GENERATION_TIME = 50
SPEED = 1.5
FRAMES_TO_REFRESH = 4
SPRITES = "goliath.bmp"
DEATH_SPRITES = "explosion2.bmp"
SPRITE_PIXEL_ROWS = 76
FACES = 8
FRAME = 0
SCALE = 2
TOTAL_FRAMES = 179
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), [170] * 16, [171] * 16, [172] * 16, [173] * 16,
          [174] * 16, [175] * 16, [176] * 16, [177] * 16, [178] * 16]
STILL_FRAMES = [0]
ATTACK_FRAMES = [5, 6, 8, 9]
MOVE_FRAMES = [0, 1, 2, 4, 5, 6, 7]
DIE_FRAMES = [10, 11, 12, 13, 14, 15, 16, 17, 18]

INVERSIBLE_FRAMES = len(FRAMES) - len(DIE_FRAMES) # los die frames no se invierten
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-flist(range(289, 296))rame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
WEIGHT_PADDING =    100
HEIGHT_PADDING =    100
X_PADDING =         15
Y_PADDING =         15
PADDING = 20

class Goliath(Soldier):
    generateSound = soldierGenerateSound
    deadSound = soldierDeadSound
    attackSound = soldierAttackSound 
    
    def __init__(self, player, xIni = -1, yIni = -1):
        Soldier.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST,
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME,
                PADDING,  takeID(), player, INVERSIBLE_FRAMES, FRAMES, DIR_OFFSET, ATTACK_FRAMES,
                STILL_FRAMES, MOVE_FRAMES, DIE_FRAMES, X_PADDING,
                Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ATTACK_INFO)

        spritesheet = pg.image.load("./sprites/" + self.spritesName).convert()
        spritesheet.set_colorkey(BLACK)
        deadSpritesheet = pg.image.load("./sprites/" + DEATH_SPRITES).convert()
        deadSpritesheet.set_colorkey(BLACK)
        self.sprites = Entity.divideSpritesheetByRows(spritesheet,
                SPRITE_PIXEL_ROWS, SCALE) + Entity.divideSpritesheetByRows(deadSpritesheet, 128, SCALE)
        self.mirrorTheChosen()
        self.dir = 8
        self.changeToStill()
        if xIni != -1:
            self.updateOwnSpace()
        #self.imageRect = rect(self.x, self.y, self.image.get_width() - WEIGHT_PADDING,
                #self.image.get_height() - HEIGHT_PADDING)
        #self.imageRect = rect(self.x - self.image.get_width()/2, self.y -self.image.get_height() , self.image.get_width(), self.image.get_height())
        #self.imageRect = rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.render = pygame.transform.scale(pygame.image.load(TERRAN_T3_RENDER), UNIT_RENDER_SIZE)
        self.type = SOLDIER
    

    def toDictionary(self, map):
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "goliath",
            "nombre": "Goliath",
            "funcion": "Unidad Colosal Terran"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
