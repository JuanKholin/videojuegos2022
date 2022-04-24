from .Unit import *

class Soldier(Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                    faces, frame, padding, id,player, minePower, timeToMine, inersibleFrames, frames,
                        dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding):
        Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                        faces, frame, padding, id, player, minePower, timeToMine, inersibleFrames, frames,
                            dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, hPadding)


    #def update():
    #    pass

    def changeToMining(self):
        self.changeToStill()

    def attack():
        pass