import pygame, math

from . import Command
from . import Utils
from . import Player

def collides(x, y, rect2):
    return (x >= rect2.x and x <= rect2.x + rect2.w and y >= rect2.y and y <= rect2.y + rect2.h )

def collideRect(rect1, rect2):
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

def printRectangulo(screen, initialX, initialY, finalX, finalY):
    if finalX>=initialX and finalY>=initialY:
        pygame.draw.rect(screen, Utils.GREEN, [initialX, initialY, finalX-initialX, finalY-initialY], 1)
    elif finalX>=initialX and finalY<initialY:
        pygame.draw.rect(screen, Utils.GREEN, [initialX, finalY, finalX-initialX, initialY-finalY], 1)
    elif finalX<initialX and finalY>=initialY:
        pygame.draw.rect(screen, Utils.GREEN, [finalX, initialY, initialX-finalX, finalY-initialY], 1)
    else: #finalX<initialX and finalY<initialY
        pygame.draw.rect(screen, Utils.GREEN, [finalX, finalY, initialX-finalX, initialY-finalY], 1)


#FUNCIONES DEL RATON
class Raton(pygame.sprite.Sprite):
    #Constructor
    sprite = []
    sprite2 = []
    index = 0
    index2 = 0
    frame = 0
    initialX = 0
    initialY = 0
    clicked = False
    collide = False
    pulsado = False
    building = False
    buildStructure = None
    def __init__(self, ruta, player):
        super().__init__()
        self.index = 0
        for i in range(5):
            self.sprite.append(pygame.image.load(ruta+"tile00"+str(i)+".png").convert_alpha())
        for i in range(14):
            j = i+34
            self.sprite2.append(pygame.image.load(ruta+"tile0"+str(j)+".png").convert_alpha())
        self.clickSprite = pygame.image.load(ruta+"click.png").convert_alpha()
        self.image = self.sprite[0]
        self.rect = self.image.get_rect() #Para posicionar el sprite
        pygame.mouse.set_visible(False)
        self.point = point(ruta)
        self.player = player

    def update(self, camera):
        self.point.update()
        self.rel_pos = pygame.mouse.get_pos()
        self.real_pos = (self.rel_pos[0] + camera.x, self.rel_pos[1] + camera.y)
        self.rect.x = self.rel_pos[0] - self.rect.width/2
        self.rect.y = self.rel_pos[1] - self.rect.height/2

        #la posicion del cursor es relativa a la camara (por que tiene dos rectangulos? (self.rect y mouseRect))
        #mouseRect = pygame.Rect(self.real_pos[0], self.real_pos[1], 1, 1)
        mouse_collide = False
        if not self.building:
            for unit in self.player.units:
                ###---LOGICA
                #pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camarax, r.y - camaray, r.w, r.h),1)
                if collides(self.real_pos[0], self.real_pos[1], unit.getRect()):
                    mouse_collide = True
                    break
            if not mouse_collide:
                for structure in self.player.structures:
                    ###---LOGICA
                    #pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camarax, r.y - camaray, r.w, r.h),1)
                    if collides(self.real_pos[0], self.real_pos[1],structure.getRect()):
                        mouse_collide = True
                        break
        else:
            self.buildStructure.setPosition(self.real_pos[0], self.real_pos[1])

        if mouse_collide:
            self.collide = True
        else:
            self.collide = False


        type = pygame.mouse.get_pressed()
        if type[0]:
            self.image = self.clickSprite
        elif self.collide:
            self.frame += 1
            if self.frame > 5:
                self.index2 = (self.index2+1)%14
                self.index = (self.index+1)%5
                self.image = self.sprite2[self.index2]
                self.frame = 0
        else:
            self.frame += 1
            if self.frame > 5:
                self.index = (self.index+1)%5
                self.index2 = (self.index2+1)%14
                self.image = self.sprite[self.index]
                self.frame = 0

    def getPosition(self):
        return self.real_pos

    def getClick(self):
        return self.clicked

    def getPressed(self):
        return self.pulsado, (self.initialX, self.initialY)

    def setCollide(self, detected):
        self.collide = detected

    def isCollide(self, rect):
        return collides(self.real_pos[0], self.real_pos[1], rect)

    def click(self):
        self.clicked = not self.clicked

    def draw(self, screen, camera):
        if Utils.state == Utils.System_State.ONGAME:
            if self.building:
                self.buildStructure.drawBuildStructure(screen, camera)
            else:
                if self.point.getClicked():
                    self.point.draw(screen, camera)
                if self.pulsado:
                    printRectangulo(screen, self.initialX - camera.x, self.initialY - camera.y, self.rel_pos[0], self.rel_pos[1])
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.sprite[self.index], (self.rect.x, self.rect.y))

    def processEvent(self, event, cameraX, cameraY):
        command = Command.Command(Command.CommandId.NULO) # 0 es nada
        self.clicked = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_type = pygame.mouse.get_pressed()
            #la posicion del cursor es relativa a la camara
            relative_mouse_pos = pygame.mouse.get_pos()
            real_mouse_pos = (relative_mouse_pos[0] + cameraX, relative_mouse_pos[1] + cameraY)
            #print(relative_mouse_pos)

            if click_type[0]:
                if not self.pulsado:
                    self.pulsado = True
                    if not self.building:
                        self.initialX = real_mouse_pos[0]
                        self.initialY = real_mouse_pos[1]
            if click_type[2]:
                if not self.pulsado:
                    if not self.building:
                        command.setId(Command.CommandId.MOVER)
                        #print("CALCULANDO PUNTOS")
                        for unit in self.player.unitsSelected:
                            pos = unit.getPosition()
                            command.addParameter(pos)
                        self.point.click(real_mouse_pos[0], real_mouse_pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            type = pygame.mouse.get_pressed()
            relative_mouse_pos = pygame.mouse.get_pos()
            real_mouse_pos = (relative_mouse_pos[0] + cameraX, relative_mouse_pos[1] + cameraY)
            #print('click liberado', type)
            
            if not type[0]:
                if self.pulsado:
                    self.pulsado = False
                    self.clicked = True
                    print('click izq liberado', real_mouse_pos, event.type)
                    if self.building:
                        if self.buildStructure.checkTiles():
                            print(self.buildStructure.checkTiles())
                            self.buildStructure.player = self.player
                            self.player.addStructures(self.buildStructure)
                            self.building = False
                    else:
                        unitSel = False
                        selectedUnit = self.player.unitsSelected
                        selectedStructures = self.player.structuresSelected
                        self.player.unitsSelected = []
                        self.player.structuresSelected = []
                        isClick = False

                        mouseRect = createRect(self.initialX, self.initialY, real_mouse_pos[0], real_mouse_pos[1])

                        for unit in self.player.units:
                            #print(unit.getRect())
                            if len(self.player.unitsSelected) < Utils.MAX_SELECTED_UNIT and collideRect(mouseRect, unit.getRect()):
                                unit.setClicked(True)
                                self.player.unitsSelected.append(unit)
                                unitSel = True
                                #print("CLICKADO" + str(terran.id))
                        if not unitSel:
                            for structure in self.player.structures:
                                if collideRect(mouseRect, structure.getRect()):
                                    structure.setClicked(True)
                                    unitSel = True
                                    self.player.structuresSelected.append(structure)
                                    #print("CLICKADO ")
                                    break

                        if unitSel:
                            for unit in self.player.units + self.player.structures:
                                if unit not in self.player.unitsSelected + self.player.structuresSelected:
                                    #print(unit)
                                    unit.setClicked(False)
                        else:
                            self.player.unitsSelected = selectedUnit
                            self.player.structuresSelected = selectedStructures

                elif not type[2]:
                    print('click der liberado', real_mouse_pos[0], real_mouse_pos[1], event.type)
                    if self.building:
                        self.buildStructure = None
                        self.building = False
        return command

class point(pygame.sprite.Sprite):
    #Constructor
    sprite = []
    index = 0
    frame = 0
    clicked = False
    realX = 0
    realY = 0
    def __init__(self, ruta):
        super().__init__()
        self.index = 0
        for i in range(5):
            self.sprite.append(pygame.image.load(ruta+"point"+str(i)+".png").convert_alpha())
        self.image = self.sprite[0]
        self.rect = self.image.get_rect() #Para posicionar el sprite

    def update(self):
        if self.clicked:
            self.frame += 1
            if self.frame > 5:
                self.index = self.index+1
                self.image = self.sprite[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.realX-self.rect.width/2
                self.rect.y = self.realY-self.rect.height/2
                self.frame = 0
            if self.index == 4:
                self.clicked = False

    def click(self, x, y):
        self.clicked = True
        self.index = 0
        self.realX = x
        self.realY = y
        self.rect.x = x-self.rect.width/2
        self.rect.y = y-self.rect.height/2

    def getClicked(self):
        return self.clicked

    def draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y))
