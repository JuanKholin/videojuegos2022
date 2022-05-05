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
        self.mapa = self.data.getMapa()

        # Para las invasiones
        self.invaders = []

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
        self.updateInvaders()

    # Toma una decision trascendental
    def makeDecission(self, units, structures, resources):
        decission = self.decide()
        if decission == 0:
            print("IA DECIDE ATACAR LO VISIBLE")
            self.attackVisible()
        elif decission == 1:
            print("IA DECIDE EXPANDIR CONSTRUCCIONES")
            self.buildExpansion()
        elif decission == 2:
            print("IA DECIDE EXPANDIR SU EJERCITO")
            self.armyExpansion()
        elif decission == 3:
            print("IA DECIDE IR POR RECURSOS LEJOS")
            self.gatherFarResources()
        elif decission == 4:
            print("IA DECIDE INVADIR")
            self.seekAndDestroy(units)

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

    # Recorre las unidades invasoras para que vayan a atacar objetivos conocidos y si no hay explorar
    # tiles no exploradas y atacar lo que se encuentren hasta la muerte o la victoria
    # CLARO ESTO SI HUBIERA VISION ASJIDASJFIDSFJEWR
    def updateInvaders(self):
        pass

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

    # Apunta a ciertos soldados libres en funcion del ejercito disponible 
    # para invadir hasta su muerte o la victoria
    def seekAndDestroy(self, units):
        soldiers = self.getSoldiers(units)
        num = 0
        if soldiers.len > 10:
            #ejercito de 3
            num = 3
        elif soldiers.len > 5:
            #ejercito de 2
            num = 2
        elif soldiers.len > 3:
            #ejercito de 3
            num = 1
        for i in range(num):
            self.player.removeFromFree(soldiers[i])
            self.invaders.append(soldiers[i])

    ##############
    # AUXILIARES #
    ##############

    # De las unidades devuelve a todos los soldados
    def getSoldiers(self, units):
        soldiers = []
        for unit in units:
            if unit.isSoldier():
                soldiers.append(unit)
        return soldiers
