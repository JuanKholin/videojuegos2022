import pygame,math
from .. import Command
class path():
    def __init__(self, angle, dist):
        self.angle = angle
        self.dist = dist

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

class Player():
    def __init__(self, units, structures, resources, keyMap):
        #Atributos
        self.units = units
        self.unitsSelected = []
        self.structures = structures
        self.resources = resources
        self.keyMap = keyMap
    def processEvent(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_type = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            
            if click_type[0]:     
                if not pulsado:
                    pulsado = True
                    initialX = mouse_pos[0]
                    initialY = mouse_pos[1]
            if click_type[2]:
                if not pulsado:
                    command = Command.Command(Command.CommandId(MOVER)) # 1 es moverse
                    #print("CALCULANDO PUNTOS")
                    for unit in self.unitsSelected:
                        rect = unit.getRect()
                        pos = (rect.x,rect.y)
                        command.addParameter(pos)
                    return command
        
    def update():
        pass
    def addUnits(self,unit):
        self.units.append(unit)
    def addStructures(self,structures):
        self.structures.append(structures)
