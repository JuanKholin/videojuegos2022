from . import Unit
from ..Utils import *
from ..Command import *
import math

import pygame as pg

class Worker(Unit.Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                    faces, frame, padding, id,player, minePower, timeToMine, inersibleFrames, frames,
                        dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding,
                            oreTransportingFrames):
        Unit.Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                                faces, frame, padding, id, player, minePower, timeToMine, inersibleFrames, frames,
                                    dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding)
        
        self.oreTransportingFrames = oreTransportingFrames


    def changeToMining(self):
        self.state = State.MINING
        self.dir = int(4 - (self.miningAngle * 8 / math.pi)) % 16
        self.count = 0
        self.frame = 0
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    #Especifico para worker
    def updateMining(self):
        self.count += pg.time.Clock().tick(CLOCK_PER_SEC)
        if self.count > self.timeToMine: #Termina de minar
            self.order = {'order':CommandId.TRANSPORTAR_ORE}
            self.cristal.getMined(self.minePower)
            self.paths = []
            for path in self.basePath:
                self.paths.append(path.copy())
            self.state = State.ORE_TRANSPORTING
        elif frame(self.framesToRefresh):
            self.updateMiningImage()
        elif len(self.paths) > 0:
            self.state = State.MOVING
    
    # Pasa de frame en una animacion de minado
    def updateMiningImage(self):
        self.frame = (self.frame + 1) % len(self.attackFrames)
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    def changeToOreTransporting(self):
        self.state = State.ORE_TRANSPORTING
        self.dir = int(4 - (self.miningAngle * 8 / math.pi)) % 16
        self.count = 0
        self.frame = 0
        self.image = self.sprites[self.frames[self.oreTransportingFrames[self.frame]][self.dirOffset[self.dir]]]

    def updateOreTransporting(self):
        if self.paths.__len__() != 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
            else: # Se acaba este camino
                self.finisOrehPath()
        self.updateOreTransportingImage()
    
    def finisOrehPath(self):
        self.paths.pop(0)
        if len(self.paths) == 0:
            print(self.order['order'])
            if self.order != 0:
                if self.order['order'] == CommandId.TRANSPORTAR_ORE:
                    #sumar minerales al jugador
                    if self.cristal.capacidad < 0:
                        self.player.resources += self.minePower + self.cristal.capacidad
                        self.changeToStill()
                        del self.cristal
                    else:
                        self.order = {'order': CommandId.MINAR_BUCLE}
                        self.player.resources += self.minePower
                        self.paths = []
                        for path in self.cristalPath:
                            self.paths.append(path.copy())
                        self.changeToMove()
                elif self.order['order'] == CommandId.TRANSPORTAR_ORE_STILL:
                    #print("sumar minerales al jugador")
                    if self.cristal.capacidad < 0:
                        self.player.resources += self.minePower + self.cristal.capacidad
                        self.changeToStill()
                        del self.cristal
                    else:
                        self.player.resources += self.minePower
                        self.changeToStill()
                        del self.cristal
                elif self.order['order'] == CommandId.MINAR_BUCLE:
                    #sumar minerales al jugador         
                    self.changeToMining()
    
    # Pasa de frame en una animacion de minado
    def updateOreTransportingImage(self):
        self.frame = (self.frame + 1) % len(self.oreTransportingFrames)
        self.image = self.sprites[self.frames[self.oreTransportingFrames[self.frame]][self.dirOffset[self.dir]]]