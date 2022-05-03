import pygame as pg

from .Entity import *
from ..Utils import *
from .Worker import *

# Constantes del Drone
HP = 400
DAMAGE = 5
COOLDOWN = 22
RANGE = 40
ATTACK_INFO = [DAMAGE, COOLDOWN, RANGE]
MINE_POWER = 8
MINERAL_COST = 20
TIME_TO_MINE = 1000
GENERATION_TIME = 200
SPEED = 2
FRAMES_TO_REFRESH = 5
SPRITES = "drone.bmp"
SPRITE_PIXEL_ROWS = 128
SCALE = 1.5
FACES = 8
FRAME = 0
TOTAL_FRAMES = 391 # 23 ristas de 17 frames (solo son necesarios 16 de cada una)
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(205, 221)), list(range(222, 238)), list(range(239, 255)),
          list(range(256, 272)), list(range(273, 289)), list(range(290, 306))]
#         list(range(307, 323)), list(range(324, 340)), list(range(341, 357)),
#         list(range(358, 374)), list(range(375, 391))]
#DONT_TOUCH_FRAMES = [18, 19, 20, 21, 22]

STILL_FRAMES = [0]
ATTACK_FRAMES = [6, 7, 8, 9]
MOVE_FRAMES = [1, 2, 3, 4, 5]
ORE_TRANSPORTING_FRAMES = MOVE_FRAMES
DIE_FRAMES = [10, 11, 12, 13, 14, 15, 16, 17]

INVERSIBLE_FRAMES = len(FRAMES) - 1 # los die frames no se invierten
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-frame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
PADDING = 110
WEIGHT_PADDING = 145
HEIGHT_PADDING = 155
X_PADDING = 22
Y_PADDING = 22

class Drone(Worker):
    # Pre: xIni e yIni marcan posiciones del mapa, (ej: (3, 2) se refiere a la posicion de
    # la cuarta columna y tercera fila del mapa)
    # Post: Crea un bichito mono que no hace practicamente nada pero tu dale tiempo
    def __init__(self, xIni, yIni, player):
        Worker.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST, GENERATION_TIME,
                SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME, PADDING, takeID(), player,
                MINE_POWER, TIME_TO_MINE, INVERSIBLE_FRAMES, FRAMES, DIR_OFFSET,
                ATTACK_FRAMES, STILL_FRAMES, MOVE_FRAMES, DIE_FRAMES, X_PADDING, Y_PADDING,
                WEIGHT_PADDING, HEIGHT_PADDING, MOVE_FRAMES, ATTACK_INFO)
        spritesheet = pg.image.load("./sprites/" + self.spritesName).convert()
        spritesheet.set_colorkey(BLACK)
        self.sprites = Entity.divideSpritesheetByRows(spritesheet, SPRITE_PIXEL_ROWS, SCALE)
        self.mirrorTheChosen()
        self.dir = 8
        self.changeToStill()
        self.render = pygame.transform.scale(pygame.image.load(DRONE_RENDER), UNIT_RENDER_SIZE)

    def toDictionary(self, map):
        x, y = map.getTileIndex(self.x, self.y)
        return {
            "clase": "drone",
            "x": x,
            "y": y,
        }
