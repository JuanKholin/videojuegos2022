from .Escena import *
from .Map import *
from .Player import *
from .Camera import *
from .Interface import *
from .Entities.Crystal import *
from .Entities.Geyser import *
from .Entities.TerranWorker import *
from .Entities.TerranBuilder import *
from .Entities.TerranSoldier import *
from .Entities.TerranBarracks import *
from .Entities.TerranSupplyDepot import *
from .Entities.TerranRefinery import *
from .Entities.Hatchery import *
from .Entities.Extractor import *
from .Entities.Drone import *
from .Entities.Zergling import *
from .Utils import *

def loadFromSave(nombre):
    escena = Escena(None, None, None, None, None, None, None, None)

    textFile = open("games/" + nombre + ".json", "r")
    data = json.load(textFile)

    #mapa
    escena.mapa = loadMap(data["mapa"])
    #players
    escena.p1 = loadPlayer(data["p1"], escena.mapa, True)
    escena.p2 = loadPlayer(data["p2"], escena.mapa, False)
    escena.walls = loadMuros(data["muros"], escena.mapa)
    # Raton
    raton = Raton.Raton(escena.p1, escena.p2, escena.mapa)


    raton.setEscena(escena)
    escena.raton = raton

    loadStructures(data["p1"]["structures"], escena.p1, escena.mapa, escena.raton)
    loadStructures(data["p2"]["structures"], escena.p2, escena.mapa, escena.raton)
    
    

    camera = loadCamera(data["camera"])
    escena.camera = camera

    escena.resources = loadResources(data["resources"])
    #print("estructuras: ", len(escena.p1.structures))
    for structure in escena.p1.structures + escena.p2.structures:
        #print(type(structure))
        structure.setTilesOcupados()
    for resource in escena.resources:
        coords = resource.getTile()
        tile = escena.mapa.mapa[coords[1]][coords[0]]
        #print(tile.tileid, type(resource))
        if tile.ocupante != None:
            #print(tile.ocupante)
            if tile.ocupante.type == REFINERY:
                #print("aaaaaaaaaaaaaa")
                tile.ocupante.resource = resource
                resource.disable()
    loadUnits(data["p2"]["units"], escena.p2, escena.mapa)
    loadUnits(data["p1"]["units"], escena.p1, escena.mapa)
    escena.p1.setBasePlayer(escena.p1.structures[0])
    escena.p2.setBasePlayer(escena.p2.structures[0])
    #print(escena.p2.limitUnits)
    return escena, raton, camera

def loadkeyShortcuts():
    textFile = open("atajos/atajos.json", "r")
    #print("atajos cargados")
    data = json.load(textFile)
    keyMap = loadKeyMap(data['keyMap'])
    commandMap = loadCommandMap(data['commandMap'])
    return keyMap, commandMap


def loadHardcodedMap(nombre):
    escena = Escena(None, None, None, None, None, None, None, None)

    textFile = open("maps/" + nombre + ".json", "r")
    data = json.load(textFile)

    #mapa
    escena.mapa = loadMap(data["mapa"])
    #players
    escena.p1 = loadPlayer(data["p1"], escena.mapa, True)
    escena.p2 = loadPlayer(data["p2"], escena.mapa, False)
    escena.walls = loadMuros(data["muros"], escena.mapa)
    # Raton
    raton = Raton.Raton(escena.p1, escena.p2, escena.mapa)


    raton.setEscena(escena)
    escena.raton = raton

    loadStructures(data["p1"]["structures"], escena.p1, escena.mapa, escena.raton)
    loadStructures(data["p2"]["structures"], escena.p2, escena.mapa, escena.raton)
    
    

    camera = loadCamera(data["camera"])
    escena.camera = camera

    escena.resources = loadResources(data["resources"])
    #print("estructuras: ", len(escena.p1.structures))
    for structure in escena.p1.structures + escena.p2.structures:
        #print(type(structure))
        structure.setTilesOcupados()
    for resource in escena.resources:
        coords = resource.getTile()
        tile = escena.mapa.mapa[coords[1]][coords[0]]
        #print(tile.tileid, type(resource))
        if tile.ocupante != None:
            #print(tile.ocupante)
            if tile.ocupante.type == REFINERY:
                #print("aaaaaaaaaaaaaa")
                tile.ocupante.resource = resource
                resource.disable()
    loadUnits(data["p2"]["units"], escena.p2, escena.mapa)
    loadUnits(data["p1"]["units"], escena.p1, escena.mapa)
    escena.p1.setBasePlayer(escena.p1.structures[0])
    escena.p2.setBasePlayer(escena.p2.structures[0])
    #print(escena.p2.limitUnits)
    return escena, raton, camera


#pre: mapDictionary es un diccionario con la info del mapa
#   map: mapa dela escena
#post: devuelve un Map
def loadMap(mapDictionary):
    m = Map.Map(mapDictionary["w"], mapDictionary["h"], True, mapDictionary["map"])
    m.loadOscuridad(mapDictionary["matrizOscuridad"])
    return m

#pre: playerDictionary es un diccionario con la info del jugador
#   map: mapa dela escena
#post: devuelve un Player
def loadPlayer(playerDictionary, map, isPlayer):
    p = Player.Player([], [], playerDictionary["resources"], {}, {}, map, isPlayer)
    keyMap, commandMap = loadkeyShortcuts();
    p.keyMap = keyMap
    p.commandMap = commandMap
    #loadKeyMap(playerDictionary["keyMap"], p)
    #loadCommandMap(playerDictionary["commandMap"], p)
    p.dañoUpgrade = playerDictionary["dañoUpgrade"]
    p.armorUpgrade = playerDictionary["armorUpgrade"]
    p.mineUpgrade = playerDictionary["mineUpgrade"]
    p.gas = playerDictionary["gas"]
    #p.limitUnits = playerDictionary["limitUnits"]
    return p

#pre: unitDictionaries: es una lista de diccionarios con la info de las unidades
#   player: es el jugador al que pertenecen
#post: ha añadido las unidades a player.units
def loadUnits(unitDictionaries, player, mapa):
    for u in unitDictionaries:
        if u["clase"] == "terranWorker":
            unit = TerranWorker(player, u["x"], u["y"])
            #print("cargo worker", u['x'], u['y'])
            unit.load(u["hp"])
            player.addUnits(unit)
        elif u["clase"] == "terranSoldier":
            unit = TerranSoldier(player, u["x"], u["y"])
            unit.load(u["hp"])
            player.addUnits(unit)
        elif u["clase"] == "zergling":
            unit = Zergling(player, u["x"], u["y"])
            unit.load(u["hp"])
            player.addUnits(unit)
        elif u["clase"] == "drone":
            unit = Drone(player, u["x"], u["y"])
            unit.load(u["hp"])
            player.addUnits(unit)
        elif u["clase"] == "hydralisk":
            unit = Hydralisk(player, u["x"], u["y"])
            unit.load(u["hp"])
            player.addUnits(unit)
        elif u["clase"] == "broodling":
            unit = Broodling(player, u["x"], u["y"])
            unit.load(u["hp"])
            player.addUnits(unit)
        elif u["clase"] == "firebat":
            unit = Firebat(player, u["x"], u["y"])
            unit.load(u["hp"])
            player.addUnits(unit)
        elif u["clase"] == "goliath":
            unit = Goliath(player, u["x"], u["y"])
            unit.load(u["hp"])
            player.addUnits(unit)
        
        try:
            #print("aaaaaaaaaaaa")
            unit.returnx = u['returnx']
            unit.returny = u['returny']
            #print("aaaaaaaaaaaa", u['disabled'])
            if u['disabled']:
                #print(mapa)
                #print(unit.returnx, unit.returny - 40)
                tile = mapa.getTile(unit.returnx, unit.returny - 40)
                #print("a extraer", tile.tileid)
                resource = tile.ocupante.resource
                #print(type(resource))
                unit.state = UnitState.EXTRACTING
                unit.resource = resource
                unit.isExtracting = True
                unit.enable = False
                unit.startTimeMining = 0
                unit.x = -5000
        except:
            pass

#post: ha añadido las unidades a player.units
def loadUnit(u, player):
        if u["clase"] == "terranWorker":
            unit = TerranWorker(player, u["x"], u["y"])
            unit.load(u["hp"])
            return unit
        elif u["clase"] == "terranSoldier":
            unit = TerranSoldier(player, u["x"], u["y"])
            unit.load(u["hp"])
            return unit
        elif u["clase"] == "zergling":
            unit = Zergling(player, u["x"], u["y"])
            unit.load(u["hp"])
            return unit
        elif u["clase"] == "drone":
            unit = Drone(player, u["x"], u["y"])
            unit.load(u["hp"])
            return unit
        elif u["clase"] == "hydralisk":
            unit = Hydralisk(player, u["x"], u["y"])
            unit.load(u["hp"])
            return unit
        elif u["clase"] == "broodling":
            unit = Broodling(player, u["x"], u["y"])
            unit.load(u["hp"])
            return unit
        elif u["clase"] == "firebat":
            unit = Firebat(player, u["x"], u["y"])
            unit.load(u["hp"])
            return unit
        elif u["clase"] == "goliath":
            unit = Goliath(player, u["x"], u["y"])
            unit.load(u["hp"])
            return unit

def loadMuros(wallDict, mapa):
    muros = []
    for u in wallDict:
        muros.append(Wall(u["type"] ,u["xIni"], u["yIni"], mapa))
    return muros



#pre: structureDictionaries: es una lista de diccionarios con la info de las estructuras
#   player: es el jugador al que pertenecen
#   map: el mapa de la escena
#post: ha añadido las estructuras a player.structures
def loadStructures(structureDictionaries, player, map, raton):
    for s in structureDictionaries:
        if s["clase"] == "terranBuilder":
            structure = TerranBuilder(s["x"], s["y"], player, map, s["building"], raton)
            structure.damageMineralUpCost = s["damageMineralUpCost"]
            structure.damageGasUpCost = s["damageGasUpCost"]
            structure.armorMineralUpCost = s["armorMineralUpCost"]
            structure.armorGasUpCost = s["armorGasUpCost"]
            structure.mineMineralUpCost = s["mineMineralUpCost"]
            structure.mineGasUpCost = s["mineGasUpCost"]
            player.setBasePlayer(structure)
        elif s["clase"] == "terranBarracks":
            structure = TerranBarracks(s["x"], s["y"], player, map, s["building"])
        elif s["clase"] == "hatchery":
            structure = Hatchery(s["x"], s["y"], player, map, s["building"], raton)
            structure.damageMineralUpCost = s["damageMineralUpCost"]
            structure.damageGasUpCost = s["damageGasUpCost"]
            structure.armorMineralUpCost = s["armorMineralUpCost"]
            structure.armorGasUpCost = s["armorGasUpCost"]
            structure.mineMineralUpCost = s["mineMineralUpCost"]
            structure.mineGasUpCost = s["mineGasUpCost"]
            player.setBasePlayer(structure)
        elif s["clase"] == "terranSupplyDepot":
            structure = TerranSupplyDepot(s["x"], s["y"], player, map, s["building"])
        elif s["clase"] == "terranRefinery":
            structure = TerranRefinery(s["x"], s["y"], player, map, s["building"])
        elif s["clase"] == "extractor":
            structure = Extractor(s["x"], s["y"], player, map, s["building"])
        elif s["clase"] == "zergBarracks":
            structure = ZergBarracks(s["x"], s["y"], player, map, s["building"])
        elif s["clase"] == "zergSupply":
            structure = ZergSupply(s["x"], s["y"], player, map, s["building"])
        for unit in s["training"]:
            structure.training.append(loadUnit(unit, player))
        structure.state = s['state']
        structure.hp = s['hp']
        structure.generationCount = s['count']
        player.addStructures(structure)
        player.limitUnits += structure.getUnitCapacity()
        structure.updateUpgrade()

#en el fichero la clave es una string, hay que hacer uno nuevo con clave numerica
def loadKeyMap(stringKeyKeyMap):
    stringKeyItems = stringKeyKeyMap.items()
    keyMap = {}
    for i in stringKeyItems:
        keyMap[int(i[0])] = i[1]
    return keyMap

def loadCommandMap(stringKeyCommandMap):
    stringKeyItems = stringKeyCommandMap.items()
    commandMap = {}
    for i in stringKeyItems:
        commandMap[int(i[0])] = i[1]
    return commandMap

# pre: mapa al menos tan grande como ventana (si no undefined behavior)
def loadCamera(cameraDictionary):
    return Camera(cameraDictionary["x"], cameraDictionary["y"],
        cameraDictionary["h"], cameraDictionary["w"])

def loadResources(resourcesDictionary):
    resources = []
    #print("pero bueno", resourcesDictionary)

    for r in resourcesDictionary:
        if r["clase"] == "cristal":
            #print(r["clase"], r["x"], r["y"], r["capacidad"])
            resources.append(Crystal(r["x"], r["y"], r["capacidad"]))
        if r["clase"] == "geyser":
            #print(r["clase"],r["capacidad"], r["x"], r["y"])
            resources.append(Geyser(r["x"], r["y"], r["capacidad"]))
    for r in resources:
        #print("hola")
        #print(r.x, r.y)
        pass
    return resources
