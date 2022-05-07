from .Utils import *
from random import *

# Esta clase va a sacar lo peor de nosotros mismos, me temo
class AI():
    def __init__(self, artificialPlayer, difficult):
        self.data = artificialPlayer
        self.reactionTime = AI_LAPSE
        self.rotativeReaction = 0
        self.decissionRate = difficult
        self.count = 0
        self.decissionsChance = [ 20, 20, 20, 20, 20 ]
        self.decissionsPool = sum(self.decissionsChance)
        self.minimalDecissionChance = 1
        self.mapa = self.data.getMapa()
        self.miniCount = 0

        # Para las invasiones
        self.invaders = []

    # Haz lo tuyo IA, es tu turno
    def make_commands(self):
        units, structures, resources = self.data.get_info()
        self.miniCount += 1
        if self.miniCount >= AI_LAPSE: # Acciones ligeras
            self.miniCount = 0
            self.alwaysToDoActions(units, structures, resources)
        #self.count += 1
        #if self.count >= self.decissionRate: # Decisiones importantes
        #    self.count = 0
        #    self.makeDecission(units, structures, resources)

    # Acciones que debe hacer casi siempre la IA
    def alwaysToDoActions(self, units, structures, resources):
        if self.rotativeReaction == 0:
            print("self defense")
            self.selfDefense(units, structures)
        elif self.rotativeReaction == 1:
            print("minimal build")
            #self.minimalBuild()
        elif self.rotativeReaction == 2:
            print("restore army")
            #self.restoreArmy()
        elif self.rotativeReaction == 3:
            print("gather nearby resources")
            #self.gatherNearbyResources()
        elif self.rotativeReaction == 4:
            print("update invaders")
            #self.updateInvaders()
        self.rotativeReaction = (self.rotativeReaction + 1) % 5 # 5 acciones distintas hay

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

    # Encuentra las unidades atacando a las estructuras y a las unidades de la IA y se defiende
    def selfDefense(self, units, structures):
        # Consigue el set de objetivos sin repetidos
        objectivesSet = set()
        for structure in structures: 
            if structure.lastAttacker != None:
                if structure.lastAttacker.attackedOne == structure:
                    objectivesSet.add(structure.lastAttacker)
                structure.lastAttacker = None
        for unit in units:
            if unit.attackedOne != None:
                objectivesSet.add(unit.attackedOne)
        objectivesList = list(objectivesSet) # Lo pasa a lista por comodi<padre_en_ingles>
        defenses = self.getSoldiers(units)
        if len(objectivesList) > 0: # Si hay amenazas reparte las tropas libres a por ellas
            i = 0
            for soldier in defenses:
                soldier.attack(objectivesList[i])
                i = (i + 1) % len(objectivesList)

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

    # De las unidades devuelve a todos los soldados libres
    def getSoldiers(self, units):
        soldiers = []
        for unit in units:
            if unit.isSoldier() and unit.isReadyToFight():
                soldiers.append(unit)
        return soldiers
