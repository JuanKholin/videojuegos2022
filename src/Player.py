
from operator import truediv
import pygame as pg
import math
from . import Utils
from .Command import *
from .Utils import *


class Player():
    def __init__(self, units, structures, resources, keyMap, commandMap, mapa, isPlayer):
        #Atributos
        self.isPlayer = isPlayer
        self.units = units
        self.unitsSelected = []
        self.enemySelected = []
        self.structureSelected = None
        self.enemyStructureSelected = None
        self.resourceSelected = None
        self.structures = structures
        self.resources = resources
        self.gas = 0
        self.keyMap = keyMap
        self.commandMap = commandMap #keyMap pero las claves son los valores y los valores las claves (solo necesario para las teclas de la camara)
        self.pulsado = False
        self.initialX = 0
        self.initialY = 0
        self.mapa = mapa
        self.dañoUpgrade = 0
        self.armorUpgrade = 0
        self.mineUpgrade = 0

        self.limitUnits = 3

        # Para la IA
        self.unitsFree = []

    def setBasePlayer(self, base):
        self.base = base

    def processEvent(self, event):
        if self.isPlayer:
            if event.type == pg.KEYDOWN:
                if event.key in self.keyMap:
                    if self.structureSelected != None:
                        command = self.structureSelected.command(self.keyMap[event.key])
                        if command != Command(CommandId.NULL):
                                return command
                    return Command(self.keyMap[event.key])
        return Command(CommandId.NULL)


    def update(self):
        for unit in self.units:
            unit.update()
        for structure in self.structures:
            structure.update()

    def addUnits(self,unit):
        self.units.append(unit)
        self.unitsFree.append(unit)

    def addStructures(self,structures):
        #print(self.limitUnits)
        self.limitUnits += structures.getUnitCapacity()
        
        self.structures.append(structures)

    def execute(self, id, param, tileClicked):
        #print("Soy player, ", self.isPlayer)
        if id == CommandId.MOVE: #Mover unidades
            for i in range(param.__len__()):
                self.unitsSelected[i].paths = param[i]
                #for path in param[i]:
                    #print("Posicion final: ",path.posFin, path.angle)
        elif id == CommandId.ORDER:
            for i in range(param.__len__()):
                #print(param[i]['order'])
                #self.unitsSelected[i].paths = param[i]['path']
                # En funcion de la orden cambiarle el estado a la unidad
                if self.unitsSelected[i].state != UnitState.DEAD and self.unitsSelected[i].state != UnitState.DYING:
                    if param[i]['order'] == CommandId.MINE:
                        self.unitsSelected[i].mine(param[i]['resource'])
                    elif param[i]['order'] == CommandId.MOVE:
                        self.unitsSelected[i].move(tileClicked)
                    elif param[i]['order'] == CommandId.EXTRACT_GAS:
                        self.unitsSelected[i].extract(tileClicked)
                    elif param[i]['order'] == CommandId.ATTACK:
                        if self.unitsSelected[i].state == UnitState.STILL or self.unitsSelected[i].state == UnitState.ATTACKING:
                            self.unitsSelected[i].attack(param[i]['attackedOne'])
                        else:
                            self.unitsSelected[i].siendoAtacado = True
                            self.unitsSelected[i].atacante = param[i]['attackedOne']
                    else:
                        self.unitsSelected[i].updateOwnSpace()
        elif id == CommandId.SEARCH_NEARBY_RIVAL:
            #print("BUSCAR")
            for unit in self.unitsSelected:
                enemy = self.mapa.getNearbyRival(unit.occupiedTile, self)
                #print(type(enemy))
                if enemy != None:
                    if unit.state == UnitState.STILL:
                        unit.attack(enemy)
                    else:
                        #print("ataco a otro")
                        unit.siendoAtacado = True
                        unit.atacante = enemy
                        #print(unit.atacante)
                else:
                    if unit.state == UnitState.STILL:
                        unit.updateOwnSpace()
                    #print("no hay naide")
        elif self.structureSelected != None:
            if id == CommandId.GENERATE_UNIT or id == CommandId.GENERATE_WORKER or id == CommandId.GENERATE_T1:
                self.structureSelected.execute(id)
            elif id == CommandId.BUILD_BARRACKS:
                #print("EXECUCION")
                self.structureSelected.execute(id)
            elif id == CommandId.BUILD_REFINERY:
                self.structureSelected.execute(id)
            elif id == CommandId.GENERATE_T2:
                self.structureSelected.execute(id)
            elif id == CommandId.GENERATE_T3:
                self.structureSelected.execute(id)
            elif id == CommandId.BUILD_DEPOT:
                self.structureSelected.execute(id)
            elif id == CommandId.BUILD_HATCHERY:
                self.structureSelected.execute(id)
            elif id == CommandId.UPGRADE_SOLDIER_DAMAGE:
                self.structureSelected.execute(id)
            elif id == CommandId.UPGRADE_SOLDIER_ARMOR:
                self.structureSelected.execute(id)
            elif id == CommandId.UPGRADE_WORKER_MINING:
                self.structureSelected.execute(id)

    def draw(self, screen, camera):
        for structure in self.structures:
            r = structure.getRect()
            #si cae en los limites de la camara dibujar.
            if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
            r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
                #aqui llamabais a el draw de structures, me lo he cargado para integrar lo que había hecho con la camara
                #luego lo vuelvo a poner
                structure.draw(screen, camera)
        for unit in self.units:
            r = unit.getRect()
            if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
            r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
                unit.draw(screen, camera)

    def drawEntity(self, screen, camera,  isMe):
        if isMe:
            for structure in self.structures:
                r = structure.getRect()
                if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
                    r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
                    pos = structure.getPosition()
                    pygame.draw.rect(screen, BLUE, pygame.Rect(Utils.ScreenWidth/2 - MINIMAP_X + (pos[0]/self.mapa.w * MINIMAP_W), Utils.ScreenHeight - MINIMAP_Y + (pos[1]/self.mapa.h * MINIMAP_H), 8, 5))
            for unit in self.units:
                if unit.state != UnitState.DEAD:
                    r = structure.getRect()
                    if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
                        r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
                        pos = unit.getPosition()
                        pygame.draw.rect(screen, GREEN, pygame.Rect(Utils.ScreenWidth/2 - MINIMAP_X + (pos[0]/self.mapa.w * MINIMAP_W), Utils.ScreenHeight - MINIMAP_Y + (pos[1]/self.mapa.h * MINIMAP_H), 3, 3))
        else:
            for structure in self.structures:
                pos = structure.getPosition()
                if self.mapa.getTile(pos[0], pos[1]).visible:
                    pygame.draw.rect(screen, ORANGE, pygame.Rect(Utils.ScreenWidth/2 - MINIMAP_X + (pos[0]/self.mapa.w * MINIMAP_W), Utils.ScreenHeight - MINIMAP_Y + (pos[1]/self.mapa.h * MINIMAP_H), 8, 5))
            for unit in self.units:
                if unit.state != UnitState.DEAD:
                    pos = unit.getPosition()
                    if (self.mapa.getTile(pos[0], pos[1]) != None) and self.mapa.getTile(pos[0], pos[1]).visible:
                        pygame.draw.rect(screen, RED, pygame.Rect(Utils.ScreenWidth/2 - MINIMAP_X + (pos[0]/self.mapa.w * MINIMAP_W), Utils.ScreenHeight - MINIMAP_Y + (pos[1]/self.mapa.h * MINIMAP_H), 3, 3))


    def removeUnit(self, unit):
        self.unitsSelected.remove(unit)

    def removeUnitFromFree(self, unit):
        self.unitsFree.remove(unit)

    # Para que la AI pueda acceder a la informacion
    def get_info(self):
        return self.unitsFree, self.structures

    def toDictionary(self, map):
        return {
            "units": [u.toDictionary(map) for u in self.units],
            "structures": [s.toDictionary(map) for s in self.structures],
            "resources": self.resources,
            "keyMap": self.keyMap,
            "commandMap": self.commandMap,
            "dañoUpgrade": self.dañoUpgrade,
            "armorUpgrade": self.armorUpgrade,
            "mineUpgrade": self.mineUpgrade,
            "limitUnits": self.limitUnits
        }

    def getMapa(self):
        return self.mapa

    #devuelve las coordenadas de las entidades que ve la camara
    def getEntitesLocation(self, camera):
        locations = []
        for u in self.units:
            if (u.x > (camera.x - VISION_RADIUS_PIXELS) and u.x < (camera.x + camera.w + VISION_RADIUS_PIXELS)
                    and u.y > (camera.y - VISION_RADIUS_PIXELS) and u.y < (camera.y + camera.h + VISION_RADIUS_PIXELS)):
                location = (u.x, u.y)
                locations.append(location)
        for s in self.structures:
            if (s.x > (camera.x - VISION_RADIUS_PIXELS) and s.x < (camera.x + camera.w + VISION_RADIUS_PIXELS)
                    and s.y > (camera.y - VISION_RADIUS_PIXELS) and s.y < (camera.y + camera.h + VISION_RADIUS_PIXELS)):
                location = (s.x, s.y)
                locations.append(location)
        return locations
