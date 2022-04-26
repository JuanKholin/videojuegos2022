import pygame
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *

class TerranBarracks(Structure):
    sprites = []
    training = []
    generationTime = 0
    generationCount = 0
    heightPad = 20
    widthPad = 19
    rectOffY = 8

    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, building):
        (x, y) = map.getTileCenter(xini, yini)
        x -= 19
        y -= 13
        Structure.__init__(self, hp, mineralCost, generationTime, x, y, takeID(), player)
        self.player = player
        self.sprites = cargarSprites(TERRAN_BARRACK_PATH, 6, False, WHITE, 1.1)
        self.map = map
        self.building = building
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)
        self.rectn = pygame.Rect(x, y, self.sprites[4].get_width() + self.widthPad, self.sprites[4].get_height()-self.heightPad)
        self.count = 0
        self.paths = []

    def update(self):
        if self.building:
            self.count += 1
            if self.count == self.generationTime / 10:
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
                    terranPos = terran.getPosition()
                    print("tp", terranPos)
                    self.map.addOre(terranPos[0], terranPos[1])
                    print("vecina ", vecinas[0].centerx, vecinas[0].centery, vecinas[0].type)
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
            if command_id == CommandId.GENERAR_UNIDAD  and self.player.resources >= TERRAN_WORKER_MINERAL_COST:
                self.player.resources -= TERRAN_WORKER_MINERAL_COST
                terranWorker = TerranWorker(self.x / 40, (self.y + self.rectn.h) / 40, self.player)
                self.generateUnit(terranWorker)

