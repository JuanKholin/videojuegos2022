import pygame
from . import Structure, Terran
from .. import Player, Map

WHITE   = (255,255,255)
BLACK   = (0,0,0)
GREEN   = (0, 255, 0)

class TerranBuilder(Structure.Structure):
    sprites = []
    training = []
    rectOffY = 20
    index = 0
    generationTime = 0
    generationCount = 0
    x = 0
    y = 0
    frameCount = 0
    clicked = False

    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, sprites):
        Structure.Structure.__init__(self, hp, mineralCost, generationTime)
        self.player = player
        for i in range(6): #0-3 construccion, 4 estado normal y 5 generando tropas
            picture = pygame.image.load(sprites + "/tile00" + str(i) + ".png")
            picture = pygame.transform.scale(picture, (160, 150)) #!!!!!
            self.sprites.insert(i,picture)
            print("picture ", i, picture.get_width(), picture.get_height())
        self.x = xini
        self.y = yini
        self.map = map
        self.building = True 
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)
        self.rectn = pygame.Rect(self.x - 80, self.y - 60, 160, 120) #!!!!
    
        self.count = 0
    def update(self):
        if self.building:
            self.count += 1
            if self.count == 120:
                self.index += 1
                self.count = 0
                if self.index == 4:
                    self.building = False
        elif len(self.training) > 0:
            self.frameCount += 1
            if self.frameCount >= 10:
                self.index += 1
                if self.index >= 6:
                    self.index = 4
                self.frameCount = 0
            self.generationCount += 1
            if self.generationCount == self.training[0].getGenerationTime():
                terran = self.training[0]
                #terran.setPosition(self.x, self.y)
                #path = self.map.calcPath(self.x, self.y, self.x+50, self.y+50)
                #terran.addPath(path)
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
        rectAux = pygame.Rect(self.x - (self.rectn.w/2), self.y - (self.rectn.h/2), self.rectn.w, self.rectn.h)
        return rectAux

    def getImage(self):
        rectAux = pygame.Rect(self.x - (self.sprites[self.index].get_width()/2), self.y - (self.sprites[self.index].get_height()/2)-10, self.sprites[self.index].get_width(), self.sprites[self.index].get_height())
        return rectAux

    def setClicked(self, click):
        self.clicked = click
        if click:
            terran = Terran.Terran(40, self.x - 100, self.y + 80, 20, 200, 2, 5, "terranSprites", 0, 0)
            self.generateUnit(terran)

    def draw(self, screen):
        rect = self.getRect()
        image = self.getImage()
        #print(image.x,image.y)
        if self.clicked:
            pygame.draw.ellipse(screen, GREEN, pygame.Rect(rect.x, rect.y, rect.w, rect.h),3)
        pygame.draw.rect(screen, BLACK, pygame.Rect(rect.x, rect.y, rect.w, rect.h),1)
        screen.blit(self.image, [image.x, image.y])
