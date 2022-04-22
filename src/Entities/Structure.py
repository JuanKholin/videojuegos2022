import pygame
from . import Entity
from .. import Player, Map, Utils

class Structure(Entity.Entity):
    x = 0
    y = 0
    clicked = False
    index = 0
    rectOffY = 0

    def __init__(self, hp, mineralCost, generationTime, xini, yini, id,player):
        Entity.Entity.__init__(self, hp, xini, yini, mineralCost, generationTime, id,player)
    
    def getPosition(self):
        return (self.rectn.x, self.rectn.y)

    def update():
        pass
    
    def draw(self, screen):
        r = self.getRect()
        pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x, r.y+self.rectOffY, r.w, r.h),1)
        image = self.getImage()
        if self.clicked:
            pygame.draw.ellipse(screen, Utils.GREEN, [self.x-self.rectn.w/2, self.y+self.rectOffY-self.rectn.h/2, self.rectn.w, self.rectn.h], 2)
        screen.blit(self.image, [image.x, image.y])
        hp = Utils.HP
        hp = pygame.transform.scale(hp, (200, 100))
        screen.blit(hp, [image.x, image.y])
    
    def getRect(self):
        rectAux = pygame.Rect(self.x - self.rectn.w/2, self.y - self.rectn.h/2 + self.rectOffY, self.rectn.w, self.rectn.h)
        return rectAux
        
    def getImage(self):
        rect = self.image.get_rect()
        rectAux = pygame.Rect(self.x - (rect.w/2), self.y - (rect.h/2), rect.w, rect.h)
        return rectAux

    def setClicked(self, click):
        self.clicked = click
