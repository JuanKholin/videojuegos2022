from .Unit import *

class Soldier(Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                    faces, frame, padding, id,player, inersibleFrames, frames,
                        dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, 
                        hPadding, attackInfo):
        Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, 
                        faces, frame, padding, id, player, inersibleFrames, frames,
                            dirOffset, attackFrames, stillFrames, moveFrames, dieFrames, xPadding, yPadding, wPadding, 
                            hPadding, attackInfo)


    #def update():
    #    pass

    def changeToMining(self):
        self.changeToStill()

    # Indica a la IA si es soldado o worker
    def isSoldier(self):
        return True
    
    def getType(self):
        return 0