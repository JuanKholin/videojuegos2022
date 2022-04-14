import pygame,math
from . import Command, Utils


def createRect(initialX, initialY, finalX, finalY):
    if finalX>=initialX and finalY>=initialY:
        area = pygame.Rect(initialX, initialY, finalX-initialX, finalY-initialY)
    elif finalX>=initialX and finalY<initialY:
        area = pygame.Rect(initialX, finalY, finalX-initialX, initialY-finalY)
    elif finalX<initialX and finalY>=initialY:
        area = pygame.Rect(finalX, initialY, initialX-finalX, finalY-initialY)
    else: #finalX<initialX and finalY<initialY
        area = pygame.Rect(finalX, finalY, initialX-finalX, initialY-finalY)
    return area

def collides(x,y, rect2):
    return (x >= rect2.x and x <= rect2.x + rect2.w and y >= rect2.y and y <= rect2.y + rect2.h )


class Player():
    def __init__(self, units, structures, resources, keyMap, commandMap):
        #Atributos
        self.units = units
        self.unitsSelected = []
        self.structures = structures
        self.resources = resources
        self.keyMap = keyMap
        self.commandMap = commandMap #keyMap pero las claves son los valores y los valores las claves (solo necesario para las teclas de la camara)
        self.pulsado = False
        self.initialX = 0
        self.initialY = 0

    def processEvent(self,event):
        for structure in self.structures:
            structure.processEvent(event)
        if event.type == pygame.KEYDOWN:
            if event.key in self.keyMap:
                return Command.Command(self.keyMap[event.key])
        return Command.Command(0)

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
                for path in param[i]:
                    print("Posicion final: ",path.posFin, path.angle)
        elif id == Command.CommandId.ORDENAR:
            for i in range(param.__len__()):
                print("ME han mandado:" ,param[i])
                self.unitsSelected[i].setOrder(param[i])
    def draw(self, screen, camera):
        for structure in self.structures:
            r = structure.getRect()
            #si cae en los limites de la camara dibujar.
            if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
            r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
                pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x - camera.x, r.y - camera.y, r.w, r.h),1)
                #aqui llamabais a el draw de structures, me lo he cargado para integrar lo que había hecho con la camara
                #luego lo vuelvo a poner
                image = structure.getImage()
                if structure.clicked:
                    pygame.draw.ellipse(screen, Utils.GREEN, [structure.x-structure.rectn.w/2 - camera.x, structure.y+structure.rectOffY-structure.rectn.h/2 - camera.y, structure.rectn.w, structure.rectn.h], 2)
                screen.blit(structure.image, [image.x - camera.x, image.y - camera.y])
                hp = Utils.HP
                hp = pygame.transform.scale(hp, (50, 8))
                hp = pygame.transform.chop(hp, ((structure.hp/structure.maxHp) * 50, 0, 50, 0))
                screen.blit(hp, [structure.x - camera.x - 25, structure.y+structure.rectOffY+structure.rectn.h/2 - 10 - camera.y])
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

    # Para que la AI pueda acceder a la informacion
    def get_info(self):
        return self.units, self.structures, self.resources
