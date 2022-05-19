import pygame as pg


from .. import Command

from .Entity import *
from ..Utils import *
from .Soldier import *
from ..Music import *

# Constantes
HP = 40
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 6
ATTACK_INFO[COOLDOWN_IND] = 12
ATTACK_INFO[RANGE_IND] = 4 * RANGE_UNIT + RANGE_BASIC
MINE_POWER = 0
MINERAL_COST = 20
GAS_COST = 0
TIME_TO_MINE = 1000
GENERATION_TIME = 20
SPEED = 2
FRAMES_TO_REFRESH = 4
FACES = 8
FRAME = 0

WEIGHT_PADDING =    65
HEIGHT_PADDING =    65
X_PADDING =         15
Y_PADDING =         15
PADDING = 110

IS_EXPLOSIVE = False

class TerranSoldier(Soldier):
    
    generateSound = soldierGenerateSound
    deadSound = soldierDeadSound
    attackSound = soldierAttackSound 
    
    def __init__(self, player, xIni = -1, yIni = -1):
        Soldier.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST,
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, FACES, FRAME,
                PADDING,  takeID(), player, TERRAN_SOLDIER_INVERSIBLE_FRAMES, TERRAN_SOLDIER_FRAMES, DIR_OFFSET, TERRAN_SOLDIER_ATTACK_FRAMES,
                TERRAN_SOLDIER_STILL_FRAMES, TERRAN_SOLDIER_MOVE_FRAMES, TERRAN_SOLDIER_DIE_FRAMES, X_PADDING,
                Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ATTACK_INFO, IS_EXPLOSIVE)

        
        sprites = Utils.TERRAN_SOLDIER_SPRITES
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
        self.render = pg.transform.scale(pg.image.load(TERRAN_T1_RENDER), UNIT_RENDER_SIZE)
        self.type = SOLDIER
    
    

    

    def toDictionary(self, map):
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "terranSoldier",
            "nombre": "Terran Marine",
            "funcion": "Unidad ofensiva a rango"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
