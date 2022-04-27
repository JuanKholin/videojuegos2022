import pygame
from . import Entity
from .. import Player, Map, Utils, Command

class Structure(Entity.Entity):
    x = 0
    y = 0
    clicked = False
    index = 0
    rectOffY = 0
    heightPad = 0
    widthPad = 0
    tileW = 0
    tileH = 0

    def __init__(self, hp, mineralCost, generationTime, xini, yini, map, id, player):
        Entity.Entity.__init__(self, hp, xini, yini, mineralCost, generationTime, id, player)
        self.map = map
        self.player = player
        
        originX = (xini - round(self.tileW/2))*self.map.tw
        originY = (yini - round(self.tileH/2))*self.map.th
        self.rectn = pygame.Rect(originX, originY + self.heightPad/2, self.tileW*self.map.tw - 1, self.tileH*self.map.th - self.heightPad/2 - 1)
    
    def getPosition(self):
        return (self.x+self.rectn.w/2, self.y+self.rectn.h/2)

    def update():
        pass
    
    def getRect(self):
        return self.rectn
        
    def getImage(self):
        image = self.image.get_rect()
        r = self.getRect()
        rectAux = pygame.Rect(r.x + r.w/2 - image.w/2, r.y - self.heightPad - self.rectOffY, image.w, image.h)
        return rectAux
    
    def getFinalImage(self):
        image = self.finalImage.get_rect()
        r = self.getRect()
        rectAux = pygame.Rect(r.x + r.w/2 - image.w/2, r.y - self.heightPad - self.rectOffY, image.w, image.h)
        return rectAux

    def setClicked(self, click):
        self.clicked = click
        
    def setPosition(self, x, y):
        xTile, yTile = self.map.getTileIndex(x, y)
        originX = (xTile - round(self.tileW/2))*self.map.tw
        originY = (yTile - round(self.tileH/2))*self.map.th
        self.rectn.x = originX
        self.rectn.y = originY + self.heightPad/2
        self.rectn.w = self.tileW*self.map.tw - 1
        self.rectn.h = self.tileH*self.map.th - self.heightPad/2 - 1
        
    def draw(self, screen, camera):
        r = self.getRect()
        image = self.getImage()
        if self.clicked:
            pygame.draw.ellipse(screen, Utils.GREEN, [r.x - camera.x, r.y - camera.y, r.w, r.h], 2)
            hp = pygame.transform.chop(pygame.transform.scale(Utils.HP, (50, 8)), ((self.hp/self.maxHp) * 50, 0, 50, 0))
            screen.blit(hp, [r.x + r.w/2 - camera.x - hp.get_rect().w/2, r.y + r.h - camera.y])
        screen.blit(self.image, [image.x - camera.x, image.y - camera.y])
        if Utils.DEBBUG:
            pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h),1)
            pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(image.x - camera.x, image.y - camera.y, image.w, image.h),1)
            
    def drawBuildStructure(self, screen, camera):
        r = self.getRect()
        #pygame.draw.rect(screen, Utils.GREEN, pygame.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h), 5)
        tiles = self.map.getRectTiles(r)
        self.map.drawTiles(screen, camera, tiles)
        
        sprite = self.getBuildSprite()
        image = self.getFinalImage()
        screen.blit(sprite, (image.x - camera.x, image.y - camera.y))
        
    def checkTiles(self):
        r = self.getRect()
        tiles = self.map.getRectTiles(r)
        ok = True
        for tile in tiles:
            if tile.type != 0:
                ok = False
                break
        return ok
            
    def command(self, command):
        return Command.Command(Command.CommandId.NULO)
    
    def getBuildSprite(self):
        return self.sprites[0]
        
