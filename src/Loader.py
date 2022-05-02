from .Map import *
from .Player import *
from .Camera import *
from .Entities.Crystal import *
from .Entities.TerranWorker import *
from .Entities.TerranBuilder import *
from .Entities.TerranSoldier import *
from .Entities.TerranBarracks import *
from .Entities.Hatchery import *
from .Entities.Drone import *
from .Entities.Zergling import *


#pre: mapDictionary es un diccionario con la info del mapa
#   map: mapa dela escena
#post: devuelve un Map
def loadMap(mapDictionary):
    m = Map.Map(mapDictionary["w"], mapDictionary["h"], mapDictionary["map"], False)
    return m

#pre: playerDictionarie es un diccionario con la info del jugador
#   map: mapa dela escena
#post: devuelve un Player
def loadPlayer(playerDictionary, map):
    p = Player.Player([], [], playerDictionary["resources"], {}, {})
    loadUnits(playerDictionary["units"], p)
    loadStructures(playerDictionary["structures"], p, map)
    loadKeyMap(playerDictionary["keyMap"], p)
    loadCommandMap(playerDictionary["commandMap"], p)
    return p

#pre: unitDictionaries: es una lista de diccionarios con la info de las unidades
#   player: es el jugador al que pertenecen
#post: ha añadido las unidades a player.units
def loadUnits(unitDictionaries, player):
    for u in unitDictionaries:
        if u["clase"] == "terranWorker":
            player.addUnits(TerranWorker(u["x"], u["y"], player))
        elif u["clase"] == "terranSoldier":
            player.addUnits(TerranSoldier(u["x"], u["y"], player))
        elif u["clase"] == "zergling":
            player.addUnits(Zergling(u["x"], u["y"], player))
        elif u["clase"] == "drone":
            player.addUnits(Drone(u["x"], u["y"], player))

#pre: structureDictionaries: es una lista de diccionarios con la info de las estructuras
#   player: es el jugador al que pertenecen
#   map: el mapa de la escena
#post: ha añadido las estructuras a player.structures
def loadStructures(structureDictionaries, player, map):
    for s in structureDictionaries:
        if s["clase"] == "terranBuilder":
            player.addStructures(TerranBuilder(s["x"], s["y"], player, map, s["building"], s["id"]))
        elif s["clase"] == "terranBarracks":
            player.addStructures(TerranBarracks(s["x"], s["y"], player, map, s["building"], s["id"]))
        elif s["clase"] == "hatchery":
            player.addStructures(Hatchery(s["x"], s["y"], player, map, s["id"]))
        elif s["clase"] == "zergBuilder":
            player.addStructures(Hatchery(s["x"], s["y"], player, map, s["building"], s["id"]))

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

def loadResources(resuorcesDictionary):
    resources = []
    for r in resuorcesDictionary:
        if r["clase"] == "cristal":
            resources.append(Cristal(r["capacidad"], r["tipo"], r["x"], r["y"]))
    return resources
