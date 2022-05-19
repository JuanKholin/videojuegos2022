from enum import Enum, auto, IntEnum
from pickle import GLOBAL
import math
from re import T
from token import MINUS
from turtle import Screen
import pygame as pg
from .Lib import *

DEBBUG = True

BGM_VOLUME = 0.2
SOUND_VOLUME = 0.5
haveBGM = False

class System_State(Enum):
    MAINMENU = auto()
    GAMESELECT = auto()
    NEWGAME = auto()
    MAP1 = auto()
    ONGAME = auto()

    LOAD = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAMEOVER = auto()
    WIN = auto()
    BUILDING_MODE = auto()
    EXIT = auto()
    INTRO = auto()
    SETTINGS = auto()
    KEY_BINDING = auto()
    HELP = auto()

class Race(Enum):
    ZERG = auto()
    TERRAN = auto()
    PROTOSS = auto()

state = System_State.MAINMENU
state2 = System_State.PLAYING

def getGameState():
    global state
    result = state
    return result

def getGameState2():
    global state2
    result = state2
    return result

def setGameState(newState):
    global state
    state = newState

def setGameState2(newState):
    global state2
    state2 = newState

# Para el struct de la info de combate
DAMAGE_IND = 0
COOLDOWN_IND = 1
RANGE_IND = 2

#MEJORAS
DANYO_MEJORA = 0.2
ARMOR_MEJORA = 0.05
MINE_MEJORA = 1

# Tipos de clase (Para la IA):
SOLDIER = "SOLDIER"
WORKER = "WORKER"
REFINERY = "REFINERY"
BASE = "BASE"
BARRACKS = "BARRACKS"
DEPOT = "DEPOT"

# Tiles types:
EMPTY = 0
OBSTACLE = 1
UNIT = 2
RESOURCE = 3
GEYSER = 4
STRUCTURE = 5

# Resource types:
CRYSTAL = 1
VESPENE = 2

# Info de las tiles
TILE_WIDTH = 40
TILE_HEIGHT = 40

# En un mundo de  solo hay 8 direcciones creo yo
TOTAL_DIRECTIONS = 8

# dificultades IA (margen de decision en frames):
EASY = 0
MEDIUM = 1
HARD = 2
NULL = 3
DECISSION_RATE = [900, 600, 300, 10000]

# espera de la IA para tomar decisiones ligeras:
AI_LAPSE = [50, 40, 30, 10000]

# Edificios de las razas:
TERRAN_BASE = "TerranBuilder"
TERRAN_BARRACKS = "TerranBarracks"
TERRAN_DEPOT = "TerranSuplyDepot"
TERRAN_REFINERY = "TerranRefinery"
TERRAN_WORKER = "TerranWorker"
TERRAN_T1 = "TerranSoldier"
TERRAN_T2 = "Firebat"
TERRAN_T3 = "Goliath"

ZERG_BASE = "Hatchery"
ZERG_BARRACKS = "ZergBarracks"
ZERG_DEPOT = "ZergSupply"
ZERG_REFINERY = "Extractor"
ZERG_WORKER = "Drone"
ZERG_T1 = "Zergling"
ZERG_T2 = "Broodling"
ZERG_T3 = "Hydralisk"


PROTOSS_BASE = None
PROTOSS_BARRACKS = None
PROTOSS_DEPOT = None
PROTOSS_REFINERY = None
PROTOSS_WORKER = None
PROTOSS_SOLDIER = None


# Rango de autoataque (al matar a un objetivo que ataque a otro)
NEARBY_RANGE = 4

# Para los stats de los entities
RANGE_UNIT = TILE_WIDTH
RANGE_BASIC = 27
ARMOR_EXTRA = 1.1

#CLOCK = pg.time.Clock()

#contador del sistema
SYSTEM_CLOCK = 0

global_time = 0

CLOCK_PER_SEC = 60

# Constantes para los colores
WHITE   = (255, 255, 255)
GREY    = (170, 170, 170)
GREY2   = (83, 81, 83)
BLACK   = (0, 0, 0)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
RED2     = (255, 80, 80)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)
BLUE2   = (35, 35, 255)
BLUE3   = (80, 66, 255)
PURPLE  = (255, 0, 255)
GREEN2  = (210, 255, 125)
GREEN3  = (110, 255, 90)
GREEN4  = (140, 255, 150)
PINK    = (255, 95, 185)
ORANGE  = (255, 200, 95)
ORANGE2 = (255, 145, 0)

HP = pg.image.load("SPRITE/EXTRA/vida3.png")
HP2 = pg.image.load("SPRITE/EXTRA/vida2.png")
BARRA_SOUND = pg.image.load("SPRITE/EXTRA/sound.png")


#CAMERA
CAMERA_SPEED = 8
resized = False

MAX_SELECTED_UNIT = 8

ENTITY_ID = 0

X_TILES = 20
Y_TILES = 15

ScreenWidth = 1024
ScreenHeight = 770
MIN_SCREEN_WIDTH = 1024
MIN_SCREEN_HEIGHT = 770
SCREEN_SCALE = 1024/770
ScreenWD = 0
ScreenHD = 0

# Para los estados de las entidades
class UnitState(Enum):
    STILL = auto()
    MOVING = auto()
    ATTACKING = auto()
    MINING = auto()
    ORE_TRANSPORTING = auto()
    GAS_TRANSPORTING = auto()
    DYING = auto()
    DEAD = auto()
    EXTRACTING = auto()

class BuildingState(Enum):
    BUILDING = auto()
    OPERATIVE = auto()
    SPAWNING = auto() # porque lucecitas suena demasiado profesional
    COLLAPSING = auto()
    DESTROYED = auto()

class Path():
    def __init__(self, angle, dist, posFin):
        self.angle = angle
        self.dist = dist
        self.posFin = posFin

    def copy(self):
        pathReturn = Path(self.angle, self.dist, self.posFin)
        return pathReturn

class Rect():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

# Para los ID de las entidades
id = 1
def takeID():
    global id
    result = id
    id += 1
    return result

#----------------------------------------------------------------
# INTERFAZ
#----------------------------------------------------------------
MOUSE_PATH = "./SPRITE/raton/"
KEY_PATH = "./SPRITE/EXTRA/key.png"

MAIN_MENU = "SPRITE/mainMenu/fondo"
MAIN_MENU_TEXT_SIZE = 30


SINGLE_TEXT_POS = [MIN_SCREEN_WIDTH/2-300, MIN_SCREEN_HEIGHT/2-210]
EXIT_TEXT_POS = [MIN_SCREEN_WIDTH/2-720, MIN_SCREEN_HEIGHT/2-580]

SINGLE_SIZE = 1.5 #(360, 180)
SINGLE_PLAYER = "SPRITE/mainMenu/SinglePlayer/single"
SINGLE_PLAYER_N = 35
SINGLE_PLAYER_POS = [MIN_SCREEN_WIDTH/2-20, MIN_SCREEN_HEIGHT/2-40]

SINGLE_PLAYER_FB = "SPRITE/mainMenu/SinglePlayer/Spanish/singleones"
SINGLE_PLAYER_FB_N = 60
SINGLE_PLAYER_FB_POS = [MIN_SCREEN_WIDTH/2-50, MIN_SCREEN_HEIGHT/2-160]

EXIT_SIZE = 1.5 #(300, 200)
EXIT = "SPRITE/mainMenu/Exit/exit"
EXIT_N = 50
EXIT_POS = [MIN_SCREEN_WIDTH/2-650, MIN_SCREEN_HEIGHT/2-420]

EXIT_FB = "SPRITE/mainMenu/Exit/Spanish/exitones"
EXIT_FB_N = 30
EXIT_FB_POS = [MIN_SCREEN_WIDTH/2-680, MIN_SCREEN_HEIGHT/2-420]

AJUSTES_SONIDO_TEXT_POS = [MIN_SCREEN_WIDTH/2-80, MIN_SCREEN_HEIGHT/2-650]
AJUSTES_ATAJOS_TEXT_POS = [MIN_SCREEN_WIDTH/2-80, MIN_SCREEN_HEIGHT/2-700]
AJUSTES_SONIDO_POS = [MIN_SCREEN_WIDTH/2-80, MIN_SCREEN_HEIGHT/2-650]
AJUSTES_ATAJOS_POS = [MIN_SCREEN_WIDTH/2-80, MIN_SCREEN_HEIGHT/2-700]

    #############
    #GAME SELECT#
    #############

ACEPTAR_POS = [MIN_SCREEN_WIDTH/2-705, MIN_SCREEN_HEIGHT/2-590]
ACEPTAR_RECT = (250, 40)
CANCELAR_POS = [MIN_SCREEN_WIDTH/2-705, MIN_SCREEN_HEIGHT/2-695]
NUEVA_PARTIDA_POS = [MIN_SCREEN_WIDTH/2-88, MIN_SCREEN_HEIGHT/2-652]
PARTIDA_DEFAULT_POS = [MIN_SCREEN_WIDTH/2-80, MIN_SCREEN_HEIGHT/2-300]



GAME_SELECT = "SPRITE/gameSelect/"
GAME_SELECT_TEXT_SIZE = 30

    #############
    #GAME SELECT#
    #############
PARTIDA_POS = [MIN_SCREEN_WIDTH/2-72, MIN_SCREEN_HEIGHT/2-205]
YPARTIDA_PAD = 35

MAPA1_POS = [MIN_SCREEN_WIDTH/2-80, MIN_SCREEN_HEIGHT/2-269]
MAPA2_POS = [MIN_SCREEN_WIDTH/2-198, MIN_SCREEN_HEIGHT/2-269]
MAPA3_POS = [MIN_SCREEN_WIDTH/2-311, MIN_SCREEN_HEIGHT/2-269]
MAPA4_POS = [MIN_SCREEN_WIDTH/2-425, MIN_SCREEN_HEIGHT/2-269]

FACIL_POS = [MIN_SCREEN_WIDTH/2-84, MIN_SCREEN_HEIGHT/2-374]
NORMAL_POS = [MIN_SCREEN_WIDTH/2-236, MIN_SCREEN_HEIGHT/2-374]
DIFICIL_POS = [MIN_SCREEN_WIDTH/2-392, MIN_SCREEN_HEIGHT/2-374]

TERRAN_POS = [MIN_SCREEN_WIDTH/2-86, MIN_SCREEN_HEIGHT/2-493]
ZERG_POS = [MIN_SCREEN_WIDTH/2-321, MIN_SCREEN_HEIGHT/2-493]

NEW_GAME = "SPRITE/newGame/"
NEW_GAME_TEXT_SIZE = 30

BARRA_COMANDO = "SPRITE/EXTRA/gui_frame"

###############
#GAME SETTINGS#
###############

SETTINGS = "SPRITE/settings/settings_bg"
SETTINGS_TOP = "SPRITE/settings/settings_bg_top"
SETTINGS_BOT = "SPRITE/settings/settings_bg_bot"


KEY_TO_TEXT = {
     pg.K_UP: "UP",
     pg.K_DOWN: "DOWN",
     pg.K_RIGHT: "RIGHT",
     pg.K_LEFT: "LEFT",
     pg.K_0: "0",
     pg.K_1: "1",
     pg.K_2: "2",
     pg.K_3: "3",
     pg.K_4: "4",
     pg.K_5: "5",
     pg.K_6: "6",
     pg.K_7: "7",
     pg.K_8: "8",
     pg.K_9: "9",
     pg.K_q: "Q",
     pg.K_w: "W",
     pg.K_e: "E",
     pg.K_r: "R",
     pg.K_t: "T",
     pg.K_y: "Y",
     pg.K_u: "U",
     pg.K_i: "I",
     pg.K_o: "O",
     pg.K_p: "P",
     pg.K_a: "A",
     pg.K_s: "S",
     pg.K_d: "D",
     pg.K_f: "F",
     pg.K_g: "G",
     pg.K_h: "H",
     pg.K_j: "J",
     pg.K_k: "K",
     pg.K_l: "L",
     pg.K_z: "Z",
     pg.K_x: "X",
     pg.K_c: "C",
     pg.K_v: "V",
     pg.K_b: "B",
     pg.K_n: "N",
     pg.K_m: "M",
}

ATAJOS_TITLE_POS = [MIN_SCREEN_WIDTH/2 - 100, MIN_SCREEN_HEIGHT/2 - 25]
ATAJOS_TITLE_TEXT_SIZE = 50
COMANDO_COLUMN_POS = [MIN_SCREEN_WIDTH/2 - 150, MIN_SCREEN_HEIGHT/2 - 110]
TECLA_COLUMN_POS = [MIN_SCREEN_WIDTH/2 - 800, MIN_SCREEN_HEIGHT/2 - 110]
COLUMN_TEXT_SIZE = 35
COMANDO_POS = [MIN_SCREEN_WIDTH/2 - 150, MIN_SCREEN_HEIGHT/2 - 170]
TECLA_POS = [MIN_SCREEN_WIDTH/2 - 800, MIN_SCREEN_HEIGHT/2 - 170]
AVISO_COLUMN_POS = [MIN_SCREEN_WIDTH/2 - 400, MIN_SCREEN_HEIGHT/2 - 110]
ATAJO_TEXT_SIZE = 30
Y_ATAJOS_OFFSET = 40
REESTABLECER_POS = [MIN_SCREEN_WIDTH/2 - 10, MIN_SCREEN_HEIGHT/2 - 700]
REESTABLECER_SIZE = [219, 50]
GUARDAR_SALIR_SETTINGS_POS = [MIN_SCREEN_WIDTH/2 - 680, MIN_SCREEN_HEIGHT/2 - 710]
GUARDAR_SALIR_SETTINGS_SIZE = [310, 40]

SCROLL_BAR_TOP_TRIANGLE_POS = [(MIN_SCREEN_WIDTH/2 -970, MIN_SCREEN_HEIGHT/2 -185),(MIN_SCREEN_WIDTH/2-985, MIN_SCREEN_HEIGHT/2 -165),(MIN_SCREEN_WIDTH/2-1000, MIN_SCREEN_HEIGHT/2 -185)]
SCROLL_BAR_RECT_POS = [MIN_SCREEN_WIDTH/2 -970, MIN_SCREEN_HEIGHT/2 -195]
SCROLL_BAR_RECT_SIZE = [30, MIN_SCREEN_HEIGHT - MIN_SCREEN_HEIGHT*0.19 - MIN_SCREEN_HEIGHT*0.13 - 100]
SCROLL_BAR_BOT_TRIANGLE_POS = [(MIN_SCREEN_WIDTH/2 -970, MIN_SCREEN_HEIGHT/2 -630),(MIN_SCREEN_WIDTH/2-985, MIN_SCREEN_HEIGHT/2 -650),(MIN_SCREEN_WIDTH/2-1000, MIN_SCREEN_HEIGHT/2 -630)]
#----------------------------------------------------------------
# GUI
#----------------------------------------------------------------
BUTTON_X = MIN_SCREEN_WIDTH/2 - 810
BUTTON_Y = MIN_SCREEN_HEIGHT - 575
BUTTON_W = 60
BUTTON_H = 55
BUTTONPADY = -64
BUTTONPADX = -74

UPGRADEX = MIN_SCREEN_WIDTH/2 - 400
UPGRADEY = MIN_SCREEN_HEIGHT - 705

UPGRADEPADX = 80

MINIMAP_X = MIN_SCREEN_WIDTH/2 - 10
MINIMAP_Y = MIN_SCREEN_HEIGHT - 560
MINIMAP_W = 205
MINIMAP_H = 205

GUI_INFO_X = MIN_SCREEN_WIDTH/2 - 270
GUI_INFO_Y = MIN_SCREEN_HEIGHT - 610
GUI_INFO_X2 = MIN_SCREEN_WIDTH/2 - 420
GUI_INFO_Y2 = MIN_SCREEN_HEIGHT - 620

RESOURCES_COUNT_X = 300

#---
HEROE_PATH = "SPRITE/Heroes/Terran/Alexei Stukov/taxfid000"
HEROE_N = 10
#----

#-------------------------------------------------------------------------
# SPRITES-----------------------------------------------------------------
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
#-------------------------------------------------------------------------
# Para todo
def init():
    loadTerranWorker()
    loadDrone()
    loadTerranSoldier()
    loadZergling()
    loadFirebat()
    loadBroodling()
    loadGoliath()
    loadHydralisk()

    loadTerranBuilder()

# TerranWorker
TERRAN_WORKER_SCALE = 1.5
TERRAN_WORKER_SPRITE_ROWS = 72
TERRAN_WORKER_TOTAL_FRAMES = 296  # [0:15] MOVERSE Y STILL [16:31] MOVER ORE [32:47] MOVER BARRIL [48:217] ATACAR Y MINAR [289:295] MORICION
TERRAN_WORKER_FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(205, 221)), [221] * 16, [222] * 16, [223] * 16, [224] * 16,
          [225] * 16, [226] * 16, [227] * 16, [228] * 16, [229] * 16, [230] * 16]
TERRAN_WORKER_STILL_FRAMES = [0]
TERRAN_WORKER_ORE_TRANSPORTING_FRAMES = [3]
TERRAN_WORKER_GAS_TRANSPORTING_FRAMES = [2]
TERRAN_WORKER_ATTACK_FRAMES = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
TERRAN_WORKER_MOVE_FRAMES = [0]
TERRAN_WORKER_DIE_FRAMES = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
TERRAN_WORKER_INVERSIBLE_FRAMES = len(TERRAN_WORKER_FRAMES) - len(TERRAN_WORKER_DIE_FRAMES) # los die frames no se invierten
TERRAN_WORKER_SPRITES = [None, None]

def loadTerranWorker():
    global TERRAN_WORKER_SPRITES
    spritesheet = pg.image.load("./sprites/scvJusto.bmp").convert()
    spritesheet.set_colorkey(BLACK)
    deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
    deadSpritesheet.set_colorkey(BLACK)
    sprites = divideSpritesheetByRows(spritesheet, TERRAN_WORKER_SPRITE_ROWS, TERRAN_WORKER_SCALE) + divideSpritesheetByRowsNoScale(deadSpritesheet, 200, (80, 80))

    for i in range(TERRAN_WORKER_INVERSIBLE_FRAMES):
        for j in range(9, 16):
            sprites[TERRAN_WORKER_FRAMES[i][DIR_OFFSET[j]]] = pg.transform.flip(sprites[TERRAN_WORKER_FRAMES[i][DIR_OFFSET[j]]], True, False)

    shadows = []
    for i in range(len(sprites) - len(TERRAN_WORKER_DIE_FRAMES)):
        aux = pg.mask.from_surface(sprites[i], 0)
        mask = aux.to_surface(setcolor = (1, 0, 0))
        mask.set_colorkey(BLACK)
        mask.set_alpha(150)
        shadows.append(mask)
    TERRAN_WORKER_SPRITES = [sprites, shadows]

# Drone
DRONE_SCALE = 1.5
DRONE_SPRITE_ROWS = 128
DRONE_TOTAL_FRAMES = 391 # 23 ristas de 17 frames (solo son necesarios 16 de cada una)
DRONE_FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(205, 221)), list(range(222, 238)), list(range(239, 255)),
          list(range(256, 272)), list(range(273, 289)), list(range(290, 306))]
DRONE_STILL_FRAMES = [0]
DRONE_ATTACK_FRAMES = [6, 7, 8, 9]
DRONE_MOVE_FRAMES = [1, 2, 3, 4, 5]
DRONE_ORE_TRANSPORTING_FRAMES = DRONE_MOVE_FRAMES
DRONE_DIE_FRAMES = [10, 11, 12, 13, 14, 15, 16, 17]

DRONE_INVERSIBLE_FRAMES = len(DRONE_FRAMES) - 1 # los die frames no se invierten
DRONE_SPRITES = [None, None]
def loadDrone():
    global DRONE_SPRITES
    spritesheet = pg.image.load("./sprites/drone.bmp").convert()
    spritesheet.set_colorkey(BLACK)
    sprites = divideSpritesheetByRows(spritesheet, DRONE_SPRITE_ROWS, DRONE_SCALE)

    for i in range(DRONE_INVERSIBLE_FRAMES):
        for j in range(9, 16):
            sprites[DRONE_FRAMES[i][DIR_OFFSET[j]]] = pg.transform.flip(sprites[DRONE_FRAMES[i][DIR_OFFSET[j]]], True, False)

    shadows = []
    for i in range(len(sprites)):
        aux = pg.mask.from_surface(sprites[i], 0)
        mask = aux.to_surface(setcolor = (1, 0, 0))
        mask.set_colorkey(BLACK)
        mask.set_alpha(150)
        shadows.append(mask)
    DRONE_SPRITES = [sprites, shadows]

# TerranSoldier
TERRAN_SOLDIER_SCALE = 1.5
TERRAN_SOLDIER_SPRITE_ROWS = 64
TERRAN_SOLDIER_TOTAL_FRAMES = 221
TERRAN_SOLDIER_FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(205, 221)), [221] * 16, [222] * 16, [223] * 16, [224] * 16,
          [225] * 16, [226] * 16, [227] * 16, [228] * 16]
TERRAN_SOLDIER_STILL_FRAMES = [0]
TERRAN_SOLDIER_GUARD_FRAMES = [1]
TERRAN_SOLDIER_ATTACK_FRAMES = [2, 3]
TERRAN_SOLDIER_MOVE_FRAMES = [4, 5, 6, 7, 8, 9, 10, 11, 12]
TERRAN_SOLDIER_DIE_FRAMES = [13, 14, 15, 16, 17, 18, 19, 20]

TERRAN_SOLDIER_INVERSIBLE_FRAMES = len(TERRAN_SOLDIER_FRAMES) - len(TERRAN_SOLDIER_DIE_FRAMES)
TERRAN_SOLDIER_SPRITES = [None, None]

def loadTerranSoldier():
    global TERRAN_SOLDIER_SPRITES
    spritesheet = pg.image.load("./sprites/terran_soldier_sheet.bmp").convert()
    spritesheet.set_colorkey(WHITE)
    sprites = divideSpritesheetByRows(spritesheet, TERRAN_SOLDIER_SPRITE_ROWS, TERRAN_SOLDIER_SCALE)

    for i in range(TERRAN_SOLDIER_INVERSIBLE_FRAMES):
        for j in range(9, 16):
            sprites[TERRAN_SOLDIER_FRAMES[i][DIR_OFFSET[j]]] = pg.transform.flip(sprites[TERRAN_SOLDIER_FRAMES[i][DIR_OFFSET[j]]], True, False)

    shadows = []
    for i in range(len(sprites) - len(TERRAN_SOLDIER_DIE_FRAMES)):
        aux = pg.mask.from_surface(sprites[i], 0)
        mask = aux.to_surface(setcolor = (1, 0, 0))
        mask.set_colorkey(BLACK)
        mask.set_alpha(150)
        shadows.append(mask)
    TERRAN_SOLDIER_SPRITES = [sprites, shadows]

# Zergling
ZERGLING_SCALE = 1.5
ZERGLING_SPRITE_ROWS = 128
ZERGLING_TOTAL_FRAMES = 296
ZERGLING_FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          [289] * 16, [290] * 16, [291] * 16, [292] * 16, [293] * 16, [294] * 16,
          [295] * 16]
ZERGLING_STILL_FRAMES = [0]
ZERGLING_ATTACK_FRAMES = [1, 2, 3]
ZERGLING_MOVE_FRAMES = [4, 5, 6, 7, 8, 9, 10, 11]
ZERGLING_DIE_FRAMES = [12, 13, 14, 15, 16, 17, 18]

ZERGLING_INVERSIBLE_FRAMES = len(ZERGLING_FRAMES) - len(ZERGLING_DIE_FRAMES)
ZERGLING_SPRITES = [None, None]

def loadZergling():
    global ZERGLING_SPRITES
    spritesheet = pg.image.load("./sprites/zergling.bmp").convert()
    spritesheet.set_colorkey(BLACK)
    sprites = divideSpritesheetByRows(spritesheet, ZERGLING_SPRITE_ROWS, ZERGLING_SCALE)

    for i in range(ZERGLING_INVERSIBLE_FRAMES):
        for j in range(9, 16):
            sprites[ZERGLING_FRAMES[i][DIR_OFFSET[j]]] = pg.transform.flip(sprites[ZERGLING_FRAMES[i][DIR_OFFSET[j]]], True, False)

    shadows = []
    for i in range(len(sprites)):
        aux = pg.mask.from_surface(sprites[i], 0)
        mask = aux.to_surface(setcolor = (1, 0, 0))
        mask.set_colorkey(BLACK)
        mask.set_alpha(150)
        shadows.append(mask)
    ZERGLING_SPRITES = [sprites, shadows]

# Firebat
FIREBAT_SCALE = 1.5
FIREBAT_SPRITE_ROWS = 32
FIREBAT_TOTAL_FRAMES = 179

FIREBAT_FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), [170] * 16, [171] * 16, [172] * 16, [173] * 16,
          [174] * 16, [175] * 16, [176] * 16, [177] * 16, [178] * 16]
FIREBAT_STILL_FRAMES = [3]
FIREBAT_ATTACK_FRAMES = [0, 1]
FIREBAT_MOVE_FRAMES = [2, 4, 5, 6, 7, 8, 9]
FIREBAT_DIE_FRAMES = [10, 11, 12, 13, 14, 15, 16, 17, 18]
FIREBAT_INVERSIBLE_FRAMES = len(FIREBAT_FRAMES) - len(FIREBAT_DIE_FRAMES)
FIREBAT_SPRITES = [None, None]

def loadFirebat():
    global FIREBAT_SPRITES
    spritesheet = pg.image.load("./sprites/firebat.bmp").convert()
    spritesheet.set_colorkey(BLACK)
    deadSpritesheet = pg.image.load("./sprites/explosion2.bmp").convert()
    deadSpritesheet.set_colorkey(BLACK)
    sprites = divideSpritesheetByRows(spritesheet, FIREBAT_SPRITE_ROWS, FIREBAT_SCALE) + divideSpritesheetByRowsNoScale(deadSpritesheet, 128, (80, 80))

    for i in range(FIREBAT_INVERSIBLE_FRAMES):
        for j in range(9, 16):
            sprites[FIREBAT_FRAMES[i][DIR_OFFSET[j]]] = pg.transform.flip(sprites[FIREBAT_FRAMES[i][DIR_OFFSET[j]]], True, False)

    shadows = []
    for i in range(len(sprites)):
        aux = pg.mask.from_surface(sprites[i], 0)
        mask = aux.to_surface(setcolor = (1, 0, 0))
        mask.set_colorkey(BLACK)
        mask.set_alpha(150)
        shadows.append(mask)
    FIREBAT_SPRITES = [sprites, shadows]

# Broodling
BROODLING_SCALE = 2
BROODLING_SPRITE_ROWS = 48
BROODLING_TOTAL_FRAMES = 209
BROODLING_FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          [204] * 16, [205] * 16, [206] * 16, [207] * 16, [208] * 16]
BROODLING_STILL_FRAMES = [11]
BROODLING_ATTACK_FRAMES = [8, 9, 10]
BROODLING_MOVE_FRAMES = [0, 1, 2, 3, 4, 5, 6, 7]
BROODLING_DIE_FRAMES = [12, 13, 14, 15, 16]
BROODLING_INVERSIBLE_FRAMES = len(BROODLING_FRAMES) - len(BROODLING_DIE_FRAMES)
BROODLING_SPRITES = [None, None]
def loadBroodling():
    global BROODLING_SPRITES
    spritesheet = pg.image.load("./sprites/broodling.bmp").convert()
    spritesheet.set_colorkey(BLACK)
    sprites = divideSpritesheetByRows(spritesheet, BROODLING_SPRITE_ROWS, BROODLING_SCALE)

    for i in range(BROODLING_INVERSIBLE_FRAMES):
        for j in range(9, 16):
            sprites[BROODLING_FRAMES[i][DIR_OFFSET[j]]] = pg.transform.flip(sprites[BROODLING_FRAMES[i][DIR_OFFSET[j]]], True, False)

    shadows = []
    for i in range(len(sprites)):
        aux = pg.mask.from_surface(sprites[i], 0)
        mask = aux.to_surface(setcolor = (1, 0, 0))
        mask.set_colorkey(BLACK)
        mask.set_alpha(150)
        shadows.append(mask)
    BROODLING_SPRITES = [sprites, shadows]

# Goliath
GOLIATH_SCALE = 2
GOLIATH_SPRITE_ROWS = 76
GOLIATH_TOTAL_FRAMES = 179
GOLIATH_FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), [170] * 16, [171] * 16, [172] * 16, [173] * 16,
          [174] * 16, [175] * 16, [176] * 16, [177] * 16, [178] * 16]
GOLIATH_STILL_FRAMES = [0]
GOLIATH_ATTACK_FRAMES = [5, 6, 8, 9]
GOLIATH_MOVE_FRAMES = [0, 1, 2, 4, 5, 6, 7]
GOLIATH_DIE_FRAMES = [10, 11, 12, 13, 14, 15, 16, 17, 18]
GOLIATH_INVERSIBLE_FRAMES = len(GOLIATH_FRAMES) - len(GOLIATH_DIE_FRAMES)
GOLIATH_SPRITES = [None, None]

def loadGoliath():
    global GOLIATH_SPRITES
    spritesheet = pg.image.load("./sprites/goliath.bmp").convert()
    spritesheet.set_colorkey(BLACK)
    deadSpritesheet = pg.image.load("./sprites/explosion2.bmp").convert()
    deadSpritesheet.set_colorkey(BLACK)
    sprites = divideSpritesheetByRows(spritesheet, GOLIATH_SPRITE_ROWS, GOLIATH_SCALE) + divideSpritesheetByRowsNoScale(deadSpritesheet, 128, (80, 80))

    for i in range(len(GOLIATH_FRAMES)):
        for j in range(9, 16):
            sprites[GOLIATH_FRAMES[i][DIR_OFFSET[j]]] = pg.transform.flip(sprites[GOLIATH_FRAMES[i][DIR_OFFSET[j]]], True, False)

    shadows = []
    for i in range(len(sprites) - len(GOLIATH_DIE_FRAMES)):
        aux = pg.mask.from_surface(sprites[i], 0)
        mask = aux.to_surface(setcolor = (1, 0, 0))
        mask.set_colorkey(BLACK)
        mask.set_alpha(150)
        shadows.append(mask)
    GOLIATH_SPRITES = [sprites, shadows]

# Hydralisk
HYDRALISK_SCALE = 2
HYDRALISK_SPRITE_ROWS = 128
HYDRALISK_TOTAL_FRAMES = 212
HYDRALISK_FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          [204] * 16, [205] * 16, [206] * 16, [207] * 16, [208] * 16, [209] * 16,
          [210] * 16, [211] * 16]
HYDRALISK_STILL_FRAMES = [0]
HYDRALISK_ATTACK_FRAMES = [1, 2, 3, 4, 1]
HYDRALISK_MOVE_FRAMES = [5, 6, 7, 8, 9, 10, 11]
HYDRALISK_DIE_FRAMES = [12, 13, 14, 15, 16, 17, 18, 19]

HYDRALISK_INVERSIBLE_FRAMES = len(HYDRALISK_FRAMES) - len(HYDRALISK_DIE_FRAMES)
HYDRALISK_SPRITES = [None, None]

def loadHydralisk():
    global HYDRALISK_SPRITES
    spritesheet = pg.image.load("./sprites/hydralisk.bmp").convert()
    spritesheet.set_colorkey(BLACK)
    sprites = divideSpritesheetByRows(spritesheet, HYDRALISK_SPRITE_ROWS, HYDRALISK_SCALE)

    for i in range(HYDRALISK_INVERSIBLE_FRAMES):
        for j in range(9, 16):
            sprites[HYDRALISK_FRAMES[i][DIR_OFFSET[j]]] = pg.transform.flip(sprites[HYDRALISK_FRAMES[i][DIR_OFFSET[j]]], True, False)

    shadows = []
    for i in range(len(sprites)):
        aux = pg.mask.from_surface(sprites[i], 0)
        mask = aux.to_surface(setcolor = (1, 0, 0))
        mask.set_colorkey(BLACK)
        mask.set_alpha(150)
        shadows.append(mask)
    HYDRALISK_SPRITES = [sprites, shadows]


# TerranBuilder
TERRAN_BUILDER_TOTAL_FRAMES = 6
TERRAN_BUILDER_SPRITES = [None, None]
def loadTerranBuilder():
    global TERRAN_BUILDER_SPRITES
    sprites = cargarSprites(TERRAN_BUILDER_PATH, TERRAN_BUILDER_TOTAL_FRAMES, False, WHITE, 1.5)

    deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
    deadSpritesheet.set_colorkey(BLACK)
    deadSprites = divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

    sprites += deadSprites

    shadows = []
    for i in range(len(sprites)):
        aux = pg.mask.from_surface(sprites[i], 0)
        mask = aux.to_surface(setcolor = (1, 0, 0))
        mask.set_colorkey(BLACK)
        mask.set_alpha(150)
        shadows.append(mask)

    TERRAN_BUILDER_SPRITES = [sprites, shadows]

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------


class Options(Enum):
    GENERATE_WORKER_TERRAN = auto()
    GENERATE_WORKER_ZERG = auto()
    GENERATE_T1_TERRAN = auto()
    GENERATE_T1_ZERG = auto()
    GENERATE_T2_TERRAN = auto()
    GENERATE_T2_ZERG = auto()
    GENERATE_T3_TERRAN = auto()
    GENERATE_T3_ZERG = auto()
    BUILD_REFINERY_TERRAN = auto()
    BUILD_REFINERY_ZERG = auto()
    BUILD_DEPOT_TERRAN = auto()
    BUILD_DEPOT_ZERG = auto()
    BUILD_BARRACKS_TERRAN = auto()
    BUILD_BARRACKS_ZERG = auto()
    BUILD_HATCHERY = auto()
    DANYO_UPGRADE = auto()
    MINE_UPGRADE = auto()
    ARMOR_UPGRADE = auto()
    NULO = auto()
    NEXT_PAGE = auto()
    PREVIOUS_PAGE = auto()
    CLOSE = auto()
    PLUS_SOUND = auto()
    MINUS_SOUND = auto()
    PLUS_BGM = auto()
    MINUS_BGM = auto()

class Upgrades(Enum):
    DANYO = auto()
    ARMOR = auto()
    MINE = auto()
    NO_DANYO = auto()
    NO_ARMOR = auto()
    NO_MINE = auto()

BUTTON_PATH = "SPRITE/button/gui_button_"
#----------------------------------------------------------------
# TROPAS
#----------------------------------------------------------------

RENDER_SIZE = [85*1.6, 97*1.6]
UNIT_RENDER_SIZE = [85*1.4, 97*1.4]
SPAW_UNIT_RENDER_SIZE = [85 * 0.8, 97 * 0.8]
WAIT_UNIT_RENDER_SIZE = [85 * 0.7, 97 * 0.7]

##---------TerranWorker------------------
TERRAN_WORKER_MINERAL_COST = 20
TERRAN_WORKER_GAS_COST = 0
TERRAN_WORKER_RENDER = "SPRITE/render/terranWorker.png"

##---------Drone-------------------------
ZERG_WORKER_MINERAL_COST = 20
ZERG_WORKER_GAS_COST = 0
ZERG_WORKER_RENDER = "SPRITE/render/drone.png"

##---------TerranSoldier-----------------------
TERRAN_T1_MINERAL_COST = 20
TERRAN_T1_GAS_COST = 0
TERRAN_T1_RENDER = "SPRITE/render/terranSoldier.png"

##---------Zergling-----------------------
ZERG_T1_MINERAL_COST = 20
ZERG_T1_GAS_COST = 0
ZERG_T1_RENDER = "SPRITE/render/zergling.png"

##---------Firebat-----------------------
TERRAN_T2_MINERAL_COST = 50
TERRAN_T2_GAS_COST = 25
TERRAN_T2_RENDER = "SPRITE/render/firebat.png"

##---------Broodling-----------------------
ZERG_T2_MINERAL_COST = 50
ZERG_T2_GAS_COST = 25
ZERG_T2_RENDER = "SPRITE/render/broodling.png"

##---------Goliath-----------------------
TERRAN_T3_MINERAL_COST = 100
TERRAN_T3_GAS_COST = 100
TERRAN_T3_RENDER = "SPRITE/render/goliath.png"

##---------Hydralisk-----------------------
ZERG_T3_MINERAL_COST = 100
ZERG_T3_GAS_COST = 100
ZERG_T3_RENDER = "SPRITE/render/hydralisk.png"



#----------------------------------------------------------------
# ESTRUCTURAS
#----------------------------------------------------------------

##---------TERRAN_BUILDER------------------
TERRAN_BUILDER_PATH = "SPRITE/structure/builder/tile00"
BUILDER_RENDER = "SPRITE/render/terranBuilder.png"

##---------TERRAN_BARRACK------------------

TERRAN_BARRACKS_PATH = "SPRITE/structure/barracks/tile00"
TERRAN_BARRACKS_MINERAL_COST = 50
BARRACKS_RENDER = "SPRITE/render/terranBarracks.png"

##---------TERRAN_REFINERY------------------

TERRAN_REFINERY_PATH = "SPRITE/structure/refinery/refinery000"
TERRAN_REFINERY_MINERAL_COST = 50
REFINERY_RENDER = "SPRITE/render/terranRefinery.png"

##---------TERRAN_DEPOT------------------
##---------DEPOT------------------
TERRAN_DEPOT_PATH = "SPRITE/structure/supply_depot/tile00"
TERRAN_DEPOT_RENDER = "SPRITE/render/terranSupply.png"
TERRAN_DEPOT_MINERAL_COST = 50

##---------HATCHERY------------------
HATCHERY_PATH = "SPRITE/structure/Hatchery/tile00"
HATCHERY_RENDER = "SPRITE/render/hatchery.png"
HATCHERY_MINERAL_COST = 100

#-------------EXTRACTOR---------------
ZERG_REFINERY_PATH = "SPRITE/structure/extractor/tile00"
ZERG_REFINERY_RENDER = "SPRITE/render/extractor.png"
ZERG_REFINERY_MINERAL_COST = 60

#-----------BARRACKS_ZERG-------------
ZERG_BARRACKS_PATH = "SPRITE/structure/zergBarracks/tile00"
ZERG_BARRACKS_RENDER = "SPRITE/render/zergBarracks.png"
ZERG_BARRACKS_MINERAL_COST = 60

#-----------S2-------------
S2_PATH = "SPRITE/structure/Zerg_2/tile00"
S2_RENDER = "SPRITE/render/extractor.png"
S2_MINERAL_COST = 60

#-----------SUPPLY_ZERG-------------
ZERG_DEPOT_PATH = "SPRITE/structure/zergSupply/tile00"
ZERG_DEPOT_RENDER = "SPRITE/render/zergSupply.png"
ZERG_DEPOT_MINERAL_COST = 60

CRYSTAL_RENDER = "SPRITE/render/mineral.png"
GEYSER_RENDER = "SPRITE/render/geyser.png"


#carga n sprites con nombre path + 0 hasta path + (n-1)
#color para eliminar color del fondo, puede ser None
#numDigit inidca el numero de digitos para localizar el sprite
def cargarSprites(path, n, twoDig, color = None, scale = None, m = 0, size = None):
    sprites = []
    for i in range(m, n):
        if twoDig and i < 10:
            nPath = "0" + str(i)
        else:
            nPath = str(i)
        if size == None:
            if scale == None:
                sprites.insert(i, pg.image.load(path + nPath + ".png").convert_alpha())
            elif scale == 2:
                sprites.insert(i, pg.transform.scale2x(pg.image.load(path + nPath + ".png").convert_alpha()))
            else:
                image = pg.image.load(path + nPath + ".png").convert_alpha()
                sprites.insert(i, pg.transform.scale(image, [image.get_rect().w * scale, image.get_rect().h * scale]))
        else:
            image = pg.image.load(path + nPath + ".png").convert_alpha()
            sprites.insert(i, pg.transform.scale(image, [size[0], size[1]]))
        if color != None:
            sprites[i - m].set_colorkey(color)
    return sprites

def clock_update():
    global SYSTEM_CLOCK
    SYSTEM_CLOCK = (SYSTEM_CLOCK + 1) % 100000

def getGlobalTime():
    global global_time
    result = global_time
    return result

def updateGlobalTime(clock):
    global global_time
    global_time += clock.tick(CLOCK_PER_SEC)

def frame(n):
    if SYSTEM_CLOCK % n == 0:
        return 1
    else:
        return 0

consolas = pg.font.match_font('consolas')
times = pg.font.match_font('times')
arial = pg.font.match_font('arial')
courier = pg.font.match_font('courier')

def muestra_texto(pantalla,fuente,texto,color, dimensiones, pos, center = False):
    tipo_letra = pg.font.Font(pg.font.match_font(fuente), dimensiones)
    superficie = tipo_letra.render(texto, True, color)
    rectangulo = superficie.get_rect()
    #print(rectangulo)
    if not center:
        rectangulo.x = pos[0]
    else:
        rectangulo.x = pos[0] - rectangulo.w/2
    rectangulo.y = pos[1]
    pantalla.blit(superficie,rectangulo)
    #print(rectangulo)
    #rectangulo.x = pos[0]
    #rectangulo.y = pos[1]
    #pantalla.blit(superficie, rectangulo)

def aux(screen):
    muestra_texto(screen, str('monotypecorsiva'), "single player", (210, 255, 124), 25, [270, 150])

def calcPath(posini, tileIni, tileObj, mapa):
        pathA = mapa.Astar(tileIni,tileObj)
        if pathA.__len__() > 0:
            pathA.pop(0)
        posIni = (posini[0], posini[1])
        path = []
        for tile in pathA:
            posFin = (tile.centerx, tile.centery)
            path1 = Path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)
            path.append(path1)
            #print(mapa.getTile(posFin[0], posFin[1]).tileid)
            posIni = posFin
        return path

def calcPathNoLimit(posini, tileIni, tileObj, mapa):
        pathA = mapa.Astar(tileIni,tileObj)
        if pathA.__len__() > 0:
            pathA.pop(0)
        posIni = (posini[0], posini[1])
        path = []
        for tile in pathA:
            posFin = (tile.centerx, tile.centery)
            path1 = Path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)
            path.append(path1)
            #print(path1.angle)
            posIni = posFin
        return path

SURF_TILE_NIEBLA = pg.Surface((40,40), pg.SRCALPHA)
SURF_TILE_NIEBLA.fill((0,0,0,128))
SURF_TILE_OSCURA = pg.Surface((40,40))
SURF_TILE_OSCURA.fill((0,0,0))

ELEVACION_PATH = "SPRITE/tile/elevacion/tile0"
TERRENO_PATH = "SPRITE/tile/terreno/tile00"
CREEP_PATH = "SPRITE/tile/creep/creep0"

MAPA1 = [[100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 202, 203, 204, 205, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 208, 209, 210, 211, 212, 213, 214, 215, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 216, 217, 218, 219, 220, 221, 222, 223, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 224, 225, 226, 227, 228, 229, 230, 231, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 234, 235, 236, 237, 202, 203, 204, 205, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 208, 209, 210, 211, 212, 213, 214, 215, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 216, 217, 218, 219, 220, 221, 222, 223, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 224, 225, 226, 227, 228, 229, 230, 231, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 234, 235, 236, 237, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 234, 235, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 202, 203, 204, 205, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 208, 209, 210, 211, 212, 213, 214, 215, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 216, 217, 218, 219, 220, 221, 222, 223, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 224, 225, 226, 227, 228, 229, 230, 231, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 234, 235, 236, 237, 202, 203, 204, 205, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 208, 209, 210, 211, 212, 213, 214, 215, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 216, 217, 218, 219, 220, 221, 222, 223, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 224, 225, 226, 227, 228, 229, 230, 231, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 234, 235, 236, 237, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
         ]

EMPTY_MAP = [[100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         ]

MAPA_CHIKITO = [[100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                ]

MAPA_GRANDITO = [[100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 100, 100, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 105, 100, 100],
                [300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 103, 104, 105, 100, 100],
                [100, 101, 102, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 302, 303, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100],
                [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 303, 304, 305, 306, 307, 300, 301, 302, 303, 304, 305, 306, 307, 300, 301, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100],
                ]

MAPA2 = [[300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301,300, 301, 302, 303, 304, 305, 306, 307, 300, 301],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        [100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101,100, 101, 102, 103, 104, 105, 106, 107, 100, 101],
        ]

VISION_RADIUS = 7
VISION_RADIUS_PIXELS = VISION_RADIUS * TILE_WIDTH
