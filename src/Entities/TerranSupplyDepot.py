import pygame

from .TerranSoldier import *
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *

HP = 200
GENERATION_TIME = 5

class TerranSupplyDepot(Structure):
    sprites = []
    training = []
    generationTime = 0
    generationCount = 0
    nBuildSprites = 4
    deafault_index = 4
    generationStartTime = 0
    heightPad = 5
    rectOffY = 8
    tileW = 4
    tileH = 3
    clicked = False

    def __init__(self, xini, yini, player, map, building, id):
        Structure.__init__(self, HP, TERRAN_SUPPLY_MINERAL_COST, GENERATION_TIME, xini, yini, map, id, player)
        self.sprites = cargarSprites(TERRAN_SUPPLY_PATH, 5, False, WHITE, 1.5)
        self.building = building
        self.image = self.sprites[self.index]
        self.finalImage = self.sprites[4]
        
        self.render = pygame.transform.scale(pygame.image.load(SUPPLY_RENDER), RENDER_SIZE)

        self.count = 0
        self.training = []
        self.paths = []

    def update(self):

        if self.building:
            self.updateBuilding(4)
        else:
            self.index = 4
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)

    def command(self, command):
        return Command(CommandId.NULO)

    def getBuildSprite(self):
        return self.sprites[4]
    
    def getOptions(self):
        return []

    def toDictionary(self, map):
        #print("barracke x e y Ini ", self.xIni, self.yIni)
        #x, y = map.getTileIndex(self.originX, self.originY)
        return {
            "clase": "terranBarracks",
            "x": self.xIni,
            "y": self.yIni,
            "building": self.building,
            "id": self.id,
        }
