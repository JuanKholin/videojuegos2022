from .Utils import *
from random import *

# Esta clase va a sacar lo peor de nosotros mismos, me temo
class AI():
    def __init__(self, artificialPlayer, difficult):
        self.data = artificialPlayer
        self.reactionTime = AI_LAPSE
        self.decissionRate = difficult
        self.count = 0
        self.decissionsChance = [ 20, 20, 20, 20, 20 ]
        self.decissionsPool = sum(self.decissionsChance)
        self.minimalDecissionChance = 1

    # Haz lo tuyo IA, es tu turno
    def make_commands(self):
        units, structures, resources = self.data.get_info()
        self.miniCount += 1
        if self.miniCount >= AI_LAPSE: # Acciones ligeras
            self.miniCount = 0
            self.alwaysToDoActions(units, structures, resources)
        self.count += 1
        if self.count >= self.decissionRate: # Decisiones importantes
            self.count = 0
            self.makeDecission(units, structures, resources)

    # Acciones que debe hacer siempre la IA
    def alwaysToDoActions(self, units, structures, resources):
        self.selfDefense()
        self.minimalBuild()
        self.restoreArmy()
        self.gatherNearbyResources()

    # Toma una decision trascendental
    def makeDecission(self, units, structures, resources):
        decission = self.decide()
        if decission == 0:
            self.attackVisible()
        elif decission == 1:
            self.buildExpansion()
        elif decission == 2:
            self.armyExpansion()
        elif decission == 3:
            self.gatherFarResources()
        elif decission == 4:
            self.seekAndDestroy()

    # Toma una decision y rebalancea el pool de decisiones, me ha quedado bastante original la verdad, 
    # estoy orgulloso y no se ni si funciona xdxdxdxd
    def decide(self):
        randPick = randint(1, 100)
        for i in range(len(self.decissionsChance)):
            if randPick < self.decissionsChance[i]:
                if self.decissionsChance[i] - len(self.decissionsChance - 1) > self.minimalDecissionChance:
                    self.decissionsChance[i] - len(self.decissionsChance - 1)
                    for j in range(len(self.decissionsChance)):
                        if j != i:
                            self.decissionsChance[j] += 1
                return i
            randPick - self.decissionsChance[i]

    ####################
    # ACCIONES LIGERAS #
    ####################

    def selfDefense(self):
        pass

    def minimalBuild(self):
        pass

    def restoreArmy(self):
        pass

    def gatherNearbyResources(self):
        pass

    ##############################
    # DECISIONES TRASCENDENTALES #
    ##############################

    def attackVisible(self):
        pass

    def buildExpansion(self):
        pass

    def armyExpansion(self):
        pass

    def gatherFarResources(self):
        pass

    def seekAndDestroy(self):
        pass