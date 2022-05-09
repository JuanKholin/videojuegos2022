import pygame
from .Zergling import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *

WHITE   = (255,255,255)
GENERATION_TIME = 10
MINERAL_COST = 50
WIDTH = 6 
HEIGHT = 4
HP = 200

class Hatchery(Structure):
    TILES_HEIGHT = 4
    TILES_WIDTH = 6
    CENTER_TILE = [2, 2]
    sprites = []
    training = []
    heightPad = 10
    generationTime = 0
    generationCount = 0
    widthPad = -20
    rectOffY = 90
    tileW = 6
    clicked = False
    tileH = 4
    frame = 8

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, player)
        self.sprites = cargarSprites(HATCHERY_PATH, 4, False, BLUE2, 1.8, 0)
        self.image = self.sprites[self.index]
        self.operativeIndex = [0, 1, 2, 3]
        self.spawningIndex = [0, 1, 2, 3]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]

        self.render = pygame.transform.scale(pygame.image.load(HATCHERY_RENDER), RENDER_SIZE)

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE
        self.count = 0

        self.count = 0
        self.training = []
        self.paths = []
        self.building = False

        self.type = ZERG_BASE

    def execute(self, command_id):
        if self.clicked:
            if command_id == CommandId.GENERAR_UNIDAD and self.player.resources >= ZERGLING_MINERAL_COST:
                self.player.resources -= ZERGLING_MINERAL_COST
                zergling = Zergling(self.x / 40, (self.y + self.rectn.h) / 40, self.player)
                self.generateUnit(zergling)

    def getOptions(self):
        #return [Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS]
        return [Options.GENERATE_WORKER, Options.BUILD_HATCHERY]

    def command(self, command):
        if command == CommandId.BUILD_STRUCTURE:
            return Command(CommandId.BUILD_HATCHERY)
        elif command == CommandId.GENERAR_UNIDAD:
            return Command(CommandId.GENERAR_UNIDAD)
        else:
            return Command(CommandId.NULO)

    def getBuildSprite(self):
        return self.sprites[3]

    def toDictionary(self, map):
        #print("x e y del zerg builder ", self.x, self.y)
        #x, y = map.getTileIndex(self.originX, self.originY)
        return {
            "clase": "hatchery",
            "x": self.xIni,
            "y": self.yIni,
            "building": self.building,
            "nombre": "Criadera de Zerg",
            "funcion": "Base enemiga"
        }
