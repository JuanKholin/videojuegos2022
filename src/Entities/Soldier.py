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

    def getUpgrades(self):
        upgrades = []
        if self.player.armorUpgrade == 0:
            upgrades.append({'upgrade': Upgrades.NO_ARMOR, 'cantidad': 0})
        else:
            upgrades.append({'upgrade': Upgrades.ARMOR, 'cantidad': self.player.armorUpgrade})
        if self.player.dañoUpgrade == 0:
            upgrades.append({'upgrade': Upgrades.NO_DANYO, 'cantidad': 0})
        else:
            upgrades.append({'upgrade': Upgrades.DANYO, 'cantidad': self.player.dañoUpgrade})
        return upgrades