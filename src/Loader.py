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

def loadFromSave(nombre):
    escena = Escena(None, None, None, None, None, None, None, None)

    textFile = open("games/" + nombre + ".json", "r")
    data = json.load(textFile)

    #mapa
    escena.mapa = loadMap(data["mapa"])
    #players
    escena.p1 = loadPlayer(data["p1"], escena.mapa, True)
    escena.p2 = loadPlayer(data["p2"], escena.mapa, False)

    # Raton
    raton = Raton.Raton(escena.p1, escena.p2, escena.mapa)
   
    
    raton.setEscena(escena)
    escena.raton = raton
    

    loadUnits(data["p1"]["units"], escena.p1)
    loadStructures(data["p1"]["structures"], escena.p1, escena.mapa, escena.raton)
    loadUnits(data["p2"]["units"], escena.p2)
    loadStructures(data["p2"]["structures"], escena.p2, escena.mapa, escena.raton)

    camera = loadCamera(data["camera"])
    escena.camera = camera

    escena.resources = loadResources(data["resources"])

    escena.p1.setBasePlayer(escena.p1.structures[0])

    return escena, raton, camera


#pre: mapDictionary es un diccionario con la info del mapa
#   map: mapa dela escena
#post: devuelve un Map
def loadMap(mapDictionary):
    m = Map.Map(mapDictionary["w"], mapDictionary["h"], True, mapDictionary["map"])
    m.loadOscuridad(mapDictionary["matrizOscuridad"])
    return m

#pre: playerDictionarie es un diccionario con la info del jugador
#   map: mapa dela escena
#post: devuelve un Player
def loadPlayer(playerDictionary, map, isPlayer):
    p = Player.Player([], [], playerDictionary["resources"], {}, {}, map, isPlayer)
    loadKeyMap(playerDictionary["keyMap"], p)
    loadCommandMap(playerDictionary["commandMap"], p)
    return p

#pre: unitDictionaries: es una lista de diccionarios con la info de las unidades
#   player: es el jugador al que pertenecen
#post: ha añadido las unidades a player.units
def loadUnits(unitDictionaries, player):
    for u in unitDictionaries:
        if u["clase"] == "terranWorker":
            unit = TerranWorker(u["x"], u["y"], player)
            unit.load(u["hp"])
            player.addUnits(unit)
        elif u["clase"] == "terranSoldier":
            unit = TerranSoldier(u["x"], u["y"], player)
            unit.load(u["hp"])
            player.addUnits(unit)
        elif u["clase"] == "zergling":
            unit = Zergling(u["x"], u["y"], player)
            unit.load(u["hp"])
            player.addUnits(unit)
        elif u["clase"] == "drone":
            unit = Drone(u["x"], u["y"], player)
            unit.load(u["hp"])
            player.addUnits(unit)



#pre: structureDictionaries: es una lista de diccionarios con la info de las estructuras
#   player: es el jugador al que pertenecen
#   map: el mapa de la escena
#post: ha añadido las estructuras a player.structures
def loadStructures(structureDictionaries, player, map, raton):
    for s in structureDictionaries:
        if s["clase"] == "terranBuilder":
            player.addStructures(TerranBuilder(s["x"], s["y"], player, map, s["building"], raton))
        elif s["clase"] == "terranBarracks":
            player.addStructures(TerranBarracks(s["x"], s["y"], player, map, s["building"]))
        elif s["clase"] == "hatchery":
            player.addStructures(Hatchery(s["x"], s["y"], player, map, s["building"]))
        elif s["clase"] == "terranSupplyDepot":
            player.addStructures(TerranSupplyDepot(s["x"], s["y"], player, map, s["building"]))
        elif s["clase"] == "terranRefinery":
            player.addStructures(TerranRefinery(s["x"], s["y"], player, map, s["building"]))
        elif s["clase"] == "extractor":
            player.addStructures(Extractor(s["x"], s["y"], player, map, s["building"]))

#en el fichero la clave es una string, hay que hacer uno nuevo con clave numerica
def loadKeyMap(stringKeyKeyMap, p):
    stringKeyItems = stringKeyKeyMap.items()
    keyMap = {}
    for i in stringKeyItems:
        keyMap[int(i[0])] = i[1]
    p.keyMap = keyMap

def loadCommandMap(stringKeyCommandMap, p):
    stringKeyItems = stringKeyCommandMap.items()
    commandMap = {}
    for i in stringKeyItems:
        commandMap[int(i[0])] = i[1]
    p.commandMap = commandMap

# pre: mapa al menos tan grande como ventana (si no undefined behavior)
def loadCamera(cameraDictionary):
    return Camera(cameraDictionary["x"], cameraDictionary["y"],
        cameraDictionary["h"], cameraDictionary["w"])

def loadResources(resourcesDictionary):
    resources = []
    print("pero bueno", resourcesDictionary)

    for r in resourcesDictionary:
        if r["clase"] == "cristal":
            print(r["clase"], r["x"], r["y"], r["capacidad"])
            resources.append(Crystal(r["x"], r["y"], r["capacidad"]))
        if r["clase"] == "geyser":
            print(r["clase"],r["capacidad"], r["x"], r["y"])
            resources.append(Geyser(r["x"], r["y"], r["capacidad"]))
    for r in resources:
        print("hola")
        print(r.x, r.y)
    return resources
