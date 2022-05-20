import pygame as pg

from .Entity import *
from ..Utils import *
from .Worker import *
from ..Lib import *
from ..Music import *

# Constantes
HP = 60
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 6
ATTACK_INFO[COOLDOWN_IND] = 5
ATTACK_INFO[RANGE_IND] = 1 * RANGE_UNIT + RANGE_BASIC
MINE_POWER = 10
MINERAL_COST = 20
GAS_COST = 0
TIME_TO_MINE = 11000
GENERATION_TIME = 20
SPEED = 5
FRAMES_TO_REFRESH = 2
FACES = 8
FRAME = 0
#Esto es mentira, salen 220 frames no 296

# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-flist(range(289, 296))rame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
WEIGHT_PADDING =    60
HEIGHT_PADDING =    60
X_PADDING =         25
Y_PADDING =         30
PADDING = 110

IS_EXPLOSIVE = True

class TerranWorker(Worker):
    
    generateSound = workerGenerateSound
    deadSound = workerDeadSound
    attackSound = workerAttackSound
    
    def __init__(self, player, xIni = -1, yIni = -1):
        Worker.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST,
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, FACES, FRAME,
                PADDING,  takeID(), player, MINE_POWER, TIME_TO_MINE,None,
                TERRAN_WORKER_FRAMES, DIR_OFFSET, TERRAN_WORKER_ATTACK_FRAMES, TERRAN_WORKER_STILL_FRAMES, TERRAN_WORKER_MOVE_FRAMES, TERRAN_WORKER_DIE_FRAMES, X_PADDING,
                Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, TERRAN_WORKER_ORE_TRANSPORTING_FRAMES,
                TERRAN_WORKER_GAS_TRANSPORTING_FRAMES, ATTACK_INFO, IS_EXPLOSIVE)
        #print(self.speed)
        
        sprites = Utils.TERRAN_WORKER_SPRITES
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
        self.render = pg.transform.scale(pg.image.load(TERRAN_WORKER_RENDER), UNIT_RENDER_SIZE)

        self.type = WORKER
    

    def toDictionary(self, map):
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "terranWorker",
            "nombre": "SCV",
            "funcion": "Unidad obrera"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
