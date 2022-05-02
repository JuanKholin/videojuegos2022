import pygame
from .Zergling import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *

WHITE   = (255,255,255)
GENERATION_TIME = 10
MINERAL_COST = 50
HP = 200

class Hatchery(Structure):
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

    def __init__(self, xini, yini, player, map, building, id):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, id, player)
        self.sprites = cargarSprites(HATCHERY_PATH, 4, False, BLUE2, 1.8, 0)
        self.building = building
        self.image = self.sprites[self.index]
        self.finalImage = self.sprites[3]
        
        self.render = pygame.transform.scale(pygame.image.load(HATCHERY_RENDER), RENDER_SIZE)

        self.count = 0
        self.training = []
        self.paths = []

    def update(self):
        if self.building:
            self.building = False
        elif len(self.training) > 0:
            self.updateTraining()
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
        #return [Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS]
        return [Options.GENERATE_WORKER, Options.BUILD_HATCHERY]

    def command(self, command):
        if command == CommandId.BUILD_STRUCTURE:
            return Command(CommandId.BUILD_ZERG_BUILDER)
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
            "clase": "zergBuilder",
            "x": self.xIni,
            "y": self.yIni,
            "building": self.building,
            "id": self.id,
        }
