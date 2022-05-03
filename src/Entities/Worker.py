from .Unit import *
from ..Utils import *
from .. import Utils
from ..Command import *
import math

class Worker(Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                    faces, frame, padding, id,player, minePower, timeToMine, inersibleFrames, frames,
                        dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding,
                            oreTransportingFrames, attackInfo):
        Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                                faces, frame, padding, id, player, inersibleFrames, frames,
                                    dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding, 
                                    attackInfo)
        # Info minado
        self.startTimeMining = 0
        self.minePower = minePower
        self.timeToMine = timeToMine
        self.resource = None
        self.isMining = False
        self.oreTransportingFrames = oreTransportingFrames

    # Indica a la unidad que recolecte mineral o gas del objetivo, si se encuentra
    # un obstaculo de camino lo esquivara. Recolecta desde la tile libre mas cercana
    def mine(self, resource):
        self.changeToMining(resource)

    def changeToMining(self, resource):
        if resource.getCapacity() != 0: # Si hay recurso, si es gas agotado es -algo
            self.state = UnitState.MINING
            self.isMining = False
            self.resource = resource
            pos = self.resource.getPosition()
            tile = self.mapa.getTile(pos[0], pos[1])
            tiles = self.mapa.getEntityTilesVecinas(tile)
            if len(tiles) > 0:
                ownTile = self.getTile()
                bestTile = tiles[0]
                for tile in tiles:
                    if tile.heur(ownTile) < bestTile.heur(ownTile):
                        bestTile = tile
                self.paths = calcPath(self.getPosition(), self.getTile(), bestTile, self.mapa)
                if len(self.paths) > 0:
                    self.moveToMining()
                else:
                    self.startMining()
            else:
                print("No hay tiles libres weird")
                exit(1)

    # Manda a la unidad hacia el recurso
    def moveToMining(self):
        self.isMining = False
        actualPath = self.paths[len(self.paths) - 1]
        if actualPath.angle < 0:
            self.angle = -actualPath.angle
        else:
            self.angle = 2 * math.pi - actualPath.angle
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]
        
    # Ya esta al lado del recurso y prepara el minado
    def startMining(self):
        self.startTimeMining = Utils.getGlobalTime()
        print("Start mining", self.startTimeMining)
        xCristal, yCristal = self.resource.getCenter()
        posicionActual = self.getPosition()
        self.isMining = True
        self.angle = math.atan2(yCristal - posicionActual[1], xCristal - posicionActual[0])
        if self.angle < 0:
            self.angle = -self.angle
        else:
            self.angle = 2 * math.pi - self.angle
        self.miningAngle = self.angle
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16

    #Especifico para worker
    def updateMining(self):
        if len(self.paths) == 0:
            if self.isMining:
                self.updateMiningAct()
            else:
                self.startMining()
        else:
            self.updateMiningRoute()
    
    def updateMiningRoute(self):
        if len(self.paths) > 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
                self.count += 1
                if self.count >= self.framesToRefresh:
                    self.count = 0
                    self.updateMovingImage()
            else: # Se acaba este camino
                self.paths.pop(0)

    def updateMiningAct(self):
        self.count += 1
        if getGlobalTime() - self.startTimeMining > self.timeToMine: #Termina de minar
            self.isMining = False
            #Hay que volver a base transportando un ore
            self.cantidadMinada = self.resource.getMined(self.minePower)
            self.paths = []
            if self.cantidadMinada == 0: #No ha minado nada, se queda en el sitio
                self.changeToStill()
            else:
                #Calcular el camino a casa
                posicionActual = self.getPosition()
                tileActual = self.mapa.getTile(posicionActual[0], posicionActual[1])
                tilesCasa = self.tilesCasa()
                tileObj = tilesCasa[0]
                for tile in tilesCasa:
                    if tile.heur(tileActual) < tileObj.heur(tileActual):
                        tileObj = tile
                self.paths = calcPath(self.getPosition(), tileActual, tileObj, self.mapa)
                self.changeToOreTransporting()
        elif self.count >= self.framesToRefresh:
            self.count = 0
            self.updateMiningImage()

    # Pasa de frame en una animacion de minado
    def updateMiningImage(self):
        self.frame = (self.frame + 1) % len(self.attackFrames)
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    def changeToOreTransporting(self):
        self.state = UnitState.ORE_TRANSPORTING
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
        self.count = 0
        self.frame = 0
        self.image = self.sprites[self.frames[self.oreTransportingFrames[self.frame]][self.dirOffset[self.dir]]]

    def updateOreTransporting(self):
        self.count += 1
        if self.paths.__len__() != 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
            else: # Se acaba este camino
                self.finishOrePath()
        if self.count >= self.framesToRefresh:
            self.count = 0
            self.updateOreTransportingImage()
    
    def finishOrePath(self):
        self.paths.pop(0)
        if len(self.paths) == 0: # he entregado el ore, miro si tengo que volver
            if self.resource.capacity < 0:
                self.player.resources += self.cantidadMinada
                print("cambiamos a still")
                self.changeToStill()
            else:
                #Tengo que volver, calculo el camino a minar
                self.player.resources += self.cantidadMinada
                self.paths = []

                posicionActual = self.getPosition()
                tileActual = self.mapa.getTile(posicionActual[0], posicionActual[1])
                tilesResource = self.tilesResource()
                if tilesResource.__len__() == 0:
                    #No hay sitio para minar
                    self.changeToStill()
                else:
                    tileObj = tilesResource[0]
                    for tile in tilesResource:
                        if tile.heur(tileActual) < tileObj.heur(tileActual):
                            tileObj = tile

                    self.paths = calcPath(self.getPosition(), tileActual, tileObj, self.mapa)
                    self.changeToMining(self.resource)         
            
    
    # Pasa de frame en una animacion de minado
    def updateOreTransportingImage(self):
        self.frame = (self.frame + 1) % len(self.oreTransportingFrames)
        self.image = self.sprites[self.frames[self.oreTransportingFrames[self.frame]][self.dirOffset[self.dir]]]

    def setCristal(self, cristal):
        self.cristal = cristal

    def changeToMovingToMining(self):
        print("PASO A MOVERME AL CRISTAL")
        self.state = UnitState.MOVING_TO_MINING
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
        self.count = 0
        self.frame = 0
        self.image = self.sprites[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]

    def updateMovingToMining(self):
        self.count += 1
        if self.paths.__len__() != 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
            else: # Se acaba este camino
                self.finishMiningPath()
        if self.count >= self.framesToRefresh:
            self.count = 0
            self.updateMovingImage()

    def finishMiningPath(self):
        self.paths.pop(0)
        if len(self.paths) == 0: #Hay que ponerse a minar
            print("Hay que ponerse a minar")
            self.startTimeMining = getGlobalTime()
            xCristal, yCristal = self.cristal.getCenter()
            posicionActual = self.getPosition()
            self.angle = math.atan2(yCristal - posicionActual[1], xCristal - posicionActual[0])
            if self.angle < 0:
                self.angle = -self.angle
            else:
                self.angle = 2 * math.pi - self.angle
            self.miningAngle = self.angle
            self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
            self.changeToMining()

    def tilesResource(self):
        tilesObj = []
        rect = self.resource.getRect()
        x = self.mapa.getTile(rect.x, rect.y).centerx
        finx = x + rect.w
        y = self.mapa.getTile(rect.x, rect.y).centery
        finy = y + rect.h
        while x <= finx:
            tileUp = self.mapa.getTile(x,y - 40)
            tileDown = self.mapa.getTile(x,finy + 40)
            #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
            if tileUp.type == 0:
                tilesObj.append(tileUp)
            if tileDown.type == 0:
                tilesObj.append(tileDown)
            x += 40
        while y <= finy:
            tileUp = self.mapa.getTile(x - 40,y)
            tileDown = self.mapa.getTile(finx + 40,y)
            #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
            if tileUp.type == 0:
                tilesObj.append(tileUp)
            if tileDown.type == 0:
                tilesObj.append(tileDown)
            y += 40
        return tilesObj

    # Indica a la IA si es soldado o worker
    def isSoldier(self):
        return False