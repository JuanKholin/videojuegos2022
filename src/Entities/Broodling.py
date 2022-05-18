import pygame as pg

from . import Entity, Worker
from ..Utils import *
from .Soldier import *

# Constantes del Broodling
HP = 100
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 9
ATTACK_INFO[COOLDOWN_IND] = 5
ATTACK_INFO[RANGE_IND] = 1 * RANGE_UNIT + RANGE_BASIC
MINE_POWER = 8
MINERAL_COST = 50
GAS_COST = 25
TIME_TO_MINE = 1000
GENERATION_TIME = 30
SPEED = 3
FRAMES_TO_REFRESH = 2
SPRITE_PIXEL_ROWS = 48
FACES = 8
FRAME = 0
PADDING = 10
WEIGHT_PADDING = 50
HEIGHT_PADDING = 50
X_PADDING = 20 * BROODLING_SCALE - 20
Y_PADDING = 20 * BROODLING_SCALE - 10

class Broodling(Soldier):
    # Pre: xIni e yIni marcan posiciones del mapa, ej: 3 y 2
    def __init__(self, player, xIni = -1, yIni = -1):
        Soldier.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST,
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, FACES, FRAME, PADDING,
                takeID(), player, BROODLING_INVERSIBLE_FRAMES,
                BROODLING_FRAMES, DIR_OFFSET, BROODLING_ATTACK_FRAMES, BROODLING_STILL_FRAMES, BROODLING_MOVE_FRAMES, BROODLING_DIE_FRAMES,
                X_PADDING, Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ATTACK_INFO)
        
        sprites = Utils.BROODLING_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]

        self.dir = 8
        self.changeToStill()
        if xIni != -1:
            self.updateOwnSpace()

        self.render = pg.transform.scale(pg.image.load(ZERG_T2_RENDER), UNIT_RENDER_SIZE)

        self.type = SOLDIER
    

    def toDictionary(self, map):
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "broodling",
            "nombre": "Broodling",
            "funcion": "Unidad ofensiva de ataque rapido"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
