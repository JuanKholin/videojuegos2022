import pygame
from . import Structure, TerranWorker
from .. import Player, Map, Utils

class TerranBarracks(Structure.Structure):
    sprites = []
    training = []
    rectOffY = 10
    generationTime = 0
    generationCount = 0

    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, sprites, id):
        Structure.Structure.__init__(self, hp, mineralCost, generationTime, xini, yini, id)
        self.player = player
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
                if event.key == pygame.K_v:
                    terranWorker = TerranWorker.TerranWorker(self.x / 40, (self.y + self.rectn.h) / 40, 1)
                    self.generateUnit(terranWorker)

