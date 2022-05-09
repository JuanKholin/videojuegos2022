from .Utils import *
from .Entities.TerranBarracks import *
from .Entities.TerranSupplyDepot import *
from .Command import *
from random import *

# Esta clase va a sacar lo peor de nosotros mismos, me temo
class AI():
    def __init__(self, artificialPlayer, race, difficult):
        self.data = artificialPlayer
        self.reactionTime = AI_LAPSE
        self.rotativeReaction = 0
        self.decissionRate = difficult
        self.count = 0
        self.decissionsChance = [ 25, 25, 25, 25 ]
        self.decissionsPool = sum(self.decissionsChance)
        self.minimalDecissionChance = 1
        self.mapa = self.data.getMapa()
        self.miniCount = 0

        self.minWorkers = 2
        self.minSoldiers = 2

        if race == Race.ZERG:
            self.base = ZERG_BASE
            self.barracks = ZERG_BARRACKS
            self.depot = ZERG_DEPOT
            self.geyserBuilding = ZERG_GEYSER_STRUCTURE
            self.worker = ZERG_WORKER
            self.soldier = ZERG_SOLDIER
            self.workerCost = ZERG_WORKER_MINERAL_COST
            self.soldierCost = ZERG_SOLDIER_MINERAL_COST
        elif race == Race.TERRAN:
            self.base = TERRAN_BASE
            self.barracks = TERRAN_BARRACKS
            self.depot = TERRAN_DEPOT
            self.geyserBuilding = TERRAN_GEYSER_STRUCTURE
            self.worker = TERRAN_WORKER
            self.soldier = TERRAN_SOLDIER
            self.workerCost = TERRAN_WORKER_MINERAL_COST
            self.soldierCost = TERRAN_SOLDIER_MINERAL_COST
        elif race == Race.PROTOSS:
            self.base = PROTOSS_BASE
            self.barracks = PROTOSS_BARRACKS
            self.depot = PROTOSS_DEPOT
            self.geyserBuilding = PROTOSS_GEYSER_STRUCTURE
            self.worker = PROTOSS_WORKER
            self.soldier = PROTOSS_SOLDIER
            self.workerCost = PROTOSS_WORKER_MINERAL_COST
            self.soldierCost = PROTOSS_SOLDIER_MINERAL_COST
        # Para los recursos
        self.crystalsSeen = set()
        self.geysersSeen = set()

        # Para las invasiones
        self.invaders = []

    # Haz lo tuyo IA, es tu turno
    def make_commands(self):
        units, structures = self.data.get_info()
        self.miniCount += 1
        if self.miniCount >= AI_LAPSE: # Acciones ligeras
            self.miniCount = 0
            self.alwaysToDoActions(units, structures)
        self.count += 1
        if self.count >= self.decissionRate: # Decisiones importantes
            self.count = 0
            self.makeDecission(units, structures)

    # Acciones que debe hacer casi siempre la IA
    def alwaysToDoActions(self, units, structures):
        if self.rotativeReaction == 0:
            self.selfDefense(units, structures)
        elif self.rotativeReaction == 1:
            self.minimalBuild(structures)
        elif self.rotativeReaction == 2:
            self.restoreArmy(units, structures)
        elif self.rotativeReaction == 3:
            self.gatherResources(units, structures)
        elif self.rotativeReaction == 4:
            self.updateInvaders()
        elif self.rotativeReaction == 5:
            self.updateVision(units, structures)
        self.rotativeReaction = (self.rotativeReaction + 1) % 6 # 6 acciones distintas hay

    # Toma una decision trascendental
    def makeDecission(self, units, structures):
        decission = self.decide()
        if decission == 0:
            print("IA DECIDE ATACAR LO VISIBLE")
            self.attackVisible()
        elif decission == 1:
            #print("IA DECIDE HACER MEJORAS")
            self.armyUpgrade()
        elif decission == 2:
            print("IA DECIDE EXPANDIR SU EJERCITO")
            self.armyExpansion(structures)
        elif decission == 3:
            print("IA DECIDE INVADIR")
            self.seekAndDestroy(units)

        print(self.decissionsChance)

    # Toma una decision y rebalancea el pool de decisiones, me ha quedado bastante original la verdad,
    # estoy orgulloso y no se ni si funciona xdxdxdxd
    def decide(self):
        randPick = randint(0, 99)
        for i in range(len(self.decissionsChance)):
            if randPick < self.decissionsChance[i]:
                # Rebalancea
                if self.decissionsChance[i] - (len(self.decissionsChance) - 1) > self.minimalDecissionChance:
                    self.decissionsChance[i] = self.decissionsChance[i] - (len(self.decissionsChance) - 1)
                    for j in range(len(self.decissionsChance)):
                        if j != i:
                            self.decissionsChance[j] += 1
                return i
            randPick = randPick - self.decissionsChance[i] 

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
    def minimalBuild(self, structures):
        if self.haveBase(structures):
            if not self.haveBarracks(structures):
                self.buildBarracks(structures)
            elif not self.haveDepot(structures):
                if (self.depot == ZERG_DEPOT) and (self.data.resources >= ZERG_DEPOT_MINERAL_COST):
                    #print("Construye zergdepot")
                    self.data.resources -= ZERG_DEPOT_MINERAL_COST
                    self.buildZergDepot(structures) # Seria Zerg pero no hay edificio xd
                elif (self.depot == TERRAN_DEPOT) and (self.data.resources >= TERRAN_DEPOT_MINERAL_COST):
                    #print("Construye terrandepot")
                    self.data.resources -= TERRAN_DEPOT_MINERAL_COST
                    self.buildTerranDepot(structures)
            
    # Si faltan workers o soldados los genera, si tiene recursos y hay edificios libres para ello
    def restoreArmy(self, units, structures):
        nWorkers = 0
        nSoldiers = 0
        for unit in units:
            if unit.type == self.worker:
                nWorkers += 1
            elif unit.type == self.soldier:
                nSoldiers += 1
        workersToCreate = self.minWorkers - nWorkers
        base = self.getBase(structures)
        if base != None:
            if workersToCreate > 0:
                if base.state == BuildingState.OPERATIVE:
                    #print("genworker")
                    base.execute(CommandId.GENERATE_WORKER)
            soldiersToCreate = self.minSoldiers - nSoldiers
            if soldiersToCreate > 0:
                barracks = self.getBarracks(structures)
                for structure in barracks:
                    if (structure.state == BuildingState.OPERATIVE) and (soldiersToCreate > 0):
                        soldiersToCreate = soldiersToCreate - 1
                        #print("gensoldier")
                        structure.execute(CommandId.GENERATE_SOLDIER)

    # Es un update de workers bastante cool, si no hace nada a minar, y si mina mina y ya
    def gatherResources(self, units, structures):
        workers = self.getWorkers(units)
        skipGasNeed = False
        if len(workers) > 0: # Si hay workers vivos y sin ser atacados
            for worker in workers:
                if (worker.state != UnitState.EXTRACTING) and (worker.state != UnitState.GAS_TRANSPORTING):
                    skipGasNeed = True 
            if not skipGasNeed: # Si hay al menos un worker extrayendo gas no es necesario hacer nada de gas
                gasMan = workers.pop()
                if self.haveGeyserInUse():
                    pass
                else:
                    if len(self.geysersSeen) > 0:
                        pass
            if len(workers) > 0: # Para el resto de workers
                if len(self.crystalsSeen) > 0: # si hay cristales conocidos,
                    crystalToMine = 0
                    for worker in workers: # todos a la mina
                        if worker.state == UnitState.STILL: # si les viene bien xd
                            worker.mine(self.crystalsSeen[crystalToMine]) 
                            crystalToMine = (crystalToMine + 1) % len(self.crystalsSeen)


    # Recorre las unidades invasoras para que vayan a atacar objetivos conocidos y si no hay explorar
    # tiles no exploradas y atacar lo que se encuentren hasta la muerte o la victoria
    def updateInvaders(self):
        pass

    #
    def updateVision(self, units, structures):
        pass

    ##############################
    # DECISIONES TRASCENDENTALES #
    ##############################

    def attackVisible(self):
        pass

    def armyUpgrade(self):
        pass

    # Aumenta los minimos del ejercito si se puede permitir al menos otro como el que tiene
    # Tambien construye un almacen si los recursos estan cerca del tope o construye otro
    # barracks si estan todos los edificios trabajando
    def armyExpansion(self, structures):
        # Almacen extra
        # AH QUE NO HACEN NADA VAYA PUTA ESTAFA

        # Barracks extra
        needExtraBarrack = True
        for structure in structures:
            if ((structure.type == self.base) or (structure.type == self.barracks)) and ((structure.state == BuildingState.OPERATIVE) or (structure.state == BuildingState.BUILDING)):
                needExtraBarrack = False
        if needExtraBarrack:
           self.buildBarracks(structures)

        # Minimos aumentados
        soldiersCost = self.minSoldiers * self.soldierCost
        if self.data.resources > soldiersCost:
            self.minSoldiers = self.minSoldiers + 1
        workersCost = self.minWorkers * self.workerCost
        if self.data.resources > workersCost + (soldiersCost / 2):
            self.minWorkers = self.minWorkers + 1

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
            if unit.type == self.soldier and unit.isReadyToFight():
                soldiers.append(unit)
        return soldiers

    # De las unidades devuelve a todos los workers libres
    def getWorkers(self, units):
        workers = []
        for unit in units:
            if unit.type == self.worker and unit.isReadyToWork():
                workers.append(unit)
        return workers

    # Devuelve si hay una base
    def haveBase(self, structures):
        for structure in structures:
            if structure.type == self.base:
                return True
        return False

    # Devuelve si hay un barracks
    def haveBarracks(self, structures):
        for structure in structures:
            if structure.type == self.barracks:
                return True
        return False

    # Devuelve si hay un depot
    def haveDepot(self, structures):
        for structure in structures:
            if structure.type == self.depot:
                return True
        return False

    # Construye un barracks de los Terran cerca de una estructura aliada aleatoria
    def buildTerranBarracks(self, structures):
        width = TerranBarracks.TILES_WIDTH
        height = TerranBarracks.TILES_HEIGHT
        centerTile = TerranBarracks.CENTER_TILE
        randBuilding = randint(0, len(structures) - 1)
        building = structures[randBuilding]
        randDirection = randint(0, 7)
        buildingsTried = 0
        directionsTried = 0
        x, y = self.getDirection(randDirection)
        buildX, buildY = building.getCords()

        builded = False
        while not builded:
            tryNew = True
            tile = self.mapa.getNextTileByOffset(buildX, buildY, x, y)
            if (tile != None) and (tile.type == STRUCTURE) and (tile.ocupante == building):
                buildX = buildX + x
                buildY = buildY + y
                #print(buildX," ", buildY, " STRUCTURE")
                tryNew = False
            elif (tile != None) and (tile.type == EMPTY): # Hueco tras edificio
                #Ahora checkear que haya hueco para el edificio a construir
                buildX = buildX + x
                buildY = buildY + y
                #print("first ", buildX, " ", buildY, " EMPTY")
                tile = self.mapa.getNextTileByOffset(buildX, buildY, x, y)
                if (tile != None) and (tile.type == EMPTY): # #primera tile libre para plantar edificio
                    buildX = buildX + x
                    buildY = buildY + y
                    #print("second ", buildX," ", buildY, " EMPTY")
                    buildX, buildY = self.getTopLeft(buildX, buildY, randDirection, width, height, centerTile)
                    #print("topLeft ", buildX," ", buildY)

                    if self.mapa.checkIfEmptyZone(buildX, buildY, buildX + (width - 1), buildY + (height - 1)):
                        #print("buildea")
                        toBuild = TerranBarracks(buildX + centerTile[0], buildY + centerTile[1], self.data, self.mapa, False)
                        self.data.addStructures(toBuild)
                        toBuild.buildProcess()
                        builded = True
            if tryNew and not builded:
                directionsTried = directionsTried + 1
                if directionsTried >= TOTAL_DIRECTIONS: # Se han probado todas las direcciones
                    directionsTried = 0
                    buildingsTried = buildingsTried + 1
                    if buildingsTried >= len(structures): # No hay espacio en el mapa (  9 _9)
                        #print("Wrong map, full occupied?")
                        exit()
                    else: # Quedan edificios por probar
                        randBuilding = (randBuilding + 1) % len(structures)
                        building = structures[randBuilding]
                else: # Quedan direcciones por probar
                    randDirection = (randDirection + 1) % TOTAL_DIRECTIONS
                    x, y = self.getDirection(randDirection)
                    #print ("New x e y ", x, " ", y)
                    buildX, buildY = building.getCords()

    # Construye un depot de los Terran cerca de una estructura aliada aleatoria
    def buildTerranDepot(self, structures):
        width = TerranSupplyDepot.TILES_WIDTH
        height = TerranSupplyDepot.TILES_HEIGHT
        centerTile = TerranSupplyDepot.CENTER_TILE
        randBuilding = randint(0, len(structures) - 1)
        building = structures[randBuilding]
        randDirection = randint(0, 7)
        buildingsTried = 0
        directionsTried = 0
        x, y = self.getDirection(randDirection)
        buildX, buildY = building.getCords()
        #print("HAOSDHAS")
        builded = False
        while not builded:
            tryNew = True
            tile = self.mapa.getNextTileByOffset(buildX, buildY, x, y)
            #print("hasdjkasd")
            if (tile != None) and (tile.type == STRUCTURE) and (tile.ocupante == building):
                buildX = buildX + x
                buildY = buildY + y
                #print(buildX," ", buildY, " STRUCTURE")
                tryNew = False
            elif (tile != None) and (tile.type == EMPTY): # Hueco tras edificio
                #Ahora checkear que haya hueco para el edificio a construir
                buildX = buildX + x
                buildY = buildY + y
                #print("first ", buildX, " ", buildY, " EMPTY")
                tile = self.mapa.getNextTileByOffset(buildX, buildY, x, y)
                if (tile != None) and (tile.type == EMPTY): # #primera tile libre para plantar edificio
                    buildX = buildX + x
                    buildY = buildY + y
                    #print("second ", buildX," ", buildY, " EMPTY")
                    buildX, buildY = self.getTopLeft(buildX, buildY, randDirection, width, height, centerTile)
                    #print("topLeft ", buildX," ", buildY)

                    if self.mapa.checkIfEmptyZone(buildX, buildY, buildX + (width - 1), buildY + (height - 1)):
                        #print("buildea")
                        toBuild = TerranSupplyDepot(buildX + centerTile[0], buildY + centerTile[1], self.data, self.mapa, False)
                        self.data.addStructures(toBuild)
                        toBuild.buildProcess()
                        builded = True
            if tryNew and not builded:
                directionsTried = directionsTried + 1
                if directionsTried >= TOTAL_DIRECTIONS: # Se han probado todas las direcciones
                    directionsTried = 0
                    buildingsTried = buildingsTried + 1
                    if buildingsTried >= len(structures): # No hay espacio en el mapa (  9 _9)
                        #print("Wrong map, full occupied?")
                        exit()
                    else: # Quedan edificios por probar
                        randBuilding = (randBuilding + 1) % len(structures)
                        building = structures[randBuilding]
                else: # Quedan direcciones por probar
                    randDirection = (randDirection + 1) % TOTAL_DIRECTIONS
                    x, y = self.getDirection(randDirection)
                    #print ("New x e y ", x, " ", y)
                    buildX, buildY = building.getCords()

    # Devuelve una direccion por la que avanzar para probar construcciones
    def getDirection(self, direction):
        if direction == 0:
            return 0, -1
        elif direction == 1:
            return 1, -1
        elif direction == 2:
            return 1, 0
        elif direction == 3:
            return 1, 1
        elif direction == 4:
            return 0, 1
        elif direction == 5:
            return -1, 1
        elif direction == 6:
            return -1, 0
        elif direction == 7:
            return -1, -1

    def getTopLeft(self, buildX, buildY, direction, w, h, centerTile):
        if direction == 0:
            buildX = buildX - centerTile[0]
            buildY = buildY - (h - 1)
            return buildX, buildY
        elif direction == 1:
            buildY = buildY - (h - 1)
            return buildX, buildY
        elif direction == 2:
            buildY = buildY - centerTile[1]
            return buildX, buildY
        elif direction == 3:
            return buildX, buildY
        elif direction == 4:
            buildX = buildX - centerTile[0]
            return buildX, buildY
        elif direction == 5:
            buildX = buildX - (w - 1)
            return buildX, buildY
        elif direction == 6:
            buildX = buildX - (w - 1)
            buildY = buildY - centerTile[1]
            return buildX, buildY
        elif direction == 7:
            buildX = buildX - (w - 1)
            buildY = buildY - (h - 1)
            return buildX, buildY

    def getBase(self, structures):
        for structure in structures:
            if structure.type == self.base:
                return structure
        return None

    def getBarracks(self, structures):
        result = []
        for structure in structures:
            if structure.type == self.barracks:
                result.append(structure)
        return result

    def buildBarracks(self, structures):
        if (self.barracks == ZERG_BARRACKS) and (self.data.resources >= ZERG_BARRACKS_MINERAL_COST):
            print("Construye zergbarracks")
            self.data.resources -= ZERG_BARRACKS_MINERAL_COST
            self.buildTerranBarracks(structures) # Seria Zerg pero no hay edificio xd
        elif (self.barracks == TERRAN_BARRACKS) and (self.data.resources >= TERRAN_BARRACKS_MINERAL_COST):
            print("Construye terranbarracks")
            self.data.resources -= TERRAN_BARRACKS_MINERAL_COST
            self.buildTerranBarracks(structures)