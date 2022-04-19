import pygame
from . import Structure, TerranWorker
from .. import Player, Map, Utils

class TerranBarracks(Structure.Structure):
    sprites = []
    training = []
    rectOffY = 10
    generationTime = 0
    generationCount = 0

    def __init__(self, hp, mineralCost, generationTime, xini, yini, map, sprites, id,player):
        Structure.Structure.__init__(self, hp, mineralCost, generationTime, xini, yini, id,player)
        for i in range(6): #0-3 construccion, 4 estado normal y 5 generando tropas
            self.sprites.insert(i, pygame.image.load(sprites + "/tile00" + str(i) + ".png"))
        self.map = map
        self.building = True 
        self.image = self.sprites[self.index]
        self.image.set_colorkey(Utils.WHITE)
        self.rectn = pygame.Rect(xini, yini, self.sprites[4].get_width(), self.sprites[4].get_height() - self.rectOffY)
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
            if self.generationCount == Utils.CLOCK_PER_SEC * self.training[0].generationTime:
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
        self.image.set_colorkey(Utils.WHITE)
        
    def generateUnit(self, unit):
        self.training.append(unit)

    def processEvent(self, event):
        if self.clicked:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_v and self.player.resources >= Utils.TERRAN_WORKER_MINERAL_COST:
                    self.player.resources -= Utils.TERRAN_WORKER_MINERAL_COST
                    terranWorker = TerranWorker.TerranWorker(self.x / 40, (self.y + self.rectn.h) / 40, 1)
                    self.generateUnit(terranWorker)

