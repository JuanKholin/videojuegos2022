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
    count = 0
    indexCount = 0

    def __init__(self, hp, mineralCost, generationTime, xini, yini, mapa, id, player):
        Entity.Entity.__init__(self, hp, xini*mapa.tw, yini*mapa.th, mineralCost, generationTime, id, player)
        self.mapa = mapa
        self.player = player
        self.xIni = xini
        self.yIni = yini
        originX = (xini - round(self.tileW/2))*self.mapa.tw
        originY = (yini - round(self.tileH/2))*self.mapa.th
        self.rectn = pygame.Rect(originX, originY + self.heightPad/2, self.tileW*self.mapa.tw - 1, self.tileH*self.mapa.th - self.heightPad/2 - 1)
        
        self.state = BuildingState.BUILDING

    def getPosition(self):
        return (self.x+self.rectn.w/2, self.y+self.rectn.h/2)

    def update(self):
        if self.state == BuildingState.BUILDING:
            self.updateBuilding()
        elif self.state == BuildingState.OPERATIVE:
            self.updateOperative()
        elif self.state == BuildingState.SPAWNING:
            self.updateSpawning()
        elif self.state == BuildingState.COLLAPSING:
            self.updateCollapsing()
        elif self.state == BuildingState.DESTROYED:
            pass
        self.image = self.sprites[self.index]


    ################
    # TRANSICIONES #
    ################

    # Pasa a estado construyendo, si lo hay
    def changeToBuilding(self):
        print("BUILDING ", self.x, " ", self.y)
        self.state = BuildingState.BUILDING
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.buildingFrames[self.frame]]]
        
    # Pasa a estado operative, es decir, disponible, on, preparado, etc.
    def changeToOperative(self):
        print("OPERATIVE ", self.x, " ", self.y)
        self.state = BuildingState.OPERATIVE
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.operativeFrames[self.frame]]]
        
    # Pasa a estado lucecitas, para sacar unidades, si lo tiene claro
    def changeToSpawning(self):        
        print("SPAWNING ", self.x, " ", self.y)
        self.state = BuildingState.SPAWNING
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.spawningFrames[self.frame]]]

    # Pasa a empezar a derrumbarse, crashear, hp a 0 y esas cosas
    def changeToCollapsing(self):
        print("COLLAPSING ", self.x, " ", self.y)
        self.state = BuildingState.COLLAPSING
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.collapsingFrames[self.frame]]]
    
    # Pasa a destruido del todo, no quedan ni los restos
    def changeToDestroyed(self):
        print("DESTROYED ", self.x, " ", self.y)
        self.state = BuildingState.DESTROYED
        self.mapa.setLibre(self.getTile())
        self.clicked = False

    def getOptions(self):
        return []

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
        self.x = xTile * self.mapa.tw
        self.y = yTile * self.mapa.th
        self.rectn.x = originX
        self.rectn.y = originY + self.heightPad/2
        self.rectn.w = self.tileW*self.mapa.tw - 1
        self.rectn.h = self.tileH*self.mapa.th - self.heightPad/2 - 1
    
    def execute(self, command_id):
        pass
    
    def updateOperative(self):
        if frame(self.frame) == 1:
            self.indexCount = (self.indexCount + 1) % len(self.operativeIndex)
            self.index = self.operativeIndex[self.indexCount]

    def updateBuilding(self):
        if self.nBuildSprites != 0:
            self.count += 1
            if self.count >= self.generationTime * CLOCK_PER_SEC / self.nBuildSprites:
                self.index += 1
                self.count = 0
            if self.index >= self.nBuildSprites:
                self.indexCount = 0
                self.state = BuildingState.OPERATIVE
        else:
            self.indexCount = 0
            self.state = BuildingState.OPERATIVE

    def updateSpawning(self):
        self.generationCount += 1
        if frame(self.frame) == 1: 
            self.indexCount = (self.indexCount + 1) % len(self.spawningIndex) 
            self.index = self.spawningIndex[self.indexCount]
        if self.generationCount >= CLOCK_PER_SEC * self.training[0].generationTime:
            unit = self.training[0]
            tile = self.mapa.getTile(self.x, self.y)
            
            libres = self.mapa.getEntityTilesVecinas(tile, unit.getTile())
            if len(libres) > 0:
                unit.x = libres[0].centerx
                unit.y = libres[0].centery

                self.player.addUnits(unit)
                self.generationCount = 0
                del self.training[0]
                if len(self.training) == 0:
                    self.state = BuildingState.OPERATIVE
                    
    def updateCollapsing(self):
        pass

    def draw(self, screen, camera):
        r = self.getRect()
        image = self.getImage()
        if self.clicked:
            if self.player.isPlayer:
                pygame.draw.ellipse(screen, GREEN, [r.x - camera.x, r.y - camera.y, r.w, r.h], 2)
                hp = pygame.transform.chop(pygame.transform.scale(HP, (50, 8)), ((self.hp/self.maxHp) * 50, 0, 50, 0))
            else:
                pygame.draw.ellipse(screen, RED, [r.x - camera.x, r.y - camera.y, r.w, r.h], 2)
                hp = pygame.transform.chop(pygame.transform.scale(HP2, (50, 8)), ((self.hp/self.maxHp) * 50, 0, 50, 0))
            screen.blit(hp, [r.x + r.w/2 - camera.x - hp.get_rect().w/2, r.y + r.h - camera.y])
        screen.blit(self.image, [image.x - camera.x, image.y - camera.y])
        if DEBBUG:
            pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h),1)
            #pygame.draw.rect(screen, BLACK, pygame.Rect(image.x - camera.x, image.y - camera.y, image.w, image.h),1)
            
            tile = self.mapa.getTile(r.x + r.w/2, r.y + r.h/2)
            #libres = self.mapa.getEntityTilesVecinas(tile)
            pygame.draw.rect(screen, BLACK, pygame.Rect(tile.x - camera.x, tile.y - camera.y, 40, 40),5)
            #for tile in libres:
             #   pygame.draw.rect(screen, PINK, pygame.Rect(tile.x - camera.x, tile.y - camera.y, tile.w, tile.h),1)

    def drawBuildStructure(self, screen, camera):
        r = self.getRect()
        #pygame.draw.rect(screen, GREEN, pygame.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h), 5)
        tiles = self.mapa.getRectTiles(r)
        self.drawBuildTiles(screen, camera, tiles)

        sprite = self.getBuildSprite()
        image = self.getFinalImage()
        screen.blit(sprite, (image.x - camera.x, image.y - camera.y))
        
    def drawBuildTiles(self, screen, camera, tiles):
        for tile in tiles:
            r = tile.getRect()
            if tile.type == EMPTY:
                pygame.draw.rect(screen, GREEN, pygame.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)
            else:
                pygame.draw.rect(screen, RED, pygame.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)

    def checkTiles(self):
        r = self.getRect()
        tiles = self.mapa.getRectTiles(r)
        ok = True
        tiles_set = set(tiles)
        if len(tiles_set) == self.tileH*self.tileW:
            for tile in tiles_set:
                if tile.type != EMPTY:
                    ok = False
                    break
        else:
            ok = False
        return ok
    
    def buildProcess(self):
        pass

    def generateUnit(self, unit):
        print("genero unidad")
        if len(self.training) == 0:
            self.generationStartTime = getGlobalTime()
        self.training.append(unit)

    def command(self, command):
        return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[0]

    def getOrder(self):
        return CommandId.NULL
    
    def getPlayer(self):
        return self.player

    def setTilesOcupados(self):
        rect = self.getRect()
        x, y = self.mapa.getTileIndex(rect.x, rect.y)
        while y*self.mapa.th <= rect.y+rect.h:
            x, _ = self.mapa.getTileIndex(rect.x, rect.y)
            while x*self.mapa.tw <= rect.x+rect.w:
                tile = self.mapa.mapa[y][x]
                self.mapa.setType(tile, STRUCTURE)
                tile.setOcupante(self)
                x += 1
            y += 1

    # Invocar para reflejar el damage de un ataque
    def beingAttacked(self, damage, unit):
        if self.hp <= damage:
            self.changeToCollapsing()
        else:
            self.hp -= damage
        return self.hp
