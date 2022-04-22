from enum import Enum, auto, IntEnum

import pygame

DEBBUG = False

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
PURPLE  = (255, 0, 255)
GREEN2  = (210, 255, 125)
GREEN3  = (110, 255, 90)

HP = pygame.image.load("SPRITE/vida3.png")
HP.set_colorkey(BLACK)

MAX_SELECTED_UNIT = 5

ENTITY_ID = 0

X_TILES = 20
Y_TILES = 15

SCREEN_WIDTH = 1025 
SCREEN_HEIGHT = 770 

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

    def copy(self):
        pathReturn = path(self.angle,self.dist,self.posFin)
        return pathReturn

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
MAIN_MENU_TEXT_SIZE = 30

SINGLE_TEXT_POS = [340, 215]
EXIT_TEXT_POS = [720, 600]

SINGLE_SIZE = 1.5 #(360, 180)
SINGLE_PLAYER = "SPRITE/mainMenu/SinglePlayer/single"
SINGLE_PLAYER_N = 35
SINGLE_PLAYER_POS = [20, 40]

SINGLE_PLAYER_FB = "SPRITE/mainMenu/SinglePlayer/Spanish/singleones"
SINGLE_PLAYER_FB_N = 60
SINGLE_PLAYER_FB_POS = [50, 160]

EXIT_SIZE = 1.5 #(300, 200)
EXIT = "SPRITE/mainMenu/Exit/exit"
EXIT_N = 50
EXIT_POS = [650, 420]

EXIT_FB = "SPRITE/mainMenu/Exit/Spanish/exitones"
EXIT_FB_N = 30
EXIT_FB_POS = [680, 420]


#----------------------------------------------------------------
# TROPAS
#----------------------------------------------------------------

##---------TERRAN_WORKER------------------
TERRAN_WORKER_MINERAL_COST = 20

##---------ZERGLING-----------------------
ZERGLING_MINERAL_COST = 20

#----------------------------------------------------------------
# ESTRUCTURAS
#----------------------------------------------------------------

##---------TERRAN_BUILDER------------------
TERRAN_BUILDER_PATH = "SPRITE/builder/tile00"

##---------TERRAN_BARRACK------------------
TERRAN_BARRACK_PATH = "SPRITE/barracks/tile00"

##---------ZERG_BUILDER------------------
ZERG_BUILDER_PATH = "SPRITE/ZergBuilder/tile00"


#carga n sprites con nombre path + 0 hasta path + (n-1)
#color para eliminar color del fondo, puede ser None
#numDigit inidca el numero de digitos para localizar el sprite 
def cargarSprites(path, n, twoDig, color = None, size = None):
    sprites = []
    for i in range(n): 
        if twoDig and i < 10:
            nPath = "0" + str(i)
        else:
            nPath = str(i)
        if size == None:
            sprites.insert(i, pygame.image.load(path + nPath + ".png"))
        elif size == 2:
            sprites.insert(i, pygame.transform.scale2x(pygame.image.load(path + nPath + ".png")))
        else:
            image = pygame.image.load(path + nPath + ".png")
            sprites.insert(i, pygame.transform.scale(image, [image.get_rect().w * size, image.get_rect().h * size]))
        if color != None:
            sprites[i].set_colorkey(color)
            pass
        
    return sprites

def clock_update():
    global SYSTEM_CLOCK
    SYSTEM_CLOCK = (SYSTEM_CLOCK + 1) % 100000

def frame(n):
    if SYSTEM_CLOCK % n == 0:
        return 1
    else:
        return 0
    
consolas = pygame.font.match_font('consolas')
times = pygame.font.match_font('times')
arial = pygame.font.match_font('arial')
courier = pygame.font.match_font('courier')

def muestra_texto(pantalla,fuente,texto,color, dimensiones, pos):
    tipo_letra = pygame.font.Font(pygame.font.match_font(fuente), dimensiones)
    superficie = tipo_letra.render(texto,True, color)
    rectangulo = superficie.get_rect()
    rectangulo.center = pos
    pantalla.blit(superficie,rectangulo)
    
def aux(screen):
    muestra_texto(screen, str('monotypecorsiva'), "single player", (210, 255, 124), 25, [270, 150])
    
   
ELEVACION_PATH = "SPRITE/tile/elevacion/tile0"
TERRENO_PATH = "SPRITE/tile/terreno/tile00"
  
MAPA1 = [[100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 202, 203, 204, 205, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 208, 209, 210, 211, 212, 213, 214, 215, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 216, 217, 218, 219, 220, 221, 222, 223, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 224, 225, 226, 227, 228, 229, 230, 231, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 234, 235, 236, 237, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 101, 102, 103, 104, 105, 106, 107, 100, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
         [100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 101, 102, 103, 104, 105, 106, 107, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
         ]