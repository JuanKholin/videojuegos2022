from . import Unit
from .. import Utils, Command

import pygame as pg

class Worker(Unit.Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                    faces, frame, padding, id,player, minePower, timeToMine, dieOffset, inersibleFrames, frames,
                        dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding):
        Unit.Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                                faces, frame, padding, id, player, minePower, timeToMine, dieOffset, inersibleFrames, frames,
                                    dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding)

    #Especifico para worker
    def updateMining(self):
        self.count += pg.time.Clock().tick(Utils.CLOCK_PER_SEC)
        print(self.count)
        if self.count > self.timeToMine: #Termina de minar
            self.order = {'order':Command.CommandId.TRANSPORTAR_ORE}
            self.cristal.getMined(self.minePower)
            print(self.basePath.__len__())
            self.paths = []
            for path in self.basePath:
                self.paths.append(path.copy())
            self.state = Utils.State.MOVING
        elif Utils.frame(self.framesToRefresh):
            self.updateMiningImage()
        if len(self.paths) > 0:
            self.state = Utils.State.MOVING
    
    # Pasa de frame en una animacion de minado
    def updateMiningImage(self):
        self.frame = (self.frame + 1) % len(self.attackFrames)
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]