import pygame as pg

from . import Entity, Worker
from ..Utils import *
from .Soldier import *

# Constantes del Hydralisk
HP = 150
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 30
ATTACK_INFO[COOLDOWN_IND] = 5
ATTACK_INFO[RANGE_IND] = 4 * RANGE_UNIT + RANGE_BASIC
MINE_POWER = 8
MINERAL_COST = 100
GAS_COST = 100
TIME_TO_MINE = 1000
GENERATION_TIME = 50
SPEED = 1.7
FRAMES_TO_REFRESH = 3
FACES = 8
FRAME = 0
PADDING = 110
WEIGHT_PADDING = 195
HEIGHT_PADDING = 130
X_PADDING = 20 * HYDRALISK_SCALE - 10
Y_PADDING = 20 * HYDRALISK_SCALE + 0

class Hydralisk(Soldier):
    selectedSound = zergSelectedSound
    generateSound = zerglingGenerateSound
    # Pre: xIni e yIni marcan posiciones del mapa, (ej: (3, 2) se refiere a la posicion de
    # la cuarta columna y tercera fila del mapa)
    def __init__(self, player, xIni = -1, yIni = -1):
        Soldier.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST,
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, FACES, FRAME, PADDING,
                takeID(), player, HYDRALISK_INVERSIBLE_FRAMES,
                HYDRALISK_FRAMES, DIR_OFFSET, HYDRALISK_ATTACK_FRAMES, HYDRALISK_STILL_FRAMES, HYDRALISK_MOVE_FRAMES, 
                HYDRALISK_DIE_FRAMES, X_PADDING, Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ATTACK_INFO, False)

        sprites = Utils.HYDRALISK_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]

        self.dir = 8
        self.changeToStill()
        if xIni != -1:
            self.updateOwnSpace()

        self.render = pg.transform.scale(pg.image.load(ZERG_T3_RENDER), UNIT_RENDER_SIZE)

        self.type = SOLDIER
    

    def toDictionary(self, map):
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "hydralisk",
            "nombre": "Hydralisk",
            "funcion": "Unidad ofesniva de rango"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
