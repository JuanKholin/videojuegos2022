from enum import Enum, auto, IntEnum
from pickle import GLOBAL
import math
from re import T
import pygame

DEBBUG = True

class System_State(Enum):
    MAINMENU = auto()
    MAP1 = auto()
    ONGAME = auto()
    BUILDING_MODE = auto()
    EXIT = auto()

state = System_State.MAINMENU

def getGameState():
    global state
    result = state
    return result

def setGameState(newState):
    global state
    state = newState

# Para el struct de la info de combate
DAMAGE_IND = 0
COOLDOWN_IND = 1
RANGE_IND = 2

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

# dificultades IA (margen de decision en frames):
EASY = 1000
MEDIUM = 600
HARD = 200

# espera de la IA para tomar decisiones ligeras:
AI_LAPSE = 50


#CLOCK = pygame.time.Clock()

#contador del sistema
SYSTEM_CLOCK = 0

global_time = 0

CLOCK_PER_SEC = 60

# Constantes para los colores
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
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

HP = pygame.image.load("SPRITE/EXTRA/vida3.png")
HP.set_colorkey(WHITE)
HP2 = pygame.image.load("SPRITE/EXTRA/vida2.png")
HP.set_colorkey(WHITE)

BGM_VOLUME = 0.5
SOUND_VOLUME = 0.5
haveBGM = False

CAMERA_SPEED = 8

MAX_SELECTED_UNIT = 8

ENTITY_ID = 0

X_TILES = 20
Y_TILES = 15

SCREEN_WIDTH = 1025
SCREEN_HEIGHT = 770

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

BARRA_COMANDO = "SPRITE/EXTRA/gui_frame"

#----------------------------------------------------------------
# GUI
#----------------------------------------------------------------
BUTTON_X = 810
BUTTON_Y = 575
BUTTON_W = 60
BUTTON_H = 55
BUTTONPADY = 64
BUTTONPADX = 74

UPGRADEPADX = 80

MINIMAP_X = 10
MINIMAP_Y = 560
MINIMAP_W = 205 
MINIMAP_H = 205

GUI_INFO_X = 280
GUI_INFO_Y = 610
GUI_INFO_X2 = 510
GUI_INFO_Y2 = 645

RESOURCES_COUNT_X = SCREEN_WIDTH - 300

#---
HEROE_PATH = "SPRITE/Heroes/Terran/Alexei Stukov/taxfid000"
HEROE_N = 10
#----


class Options(Enum):
    BUILD_BARRACKS = auto()
    GENERATE_WORKER = auto()
    GENERATE_SOLDIER = auto()
    BUILD_REFINERY = auto()
    BUILD_HATCHERY = auto()
    DANYO_UPGRADE = auto()
    MINE_UPGRADE = auto()
    ARMOR_UPGRADE = auto()
    NULO = auto()


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

##---------TERRAN_WORKER------------------
TERRAN_WORKER_MINERAL_COST = 20
WORKER_RENDER = "SPRITE/render/terranWorker.png"

TERRAN_SOLDIER_MINERAL_COST = 20
SOLDIER_RENDER = "SPRITE/render/terranSoldier.png"

##---------ZERGLING-----------------------
ZERGLING_MINERAL_COST = 20
ZERGLING_RENDER = "SPRITE/render/zergling.png"

##---------DRONE--------------------------
DRONE_MINERAL_COST = 20
DRONE_RENDER = "SPRITE/render/drone.png"

#----------------------------------------------------------------
# ESTRUCTURAS
#----------------------------------------------------------------

##---------TERRAN_BUILDER------------------
TERRAN_BUILDER_PATH = "SPRITE/structure/builder/tile00"
BUILDER_RENDER = "SPRITE/render/terranBuilder.png"

##---------TERRAN_BARRACK------------------

TERRAN_BARRACK_PATH = "SPRITE/structure/barracks/tile00"
TERRAN_BARRACK_MINERAL_COST = 50
BARRACKS_RENDER = "SPRITE/render/terranBarracks.png"

##---------TERRAN_REFINERY------------------

TERRAN_REFINERY_PATH = "SPRITE/structure/refinery/refinery000"
TERRAN_REFINERY_MINERAL_COST = 50
REFINERY_RENDER = "SPRITE/render/terranRefinery.png"

##---------HATCHERY------------------
HATCHERY_PATH = "SPRITE/structure/Hatchery/tile00"
HATCHERY_RENDER = "SPRITE/render/hatchery.png"
HATCHERY_MINERAL_COST = 100

#-------------EXTRACTOR---------------
EXTRACTOR_PATH = "SPRITE/structure/extractor/tile00"
EXTRACTOR_RENDER = "SPRITE/render/extractor.png"
EXTRACTOR_MINERAL_COST = 60

##---------SUPPLY------------------
TERRAN_SUPPLY_PATH = "SPRITE/structure/supply_depot/tile00"
SUPPLY_RENDER = "SPRITE/render/terranSupply.png"
TERRAN_SUPPLY_MINERAL_COST = 50

CRYSTAL_RENDER = "SPRITE/render/mineral.png"
GEYSER_RENDER = "SPRITE/render/geyser.png"


#carga n sprites con nombre path + 0 hasta path + (n-1)
#color para eliminar color del fondo, puede ser None
#numDigit inidca el numero de digitos para localizar el sprite
def cargarSprites(path, n, twoDig, color = None, size = None, m = 0):
    sprites = []
    for i in range(m, n):
        if twoDig and i < 10:
            nPath = "0" + str(i)
        else:
            nPath = str(i)
        if size == None:
            sprites.insert(i, pygame.image.load(path + nPath + ".png").convert_alpha())
        elif size == 2:
            sprites.insert(i, pygame.transform.scale2x(pygame.image.load(path + nPath + ".png").convert_alpha()))
        else:
            image = pygame.image.load(path + nPath + ".png").convert_alpha()
            sprites.insert(i, pygame.transform.scale(image, [image.get_rect().w * size, image.get_rect().h * size]))
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
            posIni = posFin
        return path

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
