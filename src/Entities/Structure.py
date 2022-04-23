import pygame
from . import Entity
from .. import Player, Map, Utils

class Structure(Entity.Entity):
    x = 0
    y = 0
    clicked = False
    index = 0
    rectOffY = 0
    heightPad = 0

    def __init__(self, hp, mineralCost, generationTime, xini, yini, id,player):
        Entity.Entity.__init__(self, hp, xini, yini, mineralCost, generationTime, id,player)
    
    def getPosition(self):
        return (self.x+self.rectn.w/2, self.y+self.rectn.h/2)

    def update():
        pass
    
    def getRect(self):
        return self.rectn
        
    def getImage(self):
        rect = self.image.get_rect()
        rectAux = pygame.Rect(self.x, self.y - self.rectOffY - self.heightPad, rect.w, rect.h)
        return rectAux

    def setClicked(self, click):
        self.clicked = click
        
    def draw(self, screen, camera):
        r = self.getRect()
        pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h),1)
        image = self.getImage()
        if self.clicked:
            pygame.draw.ellipse(screen, Utils.GREEN, [self.x, self.y, r.w, r.h], 2)
            hp = pygame.transform.chop(pygame.transform.scale(Utils.HP, (50, 8)), ((self.hp/self.maxHp) * 50, 0, 50, 0))
            screen.blit(hp, [self.x + r.w/2 - camera.x - hp.get_rect().w/2, self.y + r.h - camera.y])
        screen.blit(self.image, [image.x - camera.x, image.y - camera.y])
            

