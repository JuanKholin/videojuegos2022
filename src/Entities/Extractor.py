import pygame

from .TerranSoldier import *
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *
from .Entity import *

HP = 200
GENERATION_TIME = 5
CAPACITY = 0

class Extractor(Structure):
    TILES_WIDTH = 4
    TILES_HEIGHT = 3
    CENTER_TILE = [1, 1]
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
    nSprites = 4

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, EXTRACTOR_MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        self.sprites = cargarSprites(EXTRACTOR_PATH, self.nSprites, False, BLUE2, 1.1)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        deadSprites = Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.sprites += deadSprites

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

    def command(self, command):
        return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[0]

    def toDictionary(self, map):
        #print("barracke x e y Ini ", self.xIni, self.yIni)
        #x, y = map.getTileIndex(self.originX, self.originY)
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "extractor",
            "building": self.building,
            "nombre": "Extractor de Zerg",
            "funcion": "extrae recursos"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
