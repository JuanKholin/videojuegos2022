import pygame as pg
from . import Entity
from .. import Player, Map
from ..Command import *
from ..Camera import *
from ..Utils import *
from ..Music import *
from ..Lib import *

class Structure(Entity.Entity):
    clicked = False
    index = 0
    rectOffY = 0
    HEIGHT_PAD = 0
    widthPad = 0
    training = []
    nBuildSprites = 1
    count = 0
    indexCount = 0
    options = []
    generateSound = soldierGenerateSound
    deadSound = terranStructureDead
    selectedSound = structureSelectedSound

    def __init__(self, hp, mineralCost, generationTime, xini, yini, mapa, player, capacity):
        Entity.Entity.__init__(self, hp, xini*mapa.tw, yini*mapa.th, mineralCost, generationTime, takeID(), player)
        self.mapa = mapa
        self.player = player
        self.xIni = xini
        self.yIni = yini
        originX = (xini - self.CENTER_TILE[0])*self.mapa.tw
        originY = (yini - self.CENTER_TILE[1])*self.mapa.th
        self.rectn = pg.Rect(originX, originY + self.HEIGHT_PAD/2, self.TILES_WIDTH*self.mapa.tw - 1, self.TILES_HEIGHT*self.mapa.th - self.HEIGHT_PAD/2 - 1)
        self.esEstructura = True
        self.state = BuildingState.BUILDING
        self.lastAttacker = None
        self.capacity = capacity
        #print("TENGO CAPACIDAD ", self.capacity, "Y SOY ", self.player, " Y ESTOY EN ", self.xIni, self.yIni)


    def __del__(self):
        #print("fin")
        pass

    def getPosition(self):
        return (self.x, self.y)

    def getType(self):
        return -1
    
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
        if len(self.shadows) > 0:
            self.shadow = self.shadows[self.index]



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
        self.shadow = self.shadows[self.frames[self.buildingFrames[self.frame]]]

    # Pasa a estado operative, es decir, disponible, on, preparado, etc.
    def changeToOperative(self):
        #print("OPERATIVE ", self.x, " ", self.y)
        self.state = BuildingState.OPERATIVE
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.operativeFrames[self.frame]]]
        self.shadow = self.shadows[self.frames[self.operativeFrames[self.frame]]]

    # Pasa a estado lucecitas, para sacar unidades, si lo tiene claro
    def changeToSpawning(self):
        #print("SPAWNING ", self.x, " ", self.y)
        self.state = BuildingState.SPAWNING
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frame[self.spawningFrames[self.frame]]]
        self.shadow = self.shadows[self.frame[self.spawningFrames[self.frame]]]

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
        if self.player.base == self:
            if self.player.isPlayer:
                setGameState2(System_State.GAMEOVER)
            else:
                setGameState2(System_State.WIN)
        self.player.structures.remove(self)
        self.__del__()

    def getRect(self):
        return self.rectn

    def getImage(self):
        image = self.image.get_rect()
        r = self.getRect()
        rectAux = pg.Rect(r.x + r.w/2 - image.w/2 - self.widthPad, r.y - self.HEIGHT_PAD - self.rectOffY, image.w, image.h)
        return rectAux

    def getFinalImage(self):
        image = self.finalImage.get_rect()
        r = self.getRect()
        rectAux = pg.Rect(r.x + r.w/2 - image.w/2 - self.widthPad, r.y - self.HEIGHT_PAD - self.rectOffY, image.w, image.h)
        return rectAux

    def setClicked(self, click):
        self.clicked = click

    def setPosition(self, x, y):
        xTile, yTile = self.mapa.getTileIndex(x, y)
        originX = (xTile - round(self.TILES_WIDTH/2))*self.mapa.tw
        originY = (yTile - round(self.TILES_HEIGHT/2))*self.mapa.th
        self.x = xTile * self.mapa.tw
        self.y = yTile * self.mapa.th
        self.rectn.x = originX
        self.rectn.y = originY + self.HEIGHT_PAD/2
        self.rectn.w = self.TILES_WIDTH*self.mapa.tw - 1
        self.rectn.h = self.TILES_HEIGHT*self.mapa.th - self.HEIGHT_PAD/2 - 1

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

                libres = self.mapa.getEntityTilesVecinas(tile, tile)
                if len(libres) > 0:
                    unit.spawn(int(libres[0].centerx/TILE_WIDTH), int(libres[0].centery/TILE_HEIGHT))
                    self.player.addUnits(unit)
                    if inCamera([libres[0].centerx, libres[0].centery]):
                        playSound(unit.generateSound)
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
        if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
            r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
            image = self.getImage()
            if self.clicked:
                if self.player.isPlayer:
                    pg.draw.ellipse(screen, GREEN, [r.x - camera.x, r.y - camera.y, r.w, r.h], 2)
                else:
                    pg.draw.ellipse(screen, RED, [r.x - camera.x, r.y - camera.y, r.w, r.h], 2)
            if self.hp < self.maxHp:
                if self.player.isPlayer:
                    hp = pg.transform.chop(pg.transform.scale(HP, (50, 8)), ((self.hp/self.maxHp) * 50, 0, 50, 0))
                else:
                    hp = pg.transform.chop(pg.transform.scale(HP2, (50, 8)), ((self.hp/self.maxHp) * 50, 0, 50, 0))
                screen.blit(hp, [r.x + r.w/2 - camera.x - hp.get_rect().w/2, r.y + r.h - camera.y])


            #sombra

            #self.image.blit(dark, (0, 0), special_flags=pg.BLEND_RGBA_SUB)
            if len(self.shadows) > 0:
                screen.blit(self.shadow, [image.x - camera.x - 10, image.y - camera.y - 10])
            screen.blit(self.image, [image.x - camera.x, image.y - camera.y])
            if DEBBUG:
                pg.draw.rect(screen, BLACK, pg.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h),1)
                #pg.draw.rect(screen, BLACK, pg.Rect(image.x - camera.x, image.y - camera.y, image.w, image.h),1)

                tile = self.mapa.getTile(r.x + self.CENTER_TILE[0] * TILE_WIDTH, r.y + self.CENTER_TILE[1] * TILE_HEIGHT)
                libres = self.mapa.getEntityTilesVecinas(tile, tile)
                pg.draw.rect(screen, BLACK, pg.Rect(tile.x - camera.x, tile.y - camera.y, 40, 40), 5)
                for tile in libres:
                    pg.draw.rect(screen, PINK, pg.Rect(tile.x - camera.x, tile.y - camera.y, tile.w, tile.h),1)

    def drawBuildStructure(self, screen, camera):
        r = self.getRect()
        #pg.draw.rect(screen, GREEN, pg.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h), 5)
        tiles = self.mapa.getRectTiles(r)
        self.drawBuildTiles(screen, camera, tiles)

        sprite = self.getBuildSprite()
        image = self.getFinalImage()
        screen.blit(sprite, (image.x - camera.x, image.y - camera.y))

    def drawBuildTiles(self, screen, camera, tiles):
        for tile in tiles:
            r = tile.getRect()
            if tile.type == EMPTY and tile.visible:
                pg.draw.rect(screen, GREEN, pg.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)
            else:
                pg.draw.rect(screen, RED, pg.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)

    def drawInfo(self, screen, color):
        dic = self.toDictionary(self.mapa)
        muestra_texto(screen, str('monotypecorsiva'), dic['nombre'], color, 25, [Utils.ScreenWidth/2 - GUI_INFO_X2 + 80, Utils.ScreenHeight - GUI_INFO_Y2 + 10], True)
        if self.state == BuildingState.BUILDING:
            self.drawInfoBuilding(screen, color)
        elif self.state == BuildingState.OPERATIVE:
            self.drawInfoOperative(screen, color)
        elif self.state == BuildingState.SPAWNING:
            self.drawInfoSpawning(screen, color)

    def drawInfoBuilding(self, screen, color):
        muestra_texto(screen, str('monotypecorsiva'), "Construyendo...", color, 20, [Utils.ScreenWidth/2 - GUI_INFO_X2, Utils.ScreenHeight - GUI_INFO_Y2 + 50])

        progreso = self.count / (self.generationTime * CLOCK_PER_SEC)
        if progreso > 1:
            progreso = 1
        pygame.draw.rect(screen, BLUE2, pygame.Rect(Utils.ScreenWidth/2 - GUI_INFO_X2, Utils.ScreenHeight - GUI_INFO_Y2 + 85, 150*(progreso), 15))
        pygame.draw.rect(screen, BLUE, pygame.Rect(Utils.ScreenWidth/2 - GUI_INFO_X2, Utils.ScreenHeight - GUI_INFO_Y2 + 85, 150, 15), 2)

    def drawInfoOperative(self, screen, color):
        dic = self.toDictionary(self.mapa)
        muestra_texto(screen, str('monotypecorsiva'), dic['funcion'], color, 20, [Utils.ScreenWidth/2 - GUI_INFO_X2, Utils.ScreenHeight - GUI_INFO_Y2 + 50])

    def drawInfoSpawning(self, screen, color):
        #render de la tropa
        image = self.training[0].getRender()
        image = pg.transform.scale(image, SPAW_UNIT_RENDER_SIZE)
        screen.blit(image, (Utils.ScreenWidth/2 - GUI_INFO_X2 - 20, Utils.ScreenHeight - GUI_INFO_Y2 + 30))
        pg.draw.rect(screen, GREEN, pg.Rect(Utils.ScreenWidth/2 - GUI_INFO_X2 - 15, Utils.ScreenHeight - GUI_INFO_Y2 + 35, 55, 60), 2)

        #progreso
        progreso = self.generationCount / (CLOCK_PER_SEC * self.training[0].generationTime)
        if progreso > 1:
            progreso = 1
        pg.draw.rect(screen, BLUE2, pg.Rect(Utils.ScreenWidth/2 - GUI_INFO_X2 + 50, Utils.ScreenHeight - GUI_INFO_Y2 + 55, 130*(progreso), 10))
        pg.draw.rect(screen, BLUE, pg.Rect(Utils.ScreenWidth/2 - GUI_INFO_X2 + 50, Utils.ScreenHeight - GUI_INFO_Y2 + 55, 130, 10), 2)

        #tropas pendientes
        pg.draw.rect(screen, BLUE, pg.Rect(Utils.ScreenWidth/2 - GUI_INFO_X2 + 50, Utils.ScreenHeight - GUI_INFO_Y2 +80, 145, 55), 2)
        xPad = 0
        n = 0
        for unit in self.training[1:]:
            image = unit.getRender()
            image = pg.transform.scale(image, WAIT_UNIT_RENDER_SIZE)
            screen.blit(image, (Utils.ScreenWidth/2 - GUI_INFO_X2 + 50 + xPad, Utils.ScreenHeight - GUI_INFO_Y2 + 78))
            n += 1
            xPad += 45
            if n >= 3:
                break

    def checkTiles(self, visible = True):
        r = self.getRect()
        tiles = self.mapa.getRectTiles(r)
        ok = True
        tiles_set = set(tiles)
        if len(tiles_set) == self.TILES_HEIGHT*self.TILES_WIDTH:
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
            #if inCamera(self.getPosition()):
            playSound(self.deadSound)
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
