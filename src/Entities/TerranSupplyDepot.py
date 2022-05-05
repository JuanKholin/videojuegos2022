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
    frame = 8

    def __init__(self, xini, yini, player, map, building, id):
        Structure.__init__(self, HP, TERRAN_SUPPLY_MINERAL_COST, GENERATION_TIME, xini, yini, map, id, player)
        self.sprites = cargarSprites(TERRAN_SUPPLY_PATH, 5, False, WHITE, 1.5)
        self.image = self.sprites[self.index]
        self.operativeIndex = [4]
        self.spawningIndex = [4]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]
        
        self.render = pygame.transform.scale(pygame.image.load(SUPPLY_RENDER), RENDER_SIZE)

        self.training = []
        self.paths = []
        
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE

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
            "clase": "terranBarracks",
            "x": self.xIni,
            "y": self.yIni,
            "id": self.id,
        }
