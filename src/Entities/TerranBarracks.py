import pygame

from .TerranSoldier import *
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *

HP = 200
GENERATION_TIME = 5

class TerranBarracks(Structure):
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
        Structure.__init__(self, HP, TERRAN_BARRACK_MINERAL_COST, GENERATION_TIME, xini, yini, map, id, player)
        self.sprites = cargarSprites(TERRAN_BARRACK_PATH, 6, False, WHITE, 1.1)
        self.building = building
        self.image = self.sprites[self.index]
        self.finalImage = self.sprites[4]

        self.count = 0
        self.training = []
        self.paths = []

    def update(self):

        if self.building:
            self.updateBuilding(4)
        elif len(self.training) > 0:
            if frame(10) == 1:
                if self.index == 5:
                    self.index = 4
                else:
                    self.index = 5
            self.updateTraining()
        else:
            self.index = 4
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)

    def execute(self, command_id):
        if self.clicked:
            print("soy clickeado?")
            if (command_id == CommandId.GENERAR_UNIDAD or command_id == CommandId.GENERATE_SOLDIER) and self.player.resources >= TERRAN_WORKER_MINERAL_COST:
                self.player.resources -= TERRAN_WORKER_MINERAL_COST
                terranSoldier = TerranSoldier(self.x / 40, (self.y + self.rectn.h) / 40, self.player)
                self.generateUnit(terranSoldier)

    def command(self, command):
        if not self.building:
            if command == CommandId.BUILD_STRUCTURE:
                return Command(CommandId.BUILD_BARRACKS)
            elif command == CommandId.GENERAR_UNIDAD:
                return Command(CommandId.GENERAR_UNIDAD)
            return Command(CommandId.NULO)
        else:
            print(3)
            return Command(CommandId.NULO)

    def getBuildSprite(self):
        return self.sprites[4]
    
    def getOptions(self):
        return [Options.GENERATE_SOLDIER]

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
