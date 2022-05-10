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
    options = []

    def __init__(self, hp, mineralCost, generationTime, xini, yini, mapa, player, capacity):
        Entity.Entity.__init__(self, hp, xini*mapa.tw, yini*mapa.th, mineralCost, generationTime, takeID(), player)
        self.mapa = mapa
        self.player = player
        self.xIni = xini
        self.yIni = yini
        originX = (xini - self.CENTER_TILE[0])*self.mapa.tw
        originY = (yini - self.CENTER_TILE[1])*self.mapa.th
        self.rectn = pygame.Rect(originX, originY + self.heightPad/2, self.tileW*self.mapa.tw - 1, self.tileH*self.mapa.th - self.heightPad/2 - 1)
        self.esEstructura = True
        self.state = BuildingState.BUILDING
        self.lastAttacker = None
        self.capacity = capacity
        print("TENGO CAPACIDAD ", self.capacity, "Y SOY ", self.player, " Y ESTOY EN ", self.xIni, self.yIni)


    def __del__(self):
        print("fin")
        pass

    def getPosition(self):
        return (self.x, self.y)
    
    def getOptions(self):
        if self.state != BuildingState.BUILDING and self.state != BuildingState.COLLAPSING and self.state!= BuildingState.DESTROYED:
            return self.options
        else:
            return []

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
        #print("BUILDING ", self.x, " ", self.y)
        self.state = BuildingState.BUILDING
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.buildingFrames[self.frame]]]

    # Pasa a estado operative, es decir, disponible, on, preparado, etc.
    def changeToOperative(self):
        #print("OPERATIVE ", self.x, " ", self.y)
        self.state = BuildingState.OPERATIVE
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.operativeFrames[self.frame]]]

    # Pasa a estado lucecitas, para sacar unidades, si lo tiene claro
    def changeToSpawning(self):
        #print("SPAWNING ", self.x, " ", self.y)
        self.state = BuildingState.SPAWNING
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frame[self.spawningFrames[self.frame]]]

    # Pasa a empezar a derrumbarse, crashear, hp a 0 y esas cosas
    def changeToCollapsing(self):
        self.state = BuildingState.COLLAPSING
        self.count = 0
        self.index = 6
        #self.image = self.sprites[self.frames[self.collapsingFrames[self.frame]]]

    # Pasa a destruido del todo, no quedan ni los restos
    def changeToDestroyed(self):
        #print("DESTROYED ", self.x, " ", self.y)
        self.state = BuildingState.DESTROYED
        self.index = 0
        tiles = self.mapa.getRectTiles(self.getRect())
        for tile in tiles:
            self.mapa.setLibre(tile)
        self.clicked = False
        self.player.limitUnits -= self.capacity
        self.player.structures.remove(self)
        self.__del__()

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

    def getUnitCapacity(self):
        return self.capacity

    def updateOperative(self):
        if frame(self.frame) == 1:
            self.indexCount = (self.indexCount + 1) % len(self.operativeIndex)
            self.index = self.operativeIndex[self.indexCount]

    def updateBuilding(self):
        if self.nBuildSprites != 0:
            self.count += 1
            if self.count % (self.generationTime * CLOCK_PER_SEC / self.nBuildSprites) == 0:
                self.index += 1
            if self.index >= self.nBuildSprites:
                self.indexCount = 0
                self.count = 0
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
            if len(self.player.units) < self.player.limitUnits:
                unit = self.training[0]
                tile = self.mapa.getTile(self.x, self.y)

                libres = self.mapa.getEntityTilesVecinas(tile, unit.getTile())
                if len(libres) > 0:
                    unit.spawn(libres[0].centerx, libres[0].centery)
                    self.player.addUnits(unit)
                    self.generationCount = 0
                    del self.training[0]
                    if len(self.training) == 0:
                            self.state = BuildingState.OPERATIVE

    def updateCollapsing(self):
        #print("hola", self.frame)
        if frame(self.frame) == 1:
            self.index += 1
            if self.index == self.nSprites + 10:
                self.changeToDestroyed()



    def draw(self, screen, camera):
        r = self.getRect()
        image = self.getImage()
        if self.clicked:
            if self.player.isPlayer:
                pygame.draw.ellipse(screen, GREEN, [r.x - camera.x, r.y - camera.y, r.w, r.h], 2)
            else:
                pygame.draw.ellipse(screen, RED, [r.x - camera.x, r.y - camera.y, r.w, r.h], 2)
        if self.hp < self.maxHp:
            if self.player.isPlayer:
                hp = pygame.transform.chop(pygame.transform.scale(HP, (50, 8)), ((self.hp/self.maxHp) * 50, 0, 50, 0))
            else:
                hp = pygame.transform.chop(pygame.transform.scale(HP2, (50, 8)), ((self.hp/self.maxHp) * 50, 0, 50, 0))
            screen.blit(hp, [r.x + r.w/2 - camera.x - hp.get_rect().w/2, r.y + r.h - camera.y])


        #sombra
        aux = pygame.mask.from_surface(self.image, 0)
        mask = aux.to_surface(setcolor=(1, 0, 0))
        mask.set_colorkey(BLACK)
        mask.set_alpha(150)
        screen.blit(mask, [image.x - camera.x - 8, image.y - camera.y - 5])

        #self.image.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        screen.blit(self.image, [image.x - camera.x, image.y - camera.y])
        if DEBBUG:
            pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h),1)
            #pygame.draw.rect(screen, BLACK, pygame.Rect(image.x - camera.x, image.y - camera.y, image.w, image.h),1)

            tile = self.mapa.getTile(r.x + self.CENTER_TILE[0] * TILE_WIDTH, r.y + self.CENTER_TILE[1] * TILE_HEIGHT)
            #libres = self.mapa.getEntityTilesVecinas(tile)
            pygame.draw.rect(screen, BLACK, pygame.Rect(tile.x - camera.x, tile.y - camera.y, 40, 40), 5)
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
            if tile.type == EMPTY and tile.visible:
                pygame.draw.rect(screen, GREEN, pygame.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)
            else:
                pygame.draw.rect(screen, RED, pygame.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)

    def drawInfo(self, screen, color):
        dic = self.toDictionary(self.mapa)
        muestra_texto(screen, str('monotypecorsiva'), dic['nombre'], color, 25, [GUI_INFO_X2, GUI_INFO_Y2])
        if self.state == BuildingState.BUILDING:
            self.drawInfoBuilding(screen, color)
        elif self.state == BuildingState.OPERATIVE:
            self.drawInfoOperative(screen, color)
        elif self.state == BuildingState.SPAWNING:
            self.drawInfoSpawning(screen, color)

    def drawInfoBuilding(self, screen, color):
        muestra_texto(screen, str('monotypecorsiva'), "Construyendo...", color, 20, [GUI_INFO_X2, GUI_INFO_Y2 + 30])

        progreso = self.count / (self.generationTime * CLOCK_PER_SEC)
        if progreso > 1:
            progreso = 1
        pygame.draw.rect(screen, BLUE2, pygame.Rect(GUI_INFO_X2 - 75, GUI_INFO_Y2 + 55, 150*(progreso), 15))
        pygame.draw.rect(screen, BLUE, pygame.Rect(GUI_INFO_X2 - 75, GUI_INFO_Y2 + 55, 150, 15), 2)

    def drawInfoOperative(self, screen, color):
        dic = self.toDictionary(self.mapa)
        muestra_texto(screen, str('monotypecorsiva'), dic['funcion'], color, 20, [GUI_INFO_X2, GUI_INFO_Y2 + 50])

    def drawInfoSpawning(self, screen, color):
        #render de la tropa
        image = self.training[0].getRender()
        image = pygame.transform.scale(image, SPAW_UNIT_RENDER_SIZE)
        screen.blit(image, (GUI_INFO_X2 - 100, GUI_INFO_Y2 + 10))
        pygame.draw.rect(screen, GREEN, pygame.Rect(GUI_INFO_X2 - 95, GUI_INFO_Y2 + 15, 55, 60), 2)

        #progreso
        progreso = self.generationCount / (CLOCK_PER_SEC * self.training[0].generationTime)
        if progreso > 1:
            progreso = 1
        pygame.draw.rect(screen, BLUE2, pygame.Rect(GUI_INFO_X2 - 30, GUI_INFO_Y2 + 35, 130*(progreso), 10))
        pygame.draw.rect(screen, BLUE, pygame.Rect(GUI_INFO_X2 - 30, GUI_INFO_Y2 + 35, 130, 10), 2)

        #tropas pendientes
        pygame.draw.rect(screen, BLUE, pygame.Rect(GUI_INFO_X2 - 30, GUI_INFO_Y2 +60, 145, 55), 2)
        xPad = 0
        n = 0
        for unit in self.training[1:]:
            image = unit.getRender()
            image = pygame.transform.scale(image, WAIT_UNIT_RENDER_SIZE)
            screen.blit(image, (GUI_INFO_X2 - 30 + xPad, GUI_INFO_Y2 + 58))
            n += 1
            xPad += 45
            if n >= 3:
                break



    def checkTiles(self, visible = True):
        r = self.getRect()
        tiles = self.mapa.getRectTiles(r)
        ok = True
        tiles_set = set(tiles)
        if len(tiles_set) == self.tileH*self.tileW:
            for tile in tiles_set:
                if tile.type != EMPTY or (not tile.visible and visible):
                    ok = False
                    break
        else:
            ok = False
        return ok

    def buildProcess(self):
        pass

    def generateUnit(self, unit):
        #print("genero unidad")
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
                #print("ocupo", x, " ", y)
                self.mapa.setType(tile, STRUCTURE)
                tile.setOcupante(self)
                x += 1
            y += 1

    # Invocar para reflejar el damage de un ataque
    def beingAttacked(self, damage, unit):
        self.lastAttacker = unit
        if self.hp <= damage:
            self.hp -= damage
            self.changeToCollapsing()
        else:
            self.hp -= damage
        return self.hp

    def getCords(self):
        return self.x / TILE_WIDTH, self.y / TILE_HEIGHT

    def toDictionary(self, map):
        return {
            "x": self.xIni,
            "y": self.yIni,
            "hp": self.hp
        }
    def load(self, hp):
        self.hp = hp
