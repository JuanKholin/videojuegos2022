import pygame
from . import Structure, Terran
from .. import Player, Map, Utils

WHITE   = (255,255,255)

class TerranBuilder(Structure.Structure):
    sprites = []
    training = []
    rectOffY = 10
    index = 0
    generationTime = 0
    generationCount = 0
    x = 0
    y = 0
    clicked = False

    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, sprites,id):
        Structure.Structure.__init__(self, hp, mineralCost, generationTime,id)
        self.player = player
        for i in range(6): #0-3 construccion, 4 estado normal y 5 generando tropas
            self.sprites.insert(i,pygame.image.load(sprites + "/tile00" + str(i) + ".png"))
        self.x = xini
        self.y = yini
        self.map = map
        self.building = True 
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)
        self.rectn = pygame.Rect(xini, yini, self.sprites[4].get_width(), self.sprites[4].get_height()-self.rectOffY)
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
            self.count += 1
            if self.count == 20:
                self.count = 0
                if self.index == 5:
                    self.index = 4
                else:
                    self.index = 5
            self.generationCount += 1
            if self.generationCount == self.training[0].getGenerationTime():
                terran = self.training[0]
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
        rectAux = pygame.Rect(self.x - self.rectn.w/2, self.y - self.rectn.h/2, self.rectn.w, self.rectn.h)
        return rectAux

    def getImage(self):
        rect = self.image.get_rect()
        rectAux = pygame.Rect(self.x - (rect.w/2), self.y - (rect.h/2), rect.w, rect.h)
        return rectAux

    def setClicked(self, click):
        self.clicked = click

    def draw(self, screen):
        r = self.getRect()
        pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x, r.y+self.rectOffY, r.w, r.h),1)
        image = self.getImage()
        if self.clicked:
            pygame.draw.ellipse(screen, Utils.GREEN, [self.x-self.rectn.w/2, self.y+self.rectOffY-self.rectn.h/2, self.rectn.w, self.rectn.h], 2)
            screen.blit(self.image, [image.x, image.y])
        screen.blit(self.image, [image.x, image.y])

    def processEvent(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_v:
                terran = Terran.Terran(40, self.x, self.y+self.rectn.h, 20, 200, 2, 5, "terranSprites", 8, 6, 1)
                self.generateUnit(terran)