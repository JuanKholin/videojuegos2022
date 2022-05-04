import pygame, math
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

        # Para la IA
        self.unitsFree = []
    
    def setBasePlayer(self, base):
        self.base = base

    def processEvent(self, event):
        if self.isPlayer:
            if event.type == pygame.KEYDOWN:
                if event.key in self.keyMap:
                    if self.structureSelected != None:
                        command = self.structureSelected.command(self.keyMap[event.key])
                        if command != Command(CommandId.NULO):
                                return command
                    return Command(self.keyMap[event.key])
        return Command(CommandId.NULO)


    def update(self):
        for unit in self.units:
            unit.update()
        for structure in self.structures:
            structure.update()

    def addUnits(self,unit):
        self.units.append(unit)
        self.unitsFree.append(unit)


    def addStructures(self,structures):
        self.structures.append(structures)

    def execute(self, id, param, tileClicked):
        print("Soy player, ", self.isPlayer)
        if id == CommandId.MOVER: #Mover unidades
            for i in range(param.__len__()):
                self.unitsSelected[i].paths = param[i]
                #for path in param[i]:
                    #print("Posicion final: ",path.posFin, path.angle)
        elif id == CommandId.ORDENAR:
            for i in range(param.__len__()):
                print(param[i]['order'])
                self.unitsSelected[i].paths = param[i]['path']
                # En funcion de la orden cambiarle el estado a la unidad
                if param[i]['order'] == CommandId.MINE:
                    self.unitsSelected[i].mine(param[i]['resource'])
                elif param[i]['order'] == CommandId.MOVER:
                    self.unitsSelected[i].move(tileClicked)
                elif param[i]['order'] == CommandId.EXTRACT_GAS:
                    self.unitsSelected[i].extract(tileClicked)
                elif param[i]['order'] == CommandId.ATTACK:
                    self.unitsSelected[i].attack(param[i]['attackedOne'])
        elif self.structureSelected != None:
            if id == CommandId.GENERAR_UNIDAD or id == CommandId.GENERATE_WORKER or id == CommandId.GENERATE_SOLDIER:
                self.structureSelected.execute(id)
            elif id == CommandId.BUILD_BARRACKS:
                self.structureSelected.execute(id)
            elif id == CommandId.BUILD_REFINERY:
                self.structureSelected.execute(id)
            elif id == CommandId.BUILD_HATCHERY:
                self.structureSelected.execute(id)
            elif id == CommandId.MEJORAR_DAÑO_SOLDADO:
                self.structureSelected.execute(id)
            elif id == CommandId.MEJORAR_ARMADURA_SOLDADO:
                self.structureSelected.execute(id)
            elif id == CommandId.MEJORAR_MINADO_WORKER:
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
                
    def drawEntity(self, screen, isMe):
        if isMe:
            for structure in self.structures:
                pos = structure.getPosition()
                pygame.draw.rect(screen, BLUE, pygame.Rect(MINIMAP_X + (pos[0]/self.mapa.w * MINIMAP_W), MINIMAP_Y + (pos[1]/self.mapa.h * MINIMAP_H), 8, 5))
            for unit in self.units:
                if unit.state != UnitState.DEAD:
                    pos = unit.getPosition()
                    pygame.draw.rect(screen, GREEN, pygame.Rect(MINIMAP_X + (pos[0]/self.mapa.w * MINIMAP_W), MINIMAP_Y + (pos[1]/self.mapa.h * MINIMAP_H), 3, 3))    
        else:
            for structure in self.structures:
                pos = structure.getPosition()
                pygame.draw.rect(screen, ORANGE, pygame.Rect(MINIMAP_X + (pos[0]/self.mapa.w * MINIMAP_W), MINIMAP_Y + (pos[1]/self.mapa.h * MINIMAP_H), 8, 5))
            for unit in self.units:
                if unit.state != UnitState.DEAD:
                    pos = unit.getPosition()
                    pygame.draw.rect(screen, RED, pygame.Rect(MINIMAP_X + (pos[0]/self.mapa.w * MINIMAP_W), MINIMAP_Y + (pos[1]/self.mapa.h * MINIMAP_H), 3, 3))    


    def removeUnit(self, unit):
        self.unitsSelected.remove(unit)

    def removeUnitFromFree(self, unit):
        self.unitsFree.remove(unit)

    # Para que la AI pueda acceder a la informacion
    def get_info(self):
        return self.unitsFree, self.structures, self.resources

    def toDictionary(self, map):
        return {
            "units": [u.toDictionary(map) for u in self.units],
            "structures": [s.toDictionary(map) for s in self.structures],
            "resources": self.resources,
            "keyMap": self.keyMap,
            "commandMap": self.commandMap,
        }

    def getMapa(self):
        return self.mapa