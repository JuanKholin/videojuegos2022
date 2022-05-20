import pygame as pg

from .Entity import *
from ..Utils import *
from .Worker import *

# Constantes del Drone
HP = 60
DAMAGE = 2
COOLDOWN = 15
RANGE = 1 * RANGE_UNIT + RANGE_BASIC
ATTACK_INFO = [DAMAGE, COOLDOWN, RANGE]
MINE_POWER = 10
MINERAL_COST = ZERG_WORKER_MINERAL_COST
GAS_COST = ZERG_WORKER_GAS_COST
TIME_TO_MINE = 11000
GENERATION_TIME = 20
SPEED = 5
FRAMES_TO_REFRESH = 2
FACES = 8
FRAME = 0

PADDING = 110
WEIGHT_PADDING = 145
HEIGHT_PADDING = 145
X_PADDING = 22
Y_PADDING = 22

IS_EXPLOSIVE = False

class Drone(Worker):
    selectedSound = zergSelectedSound
    generateSound = zerglingGenerateSound
    attackSound = zerglingAttackSound
    # Pre: xIni e yIni marcan posiciones del mapa, (ej: (3, 2) se refiere a la posicion de
    # la cuarta columna y tercera fila del mapa)
    # Post: Crea un bichito mono que no hace practicamente nada pero tu dale tiempo
    def __init__(self, player, xIni = -1, yIni = -1):
        Worker.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST, GENERATION_TIME,
                SPEED, FRAMES_TO_REFRESH, FACES, FRAME, PADDING, takeID(), player,
                MINE_POWER, TIME_TO_MINE, DRONE_INVERSIBLE_FRAMES, DRONE_FRAMES, DIR_OFFSET,
                DRONE_ATTACK_FRAMES, DRONE_STILL_FRAMES, DRONE_MOVE_FRAMES, DRONE_DIE_FRAMES, X_PADDING, Y_PADDING,
                WEIGHT_PADDING, HEIGHT_PADDING, DRONE_MOVE_FRAMES, DRONE_MOVE_FRAMES, ATTACK_INFO, IS_EXPLOSIVE)

        sprites = Utils.DRONE_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]
        
        self.dir = 8
        self.changeToStill()
        if xIni != -1:
            self.updateOwnSpace()
        self.render = pg.transform.scale(pg.image.load(ZERG_WORKER_RENDER), UNIT_RENDER_SIZE)
        self.type = WORKER


    def toDictionary(self, map):
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "drone",
            "nombre": "Drone",
            "funcion": "Unidad obrera"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
