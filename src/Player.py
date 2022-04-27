import pygame, math
from . import Command, Utils


class Player():
    def __init__(self, units, structures, resources, keyMap, commandMap):
        #Atributos
        self.units = units
        self.unitsSelected = []
        self.structuresSelected = []
        self.structures = structures
        self.resources = resources
        self.keyMap = keyMap
        self.commandMap = commandMap #keyMap pero las claves son los valores y los valores las claves (solo necesario para las teclas de la camara)
        self.pulsado = False
        self.initialX = 0
        self.initialY = 0

    def processEvent(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.keyMap:
                for structure in self.structuresSelected:
                    command = structure.command(self.keyMap[event.key])
                    if command != Command.Command(Command.CommandId.NULO):
                        return command
                return Command.Command(self.keyMap[event.key])
        return Command.Command(Command.CommandId.NULO)


    def update(self):
        for structure in self.structures:
            structure.update()
        for unit in self.units:
            unit.update()

    def addUnits(self,unit):
        self.units.append(unit)

    def addStructures(self,structures):
        self.structures.append(structures)

    def execute(self,id, param):
        if id == Command.CommandId.MOVER: #Mover unidades
            for i in range(param.__len__()):
                self.unitsSelected[i].paths = param[i]
                #for path in param[i]:
                    #print("Posicion final: ",path.posFin, path.angle)
        elif id == Command.CommandId.ORDENAR:
            for i in range(param.__len__()):
                #print("ME han mandado:" ,param[i])
                self.unitsSelected[i].paths = param[i]['path']
                self.unitsSelected[i].setOrder(param[i])
        elif id == Command.CommandId.GENERAR_UNIDAD:
            for i in self.structuresSelected:
                print("structura ", i.id)
                i.execute(id)
        elif id == Command.CommandId.BUILD_BARRACKS:
            for i in self.structuresSelected:
                i.execute(id)

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
            #print(r)
            pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x - camera.x, r.y  - camera.y, r.w, r.h),1)
            if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
            r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
                drawPos = unit.getDrawPosition()
                if unit.clicked:
                    pygame.draw.ellipse(screen, Utils.GREEN, [r.x - camera.x, r.y + (0.7*r.h)- camera.y,r.w , 0.3*r.h], 2)
                #screen.blit(unit.image, [r.x - camera.x, r.y - camera.y])
                screen.blit(unit.image, [drawPos[0] - camera.x, drawPos[1] - camera.y])
                if unit.clicked:
                    hp = pygame.transform.chop(pygame.transform.scale(Utils.HP, (50, 8)), ((unit.hp/unit.maxHp) * 50, 0, 50, 0))
                    screen.blit(hp, [unit.x - camera.x - hp.get_rect().w/2, unit.y + r.h/2 - camera.y])

    # Para que la AI pueda acceder a la informacion
    def get_info(self):
        return self.units, self.structures, self.resources

    def toDictionary(self, map):
        return {
            "units": [u.toDictionary(map) for u in self.units],
            "structures": [s.toDictionary(map) for s in self.structures],
            "resources": self.resources,
            "keyMap": self.keyMap,
            "commandMap": self.commandMap,
        }
