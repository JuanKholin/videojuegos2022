import pygame
from . import Structure, Zergling
from .. import Player, Map, Utils, Tile
from src.Utils import *

WHITE   = (255,255,255)

class ZergBuilder(Structure.Structure):
    sprites = []
    training = []
    rectOffY = 50
    heightPad = 50
    generationTime = 0
    generationCount = 0

    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, building, id):
        Structure.Structure.__init__(self, hp, mineralCost, generationTime, xini, yini, id, player)
        self.player = player
        
        self.sprites = cargarSprites(ZERG_BUILDER_PATH, 4, False, BLUE, 2)
        
        self.map = map
        self.building = building 
        self.image = self.sprites[self.index]
        self.image.set_colorkey(BLUE)
        self.rectn = pygame.Rect(xini, yini+self.rectOffY, self.sprites[0].get_width(), self.sprites[0].get_height()-self.rectOffY)
        self.count = 0
        self.paths = []
    def update(self):
        if len(self.training) > 0:
            self.generationCount += 1
            if self.generationCount == CLOCK_PER_SEC*self.training[0].generationTime:
                zergling = self.training[0]
                zerglingPos = zergling .getPosition()
                zerglingTile = self.map.getTile(zerglingPos[0], zerglingPos[1])
                if zerglingTile.type != 0:
                    vecinas = self.map.getTileVecinas(zerglingTile)
                    zergling.setTilePosition(vecinas[0]) 
                self.player.addUnits(zergling)
                self.generationCount = 0
                del self.training[0]
        self.index = (self.index + frame(8)) % 4
        self.image = self.sprites[self.index]
        self.image.set_colorkey(BLUE)
        
    def generateUnit(self, unit):
        self.training.append(unit)

    def getRect(self):
        print("me llaman")
        rectAux = pygame.Rect(self.x - self.rectn.w/2, self.y - self.rectn.h/2 + self.rectOffY, self.rectn.w, self.rectn.h - self.heightPad)
        return rectAux

    def getImage(self):
        rect = self.image.get_rect()
        rectAux = pygame.Rect(self.x - (rect.w/2), self.y - (rect.h/2), rect.w, rect.h)
        return rectAux

    def setClicked(self, click):
        self.clicked = click

    def draw(self, screen, camera):
        r = self.getRect()
        pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h),1)
        image = self.getImage()
        if self.clicked:
            pygame.draw.ellipse(screen, Utils.GREEN, [self.x- r.w/2 - camera.x + 15, self.y+self.rectOffY-r.h/2+10 - camera.y + 30, r.w - 25, r.h - 30], 2)
        screen.blit(self.image, [image.x - camera.x, image.y - camera.y])
        hp = Utils.HP
        hp = pygame.transform.scale(hp, (50, 8))
        hp = pygame.transform.chop(hp, ((self.hp/self.maxHp) * 50, 0, 50, 0))
        screen.blit(hp, [self.x - camera.x - 25, self.y+self.rectOffY+self.rectn.h/2 - 30 - camera.y])

    def processEvent(self, event):
        if self.clicked:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_v and self.player.resources >= ZERGLING_MINERAL_COST:
                    self.player.resources -= ZERGLING_MINERAL_COST
                    zergling = Zergling.Zergling(self.x / 40, (self.y + self.rectn.h) / 40, 1)
                    self.generateUnit(zergling)

