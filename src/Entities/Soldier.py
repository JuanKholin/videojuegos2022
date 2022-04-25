from .Unit import *

class Soldier(Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                    faces, frame, padding, id,player, minePower, timeToMine, inersibleFrames, frames,
                        dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, 
                        hPadding, attackInfo):
        Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                        faces, frame, padding, id, player, minePower, timeToMine, inersibleFrames, frames,
                            dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, 
                            hPadding, attackInfo)


    #def update():
    #    pass

    def changeToMining(self):
        self.changeToStill()