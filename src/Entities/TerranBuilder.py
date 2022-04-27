import pygame
from .TerranWorker import *
from .. import Player, Map, Tile
from .Structure import *
from ..Command import *
from src.Utils import *

HP = 200
GENERATION_TIME = 40
MINERAL_COST = 600

class TerranBuilder(Structure):
    sprites = []
    training = []
    rectOffY = 3
    generationTime = 0
    generationCount = 0
    heightPad = 25
    hola = 0
    tileW = 5
    tileH = 4
    clicked = False

    def __init__(self, xini, yini, player, map, building, id):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, id, player)
        self.sprites = cargarSprites(TERRAN_BUILDER_PATH, 6, False, WHITE, 1.5)
        self.image = self.sprites[self.index]
        self.finalImage = self.sprites[4]
        self.building = building
        self.count = 0

        self.training = []
        self.paths = []

    def update(self):
        if self.building:
            self.count += 1
            if self.count == self.generationTime/3:
                self.index += 1
                self.count = 0
                if self.index == 4:
                    self.building = False
        elif len(self.training) > 0:
            self.count += 1
            if self.count == 10:
                self.count = 0
                if self.index == 5:
                    self.index = 4
                else:
                    self.index = 5
            self.generationCount += 1
            if self.generationCount == CLOCK_PER_SEC * self.training[0].generationTime:
                terran = self.training[0]
                terranPos = terran.getPosition()
                terranTile = self.map.getTile(terranPos[0], terranPos[1])
                if terranTile.type != 0:
                    vecinas = self.map.getTileVecinas(terranTile)
                    terran.setTilePosition(vecinas[0])
                self.player.addUnits(terran)
                self.generationCount = 0
                del self.training[0]
        else:
            self.index = 4
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)

    def generateUnit(self, unit):
        self.training.append(unit)

    def getOrder(self):
        return CommandId.TRANSPORTAR_ORE_STILL

    def execute(self, command_id):
        if self.clicked:
            if command_id == CommandId.GENERAR_UNIDAD and self.player.resources >= TERRAN_WORKER_MINERAL_COST:
                self.player.resources -= TERRAN_WORKER_MINERAL_COST
                terranWorker = TerranWorker(self.x / 40, (self.y + self.rectn.h) / 40, self.player)
                self.generateUnit(terranWorker)

    def command(self, command):
        if command == CommandId.BUILD_STRUCTURE:
            return Command(CommandId.BUILD_BARRACKS)
        elif command == CommandId.GENERAR_UNIDAD:
            return Command(CommandId.GENERAR_UNIDAD)
        else:
            return Command(CommandId.NULO)

    def getBuildSprite(self):
        return self.sprites[4]

    def toDictionary(self, map):
        #x, y = map.getTileIndex(self.originX, self.originY)
        return {
            "clase": "terranBuilder",
            "x": self.xIni,
            "y": self.yIni,
            "building": self.building,
            "id": self.id,
        }
