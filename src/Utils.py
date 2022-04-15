from enum import Enum, auto, IntEnum

import pygame

class System_State(Enum):
    MAINMENU = auto()
    MAP1 = auto()
    ONGAME = auto()
    EXIT = auto()

STATE = System_State.MAINMENU

#contador del sistema
SYSTEM_CLOCK = 0

CLOCK_PER_SEC = 60

# Constantes para los colores
WHITE   = (255,255,255)
BLACK   = (0,0,0)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
BLUE    = (0, 0, 255)
PURPLE    = (255, 0, 255)

HP = pygame.image.load("SPRITE/vida2.png")
HP.set_colorkey(WHITE)

ENTITY_ID = 0

X_TILES = 20
Y_TILES = 10

SCREEN_WIDTH = X_TILES * 40
SCREEN_HEIGHT = Y_TILES * 40

# Para los estados de las entidades
class State(Enum):
    STILL = auto()
    MOVING = auto()
    ATTACKING = auto()
    DYING = auto()
    DEAD = auto()
    ORE_TRANSPORTING = auto()
    BARREL_TRANSPORTING = auto()
    MINING = auto()
    


class path():
    def __init__(self, angle, dist, posFin):
        self.angle = angle
        self.dist = dist
        self.posFin = posFin

class rect():
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


MAIN_MENU = "SPRITE/mainMenu/fondo"

SINGLE_PLAYER = "SPRITE/mainMenu/SinglePlayer/single"
SINGLE_PLAYER_N = 35
SINGLE_PLAYER_POS = [20, 40]

SINGLE_PLAYER_FB = "SPRITE/mainMenu/SinglePlayer/Spanish/singleones"
SINGLE_PLAYER_FB_N = 60
SINGLE_PLAYER_FB_POS = [50, 120]

EXIT = "SPRITE/mainMenu/Exit/exit"
EXIT_N = 50
EXIT_POS = [520, 200]

EXIT_FB = "SPRITE/mainMenu/Exit/Spanish/exitones"
EXIT_FB_N = 30
EXIT_FB_POS = [540, 200]

#----------------------------------------------------------------
# TROPAS
#----------------------------------------------------------------

##---------TERRAN_WORKER------------------
TERRAN_WORKER_MINERAL_COST = 20


#carga n sprites con nombre path + 0 hasta path + (n-1)
#color para eliminar color del fondo, puede ser None
#numDigit inidca el numero de digitos para localizar el sprite 
def cargarSprites(path, n, twoDig, color):
    sprites = []
    for i in range(n): 
        if twoDig and i < 10:
            nPath = "0" + str(i)
        else:
            nPath = str(i)
        sprites.insert(i, pygame.image.load(path + nPath + ".png"))
        if color != None:
            sprites[i].set_colorkey(color)
            pass
    return sprites

def clock_update():
    global SYSTEM_CLOCK
    SYSTEM_CLOCK = (SYSTEM_CLOCK + 1) % 1000

def frame(n):
    if SYSTEM_CLOCK % n == 0:
        return 1
    else:
        return 0