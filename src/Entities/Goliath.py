import pygame as pg


from .. import Command

from .Entity import *
from ..Utils import *
from .Soldier import *
from ..Music import *

# Constantes
HP = 300
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 50
ATTACK_INFO[COOLDOWN_IND] = 45
ATTACK_INFO[RANGE_IND] = 1 * RANGE_UNIT + RANGE_BASIC
MINE_POWER = 0
MINERAL_COST = 100
GAS_COST = 40
TIME_TO_MINE = 1000
GENERATION_TIME = 40
SPEED = 2.5
FRAMES_TO_REFRESH = 3
FACES = 8
FRAME = 0
WEIGHT_PADDING =    100
HEIGHT_PADDING =    50
X_PADDING =         25
Y_PADDING =         30
PADDING = 20

IS_EXPLOSIVE = True

class Goliath(Soldier):
    generateSound = soldierGenerateSound
    deadSound = workerDeadSound
    attackSound = goliathAttackSound
    
    def __init__(self, player, xIni = -1, yIni = -1):
        Soldier.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST,
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, FACES, FRAME,
                PADDING,  takeID(), player, GOLIATH_INVERSIBLE_FRAMES, GOLIATH_FRAMES, 
                DIR_OFFSET, GOLIATH_ATTACK_FRAMES, GOLIATH_STILL_FRAMES, GOLIATH_MOVE_FRAMES, 
                GOLIATH_DIE_FRAMES, X_PADDING, Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ATTACK_INFO, IS_EXPLOSIVE)

        sprites = Utils.GOLIATH_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]

        self.dir = 8
        self.changeToStill()
        if xIni != -1:
            self.updateOwnSpace()
        #self.imageRect = rect(self.x, self.y, self.image.get_width() - WEIGHT_PADDING,
                #self.image.get_height() - HEIGHT_PADDING)
        #self.imageRect = rect(self.x - self.image.get_width()/2, self.y -self.image.get_height() , self.image.get_width(), self.image.get_height())
        #self.imageRect = rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.render = pg.transform.scale(pg.image.load(TERRAN_T3_RENDER), UNIT_RENDER_SIZE)
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
