from .Unit import *
from ..Utils import *
from .. import Utils
from ..Command import *
import math

import pygame as pg

class Worker(Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                    faces, frame, padding, id,player, minePower, timeToMine, inersibleFrames, frames,
                        dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding,
                            oreTransportingFrames, attackInfo):
        Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                                faces, frame, padding, id, player, minePower, timeToMine, inersibleFrames, frames,
                                    dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding, 
                                    attackInfo)
        
        self.oreTransportingFrames = oreTransportingFrames


    def changeToMining(self):
        print("PASO AL MINING")
        self.state = State.MINING
        self.dir = int(4 - (self.miningAngle * 8 / math.pi)) % 16
        self.count = 0
        self.frame = 0
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    #Especifico para worker
    def updateMining(self):
        self.count += 1
        if getGlobalTime() - self.startTimeMining > self.timeToMine: #Termina de minar
            #Hay que volver a base transportando un ore
            self.cantidadMinada = self.cristal.getMined(self.minePower)
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
                self.paths = calcPath(tileActual, tileObj, self.mapa)
                self.changeToOreTransporting()
        elif self.count >= self.framesToRefresh:
            self.count = 0
            self.updateMiningImage()
        elif len(self.paths) > 0:
            self.state = State.MOVING
    
    # Pasa de frame en una animacion de minado
    def updateMiningImage(self):
        self.frame = (self.frame + 1) % len(self.attackFrames)
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    def changeToOreTransporting(self):
        print("PASO AL ORE TRANSPORTING")
        self.state = State.ORE_TRANSPORTING
        self.dir = int(4 - (self.miningAngle * 8 / math.pi)) % 16
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
            if self.cristal.capacidad < 0:
                self.player.resources += self.cantidadMinada
                print("cambiamos a still")
                self.changeToStill()
                del self.cristal
            else:
                #Tengo que volver, calculo el camino a minar
                self.player.resources += self.cantidadMinada
                self.paths = []

                posicionActual = self.getPosition()
                tileActual = self.mapa.getTile(posicionActual[0], posicionActual[1])
                tilesCristal = self.tilesCristal()
                if tilesCristal.__len__() == 0:
                    #No hay sitio para minar
                    self.changeToStill()
                else:
                    tileObj = tilesCristal[0]
                    for tile in tilesCristal:
                        if tile.heur(tileActual) < tileObj.heur(tileActual):
                            tileObj = tile

                    self.paths = calcPath(tileActual, tileObj, self.mapa)
                    self.changeToMovingToMining()
                
                
            
    
    # Pasa de frame en una animacion de minado
    def updateOreTransportingImage(self):
        self.frame = (self.frame + 1) % len(self.oreTransportingFrames)
        self.image = self.sprites[self.frames[self.oreTransportingFrames[self.frame]][self.dirOffset[self.dir]]]

    def setCristal(self, cristal):
        self.cristal = cristal

    def changeToMovingToMining(self):
        print("PASO A MOVERME AL CRISTAL")
        self.state = State.MOVING_TO_MINING
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
            self.miningAngle = self.angle
            self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
            self.changeToMining()

    def tilesCristal(self):
        tilesObj = []
        rect = self.cristal.getRect()
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