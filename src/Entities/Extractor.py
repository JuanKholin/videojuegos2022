import pygame

from .TerranSoldier import *
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *

HP = 200
GENERATION_TIME = 5

class Extractor(Structure):
    sprites = []
    training = []
    generationTime = 0
    generationCount = 0
    nBuildSprites = 3
    deafault_index = 3
    generationStartTime = 0
    heightPad = 20
    rectOffY = 40
    tileW = 4
    tileH = 3
    clicked = False
    frame = 8

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, EXTRACTOR_MINERAL_COST, GENERATION_TIME, xini, yini, map, player)
        self.sprites = cargarSprites(EXTRACTOR_PATH, 4, False, BLUE2, 1.1)
        self.image = self.sprites[self.index]
        self.operativeIndex = [0, 1, 2, 3]
        self.spawningIndex = [0, 1, 2, 3]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]

        self.render = pygame.transform.scale(pygame.image.load(EXTRACTOR_RENDER), RENDER_SIZE)

        self.state = BuildingState.OPERATIVE

        self.building = building
        
        self.count = 0
        self.training = []
        self.paths = []

        self.type = ZERG_GEYSER_STRUCTURE

    def getOptions(self):
        return []

    def command(self, command):
        return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[0]

    def toDictionary(self, map):
        #print("barracke x e y Ini ", self.xIni, self.yIni)
        #x, y = map.getTileIndex(self.originX, self.originY)
        return {
            "clase": "extractor",
            "x": self.xIni,
            "y": self.yIni,
            "building": self.building,
            "nombre": "Extractor de Zerg",
            "funcion": "extrae recursos"
        }
