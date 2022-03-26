import pygame,math
from . import Command

BLACK   = (0,0,0)

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

def collides(rect1, rect2):
    collideX = False
    collideY = False
    if (rect1.x >= rect2.x) and (rect1.x <= (rect2.x+rect2.width)):
        collideX = True
    elif (rect2.x >= rect1.x) and (rect2.x <= (rect1.x+rect1.width)):
        collideX = True
    if (rect1.y >= rect2.y) and (rect1.y <= (rect2.y+rect2.height)):
        collideY = True
    elif (rect2.y >= rect1.y) and (rect2.y <= (rect1.y+rect1.height)):
        collideY = True
    return collideX and collideY

class Player():
    def __init__(self, units, structures, resources, keyMap):
        #Atributos
        self.units = units
        self.unitsSelected = []
        self.structures = structures
        self.resources = resources
        self.keyMap = keyMap
        self.pulsado = False
        self.initialX = 0
        self.initialY = 0
    def processEvent(self,event):
        command = Command.Command(0) # 0 es nada
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_type = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            
            if click_type[0]:     
                if not self.pulsado:
                    self.pulsado = True
                    self.initialX = mouse_pos[0]
                    self.initialY = mouse_pos[1]
            if click_type[2]:
                if not self.pulsado:
                    command.setId(1)
                    #print("CALCULANDO PUNTOS")
                    for unit in self.unitsSelected:
                        rect = unit.getRect()
                        pos = (rect.x,rect.y)
                        command.addParameter(pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            type = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()  
            #print('click liberado', type)
            if not type[0]:   
                if self.pulsado: 
                    self.pulsado = False
                    #print('click izq liberado', mouse_pos[0], mouse_pos[1], event.type)
                    mouseRect = createRect(self.initialX, self.initialY, mouse_pos[0], mouse_pos[1])
                    for unit in self.units:
                        if collides(unit.getRect(), mouseRect):
                            unit.setClicked(True)
                            self.unitsSelected.append(unit)
                            
                            #print("CLICKADO" + str(terran.id))
                        else:
                            unit.setClicked(False)
                            #unitsClicked.remove(terran)
                            #print("DESCLICKADO" + str(terran.id)) 
            if type[2]:
                print('click der liberado', mouse_pos[0], mouse_pos[1], event.type)
        return command
        
    def update(self):
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
    def draw(self, screen):
        for unit in self.units:
            r = unit.getRect()
            pygame.draw.rect(screen, BLACK, pygame.Rect(r.x, r.y, r.w, r.h),1)
            screen.blit(unit.image, [r.x, r.y])
