import pygame
from . import Structure, TerranWorker
from .. import Player, Map, Utils, Tile, Command
from src.Utils import *

WHITE   = (255,255,255)

class TerranBuilder(Structure.Structure):
    sprites = []
    training = []
    rectOffY = 0
    generationTime = 0
    generationCount = 0
    rectOffY = 20

    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, building,id):
        (x, y) = map.getTileCenter(xini, yini)
        x -= 18
        y -= 16
        Structure.Structure.__init__(self, hp, mineralCost, generationTime, x, y, id, player)
        self.player = player

        self.sprites = cargarSprites(TERRAN_BUILDER_PATH, 6, False, WHITE, 1.5)
        self.map = map
        self.building = building
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)
        self.rectn = pygame.Rect(x, y, self.sprites[4].get_width(), (self.sprites[4].get_height()-self.rectOffY))
        self.count = 0
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
            if self.generationCount == Utils.CLOCK_PER_SEC*self.training[0].generationTime:
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
        
    def execute(self, command_id):
        if self.clicked:
            if command_id == Command.CommandId.GENERAR_UNIDAD and self.player.resources >= Utils.TERRAN_WORKER_MINERAL_COST:
                self.player.resources -= Utils.TERRAN_WORKER_MINERAL_COST
                terranWorker = TerranWorker.TerranWorker(self.x / 40, (self.y + self.rectn.h) / 40, self.player)
                self.generateUnit(terranWorker)
