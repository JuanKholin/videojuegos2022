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
    nBuildSprites = 4
    deafault_index = 4
    generationStartTime = 0
    heightPad = 5
    rectOffY = 8
    tileW = 4
    tileH = 3
    clicked = False

    def __init__(self, xini, yini, player, map, building, id):
        Structure.__init__(self, HP, EXTRACTOR_MINERAL_COST, GENERATION_TIME, xini, yini, map, id, player)
        self.sprites = cargarSprites(EXTRATOR_SUPPLY_PATH, 5, False, WHITE, 1.5)
        self.building = building
        self.image = self.sprites[self.index]
        self.finalImage = self.sprites[4]
        
        self.render = pygame.transform.scale(pygame.image.load(EXTRATOR_RENDER), RENDER_SIZE)

        self.count = 0
        self.training = []
        self.paths = []

    def update(self):
        if self.building:
            self.building = False
        elif len(self.training) > 0:
            self.updateSpawning()
        self.index = (self.index + frame(8)) % 4
        self.image = self.sprites[self.index]
        self.image.set_colorkey(BLUE2)

    def execute(self, command_id):
        if self.clicked:
            if command_id == CommandId.GENERAR_UNIDAD and self.player.resources >= ZERGLING_MINERAL_COST:
                self.player.resources -= ZERGLING_MINERAL_COST
                zergling = Zergling(self.x / 40, (self.y + self.rectn.h) / 40, 1)
                self.generateUnit(zergling)

    def getOptions(self):
        return []

    def command(self, command):
        return Command(CommandId.NULO)

    def getBuildSprite(self):
        return self.sprites[0]

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
