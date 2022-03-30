import pygame
from . import Structure, Terran
from .. import Player, Map

WHITE   = (255,255,255)

class terranBuilder(Structure.Structure):
    sprites = []
    training = []
    rectOffY = 20
    index = 0
    generationTime = 0
    generationCount = 0
    x = 0
    y = 0

    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, sprites,id):
        Structure.Structure.__init__(self, hp, mineralCost, generationTime,id)
        self.player = player
        for i in range(5): #0-3 construccion, 4 estado normal y 5 generando tropas
            self.sprites.insert(i,pygame.image.load(sprites + "/tile00" + str(i) + ".png"))
        self.x = xini
        self.y = yini
        self.map = map
        self.building = True 
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)
        self.rectn = pygame.Rect(xini, yini, self.sprites[4].get_width(), self.sprites[4].get_height() - self.rectOffY)
        self.count = 0
        self.paths = []
    def update(self):
        if self.building:
            self.count += 1
            if self.count == 120:
                self.index += 1
                self.count = 0
                if self.index == 4:
                    self.building = False
        elif len(self.training) > 0:
            self.index = 5
            self.generationCount += 1
            if self.generationCount == self.training[0].getGenerationTime():
                self.training -= 1
                terran = self.training[0]
                terran.setPosition(self.x, self.y)
                path = self.map.calcPath(self.x, self.y, self.x+50, self.y+50)
                terran.addPath(path)
                self.player.addUnits(terran)
                self.generationCount = 0
                del self.training[0]
        else:
            self.index = 4
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)
        
    def generateUnit(self, unit):
        self.training.append(unit)

    def getRect(self):
        rectAux = pygame.Rect(self.rectn.x - self.rectn.w/2, self.rectn.y - self.rectn.h, self.rectn.w, self.rectn.h)
        return rectAux