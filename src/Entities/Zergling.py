import pygame as pg

from . import Entity, Worker
from ..Utils import *
from .Soldier import *

# Constantes del Zergling
HP = 60
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 5
ATTACK_INFO[COOLDOWN_IND] = 4
ATTACK_INFO[RANGE_IND] = 1 * RANGE_UNIT + RANGE_BASIC
MINE_POWER = 8
MINERAL_COST = 20
GAS_COST = 0
TIME_TO_MINE = 1000
GENERATION_TIME = 20
SPEED = 6
FRAMES_TO_REFRESH = 2
FACES = 8
FRAME = 0
PADDING = 110
WEIGHT_PADDING = 165
HEIGHT_PADDING = 155
X_PADDING = 13
Y_PADDING = 15

IS_EXPLOSIVE = True

class Zergling(Soldier):
    
    generateSound = zerglingGenerateSound
    deadSound = zerglingDeadSound
    attackSound = zerglingAttackSound
    selectedSound = zergSelectedSound
    # Pre: xIni e yIni marcan posiciones del mapa, (ej: (3, 2) se refiere a la posicion de
    # la cuarta columna y tercera fila del mapa)
    # Post: Crea un bichito mono que no hace practicamente nada pero tu dale tiempo
    def __init__(self, player, xIni = -1, yIni = -1):
        Soldier.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST,
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, FACES, FRAME, PADDING,
                takeID(), player, ZERGLING_INVERSIBLE_FRAMES,
                ZERGLING_FRAMES, DIR_OFFSET, ZERGLING_ATTACK_FRAMES, ZERGLING_STILL_FRAMES, 
                ZERGLING_MOVE_FRAMES, ZERGLING_DIE_FRAMES,
                X_PADDING, Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ATTACK_INFO, IS_EXPLOSIVE)

        sprites = Utils.ZERGLING_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]
        self.dir = 8
        self.changeToStill()
        if xIni != -1:
            self.updateOwnSpace()

        self.render = pg.transform.scale(pg.image.load(ZERG_T1_RENDER), UNIT_RENDER_SIZE)

        self.type = SOLDIER
    

    def toDictionary(self, map):
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "zergling",
            "nombre": "Zergling",
            "funcion": "Unidad ofensiva rapida"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
