import pygame
from . import Entity
from .. import Player, Map
from ..Command import *
from ..Utils import *

class Structure(Entity.Entity):
    clicked = False
    index = 0
    rectOffY = 0
    heightPad = 0
    widthPad = 0
    tileW = 0
    tileH = 0
    training = []
    nBuildSprites = 1

    def __init__(self, hp, mineralCost, generationTime, xini, yini, mapa, id, player):
        Entity.Entity.__init__(self, hp, xini*mapa.tw, yini*mapa.th, mineralCost, generationTime, id, player)
        self.mapa = mapa
        self.player = player
        self.xIni = xini
        self.yIni = yini
        originX = (xini - round(self.tileW/2))*self.mapa.tw
        originY = (yini - round(self.tileH/2))*self.mapa.th
        self.rectn = pygame.Rect(originX, originY + self.heightPad/2, self.tileW*self.mapa.tw - 1, self.tileH*self.mapa.th - self.heightPad/2 - 1)

    def getPosition(self):
        return (self.x+self.rectn.w/2, self.y+self.rectn.h/2)

    def update(self):
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
        xTile, yTile = self.mapa.getTileIndex(x, y)
        originX = (xTile - round(self.tileW/2))*self.mapa.tw
        originY = (yTile - round(self.tileH/2))*self.mapa.th
        self.rectn.x = originX
        self.rectn.y = originY + self.heightPad/2
        self.rectn.w = self.tileW*self.mapa.tw - 1
        self.rectn.h = self.tileH*self.mapa.th - self.heightPad/2 - 1

    def update(self):
        pass

    def updateBuilding(self, nBuildSprites):
        if nBuildSprites != 0:
            self.count += 1
            if self.count >= self.generationTime*CLOCK_PER_SEC / nBuildSprites:
                self.index += 1
                self.count = 0
            if self.index == 4:
                self.building = False
        else:
            self.building = False

    def updateTraining(self):
        self.generationCount += 1
        if self.generationCount >= CLOCK_PER_SEC * self.training[0].generationTime:
        #if (getGlobalTime() - self.generationStartTime) > self.training[0].generationTime:
            unit = self.training[0]
            tile = self.mapa.getTile(self.x, self.y)
            libres = self.mapa.getEntityTilesVecinas(tile)
            if len(libres) > 0:
                #unit.setTilePosition(libres[0])
                
                unit.x = libres[0].centerx
                unit.y = libres[0].centery - self.mapa.th
                print(unit.x, unit.y)

                #libres[0].setOcupada(1)

                self.player.addUnits(unit)
                self.generationCount = 0
                del self.training[0]
                self.generationStartTime = getGlobalTime()

    def draw(self, screen, camera):
        r = self.getRect()
        image = self.getImage()
        if self.clicked:
            pygame.draw.ellipse(screen, GREEN, [r.x - camera.x, r.y - camera.y, r.w, r.h], 2)
            hp = pygame.transform.chop(pygame.transform.scale(HP, (50, 8)), ((self.hp/self.maxHp) * 50, 0, 50, 0))
            screen.blit(hp, [r.x + r.w/2 - camera.x - hp.get_rect().w/2, r.y + r.h - camera.y])
        screen.blit(self.image, [image.x - camera.x, image.y - camera.y])
        if DEBBUG:
            pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h),1)
            pygame.draw.rect(screen, BLACK, pygame.Rect(image.x - camera.x, image.y - camera.y, image.w, image.h),1)
            
            tile = self.mapa.getTile(r.x + r.w/2, r.y + r.h/2)
            libres = self.mapa.getEntityTilesVecinas(tile)
            pygame.draw.rect(screen, BLACK, pygame.Rect(tile.x - camera.x, tile.y - camera.y, 40, 40),5)
            for tile in libres:
                pygame.draw.rect(screen, PINK, pygame.Rect(tile.x - camera.x, tile.y - camera.y, tile.w, tile.h),1)

    def drawBuildStructure(self, screen, camera):
        r = self.getRect()
        #pygame.draw.rect(screen, GREEN, pygame.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h), 5)
        tiles = self.mapa.getRectTiles(r)
        self.mapa.drawTiles(screen, camera, tiles)

        sprite = self.getBuildSprite()
        image = self.getFinalImage()
        screen.blit(sprite, (image.x - camera.x, image.y - camera.y))

    def checkTiles(self):
        r = self.getRect()
        tiles = self.mapa.getRectTiles(r)
        ok = True
        tiles_set = set(tiles)
        if len(tiles_set) == self.tileH*self.tileW:
            for tile in tiles_set:
                if tile.type != 0:
                    ok = False
                    break
        else:
            ok = False
        return ok

    def generateUnit(self, unit):
        print("genero unidad")
        if len(self.training) == 0:
            self.generationStartTime = getGlobalTime()
        self.training.append(unit)

    def command(self, command):
        return Command(CommandId.NULO)

    def getBuildSprite(self):
        return self.sprites[0]

    def getOrder(self):
        return CommandId.NULO

    def setTilesOcupados(self):
        rect = self.getRect()
        x, y = self.mapa.getTileIndex(rect.x, rect.y)
        while y*self.mapa.th <= rect.y+rect.h:
            x, _ = self.mapa.getTileIndex(rect.x, rect.y)
            while x*self.mapa.tw <= rect.x+rect.w:
                tile = self.mapa.mapa[y][x]
                self.mapa.setVecina(tile, self.id)
                tile.setOcupante(self)
                x += 1
            y += 1
