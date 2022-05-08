from .Utils import *
from random import *

# Esta clase va a sacar lo peor de nosotros mismos, me temo
class AI():
    def __init__(self, artificialPlayer, race, difficult):
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

        if race == Race.ZERG:
            self.base = ZERG_BASE
            self.barracks = ZERG_BARRACKS
            self.depot = ZERG_DEPOT
            self.geyserBuilding = ZERG_GEYSER_STRUCTURE
        elif race == Race.TERRAN:
            self.base = TERRAN_BASE
            self.barracks = TERRAN_BARRACKS
            self.depot = TERRAN_DEPOT
            self.geyserBuilding = TERRAN_GEYSER_STRUCTURE
        elif race == Race.PROTOSS:
            self.base = PROTOSS_BASE
            self.barracks = PROTOSS_BARRACKS
            self.depot = PROTOSS_DEPOT
            self.geyserBuilding = PROTOSS_GEYSER_STRUCTURE

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
            #print("self defense")
            self.selfDefense(units, structures)
        '''
        elif self.rotativeReaction == 1:
            print("minimal build")
            #self.minimalBuild(structures)
        elif self.rotativeReaction == 2:
            #print("restore army")
            #self.restoreArmy()
        elif self.rotativeReaction == 3:
            #print("gather nearby resources")
            #self.gatherNearbyResources()
        elif self.rotativeReaction == 4:
            #print("update invaders")
            #self.updateInvaders()'''
        self.rotativeReaction = (self.rotativeReaction + 1) % 5 # 5 acciones distintas hay

    # Toma una decision trascendental
    def makeDecission(self, units, structures, resources):
        decission = self.decide()
        if decission == 0:
            #print("IA DECIDE ATACAR LO VISIBLE")
            self.attackVisible()
        elif decission == 1:
            print("IA DECIDE HACER MEJORAS")
            self.armyUpgrade()
        elif decission == 2:
            #print("IA DECIDE EXPANDIR SU EJERCITO")
            self.armyExpansion()
        elif decission == 3:
            #print("IA DECIDE IR POR RECURSOS LEJOS")
            self.gatherFarResources()
        elif decission == 4:
            #print("IA DECIDE INVADIR")
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

    # Si la IA tiene al menos una estructura puede construir mas, se considera build minima
    # un edificio de cada
    def minimalBuild(self, structures, resources):
        if haveBase(structures):
            if not haveBarracks(structures):
                if (self.barracks == ZERG_BARRACKS) and (self.resources >= ZERG_BARRACKS_MINERAL_COST):
                    self.data.resources -= ZERG_BARRACKS_MINERAL_COST
                    self.buildZergBarracks(structures)
                elif (self.barracks == TERRAN_BARRACKS) and (self.resources >= TERRAN_BARRACKS_MINERAL_COST):
                    self.data.resources -= TERRAN_BARRACKS_MINERAL_COST
                    self.buildTerranBarracks(structures)
            elif not haveDepot(structures):
                if (self.depot == ZERG_DEPOT) and (self.resources >= ZERG_DEPOT_MINERAL_COST):
                    self.data.resources -= ZERG_DEPOT_MINERAL_COST
                    self.buildZergDepot(structures)
                elif (self.barracks == TERRAN_DEPOT) and (self.resources >= TERRAN_DEPOT_MINERAL_COST):
                    self.data.resources -= TERRAN_DEPOT_MINERAL_COST
                    self.buildTerranDepot(structures)
            
    def restoreArmy(self):
        pass

    def gatherNearbyResources(self):
        pass

    ##############################
    # DECISIONES TRASCENDENTALES #
    ##############################

    def attackVisible(self):
        pass

    def armyUpgrade(self):
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

    # Devuelve una lista con los tipos de edificios que no se tienen
    def findHavingBuildings(self, structures):
        haveBarrack = False
        haveDepot = False
        for structure in structures:
            havingBuildings.add(self.buildingSet.index(type(structure)))
        nonHavingBuildings = list(set(range(len(self.buildingSet))).difference(havingBuildings))

    # Devuelve si hay una base
    def haveBase(self, structures):
        for structure in structures:
            if type(structure) == self.base:
                return True
        return False

    # Devuelve si hay un barrack
    def haveBarrack(self, structures):
        for structure in structures:
            if type(structure) == self.barrack:
                return True
        return False

    # Devuelve si hay un depot
    def haveDepot(self, structures):
        for structure in structures:
            if type(structure) == self.depot:
                return True
        return False

    # Construye si se puede el edificio indicado en el buildingSet con indice i
    def build(self, i, structures):
        if self.buildStructure.checkTiles() and self.player.resources >= self.buildStructure.mineralCost:
            self.player.resources -= self.buildStructure.mineralCost
            self.buildStructure.player = self.player
            self.player.addStructures(self.buildStructure)
            self.buildStructure.buildProcess()
            self.building = False
            self.buildStructure = None

            building = globals()[self.buildingSet[i]]
            buildingInstance = building()
            
    # Construye un barracks de los Terran cerca de una estructura aliada aleatoria
    def buildTerranBarracks(self, structures):
        randBuilding = structures[randInt(0, len(structures) - 1)]
        x, y = self.getRandDirection()

    # Construye un barracks de los Zerg cerca de una estructura aliada aleatoria
    def buildZergBarracks(self, structures):
        randBuilding = structures[randInt(0, len(structures) - 1)]

    # Construye un depot de los Terran cerca de una estructura aliada aleatoria
    def buildTerranDepot(self, structures):
        randBuilding = structures[randInt(0, len(structures) - 1)]

    # Construye un depot de los Zerg cerca de una estructura aliada aleatoria
    def buildZergDepot(self, structures):
        randBuilding = structures[randInt(0, len(structures) - 1)]

    # Devuelve una direccion por la que avanzar para probar construcciones
    def getRandDirection(self):
        randDirection = randInt(0, 7)
        if randDirection == 0:
            return 0, -1
        elif randDirection == 1:
            return 1, -1
        elif randDirection == 2:
            return 1, 0
        elif randDirection == 3:
            return 1, 1
        elif randDirection == 4:
            return 0, 1
        elif randDirection == 5:
            return -1, 1
        elif randDirection == 6:
            return -1, 0
        elif randDirection == 7:
            return -1, -1