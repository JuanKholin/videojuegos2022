import pygame
from . import Structure, Zergling
from .. import Player, Map, Utils, Tile, Command
from src.Utils import *

WHITE   = (255,255,255)

class ZergBuilder(Structure.Structure):
    sprites = []
    training = []
    heightPad = 10
    generationTime = 0
    generationCount = 0
    widthPad = -20
    rectOffY = 90
    tileW = 6
    tileH = 4

    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, building, id):
        Structure.Structure.__init__(self, hp, mineralCost, generationTime, xini, yini, map, id, player)
        self.sprites = cargarSprites(ZERG_BUILDER_PATH, 4, False, BLUE, 1.8)
        self.building = building
        self.image = self.sprites[self.index]
        self.finalImage = self.sprites[3]

        self.count = 0
        self.paths = []
        
    def update(self):
        if len(self.training) > 0:
            self.generationCount += 1
            if self.generationCount == CLOCK_PER_SEC*self.training[0].generationTime:
                zergling = self.training[0]
                zerglingPos = zergling.getPosition()
                zerglingTile = self.map.getTile(zerglingPos[0], zerglingPos[1])
                if zerglingTile.type != 0:
                    vecinas = self.map.getTileVecinas(zerglingTile)
                    zergling.setTilePosition(vecinas[0])
                self.player.addUnits(zergling)
                self.generationCount = 0
                del self.training[0]
        self.index = (self.index + frame(8)) % 4
        self.image = self.sprites[self.index]
        self.image.set_colorkey(BLUE)

    def generateUnit(self, unit):
        self.training.append(unit)

    def execute(self, command_id):
        if self.clicked:
            if command_id == Command.CommandId.GENERAR_UNIDAD and self.player.resources >= ZERGLING_MINERAL_COST:
                self.player.resources -= ZERGLING_MINERAL_COST
                zergling = Zergling.Zergling(self.x / 40, (self.y + self.rectn.h) / 40, 1)
                self.generateUnit(zergling)
                
    def command(self, command):
        if command == Command.CommandId.BUILD_STRUCTURE:
            return Command.Command(Command.CommandId.BUILD_ZERG_BUILDER)
        elif command == Command.CommandId.GENERAR_UNIDAD:
            return Command.Command(Command.CommandId.GENERAR_UNIDAD)
        else:
            return Command.Command(Command.CommandId.NULO)
        
    def getBuildSprite(self):
        return self.sprites[3]
