import pygame

from .TerranSoldier import *
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *

HP = 200
GENERATION_TIME = 5

TILES_HEIGHT = 3
TILES_WIDTH = 4
CENTER_TILE = [1, 1]

class TerranSupplyDepot(Structure):
    sprites = []
    training = []
    generationTime = 0
    generationCount = 0
    nBuildSprites = 4
    deafault_index = 4
    generationStartTime = 0
    heightPad = 15
    rectOffY = 8
    tileW = 4
    tileH = 3
    clicked = False
    frame = 8

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, TERRAN_SUPPLY_MINERAL_COST, GENERATION_TIME, xini, yini, map, player)
        self.sprites = cargarSprites(TERRAN_SUPPLY_PATH, 5, False, WHITE, 1.5)
        self.image = self.sprites[self.index]
        self.operativeIndex = [4]
        self.spawningIndex = [4]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]

        self.render = pygame.transform.scale(pygame.image.load(SUPPLY_RENDER), RENDER_SIZE)

        self.training = []
        self.paths = []

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE

        self.type = TERRAN_DEPOT

    def command(self, command):
        return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[self.operativeIndex]

    def getOptions(self):
        return []

    def toDictionary(self, map):
        #print("barracke x e y Ini ", self.xIni, self.yIni)
        #x, y = map.getTileIndex(self.originX, self.originY)
        return {
            "clase": "terranSupplyDepot",
            "x": self.xIni,
            "y": self.yIni,
            "building": self.building,
            "nombre": "Deposito de suministros",
            "funcion": "aumenta la capacidad de suministros"
        }
