from enum import Enum, auto, IntEnum

ENTITY_ID = 0

# Constantes para los colores
WHITE   = (255,255,255)
BLACK   = (0,0,0)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
BLUE    = (0, 0, 255)
PURPLE    = (255, 0, 255)

X_TILES = 20
Y_TILES = 10

SCREEN_WIDTH = X_TILES * 40
SCREEN_HEIGHT = Y_TILES * 40

CLOCK_PER_SEC = 60

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
# TROPAS
#----------------------------------------------------------------

##---------TERRAN_WORKER------------------
TERRAN_WORKER_MINERAL_COST = 20