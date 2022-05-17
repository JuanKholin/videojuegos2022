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
SPRITES = "hydralisk.bmp"
SPRITE_PIXEL_ROWS = 128
FACES = 8
FRAME = 0
SCALE = 2
TOTAL_FRAMES = 204 + 8  # [0:203] MOVICION
                    # [204:211] MORICION
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          [204] * 16, [205] * 16, [206] * 16, [207] * 16, [208] * 16, [209] * 16,
          [210] * 16, [211] * 16]
STILL_FRAMES = [0]
ATTACK_FRAMES = [1, 2, 3, 4, 1]
MOVE_FRAMES = [5, 6, 7, 8, 9, 10, 11]
DIE_FRAMES = [12, 13, 14, 15, 16, 17, 18, 19]
INVERSIBLE_FRAMES = len(FRAMES) - len(DIE_FRAMES) # los die frames no se invierten
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-frame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
PADDING = 110
WEIGHT_PADDING = 195
HEIGHT_PADDING = 170
X_PADDING = 20 * SCALE - 10
Y_PADDING = 20 * SCALE + 15

class Hydralisk(Soldier):
    # Pre: xIni e yIni marcan posiciones del mapa, (ej: (3, 2) se refiere a la posicion de
    # la cuarta columna y tercera fila del mapa)
    def __init__(self, player, xIni = -1, yIni = -1):
        Soldier.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST,
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME, PADDING,
                takeID(), player, INVERSIBLE_FRAMES,
                FRAMES, DIR_OFFSET, ATTACK_FRAMES, STILL_FRAMES, MOVE_FRAMES, DIE_FRAMES,
                X_PADDING, Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ATTACK_INFO)
        spritesheet = pg.image.load("./sprites/" + self.spritesName).convert()
        spritesheet.set_colorkey(BLACK)
        self.sprites = Entity.divideSpritesheetByRows(spritesheet, SPRITE_PIXEL_ROWS, SCALE)
        self.mirrorTheChosen()
        self.dir = 8
        self.changeToStill()
        if xIni != -1:
            self.updateOwnSpace()

        self.render = pygame.transform.scale(pygame.image.load(HYDRALISK_REDNER), UNIT_RENDER_SIZE)

        self.type = ZERG_SOLDIER
    

    def toDictionary(self, map):
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "hydralisk",
            "nombre": "Hydralisk",
            "funcion": "Unidad Zerg de rango"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
