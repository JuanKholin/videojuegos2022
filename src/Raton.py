import pygame, math
from . import Command, Utils
from . import Player
from .Utils import *
from .Lib import *
from .Music import *

def collides(x, y, rect2):
    return (x >= rect2.x and x <= rect2.x + rect2.w and y >= rect2.y and y <= rect2.y + rect2.h)

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
        pygame.draw.rect(screen, GREEN, [initialX, initialY, finalX-initialX, finalY-initialY], 1)
    elif finalX>=initialX and finalY<initialY:
        pygame.draw.rect(screen, GREEN, [initialX, finalY, finalX-initialX, initialY-finalY], 1)
    elif finalX<initialX and finalY>=initialY:
        pygame.draw.rect(screen, GREEN, [finalX, initialY, initialX-finalX, finalY-initialY], 1)
    else: #finalX<initialX and finalY<initialY
        pygame.draw.rect(screen, GREEN, [finalX, finalY, initialX-finalX, initialY-finalY], 1)


#FUNCIONES DEL RATON
class Raton(pygame.sprite.Sprite):
    #Constructor
    sprite = []
    sprite2 = []
    index = 0
    index2 = 0
    initialX = 0
    initialY = 0
    clicked = False
    collideAlly = False
    collideEnemy = False
    collideResourse = False
    pulsado = False
    derPulsado = False
    building = False
    buildStructure = None
    def __init__(self, player, enemy, mapa):
        super().__init__()
        self.index = 0
        self.sprite = cargarSprites(MOUSE_PATH + "tile00", 5, False, WHITE) #raton default
        self.sprite2 = cargarSprites(MOUSE_PATH + "tile0", 48, True, WHITE, m=34) #raton selectedUnit
        self.sprite3 = cargarSprites(MOUSE_PATH + "tile0", 82, True, WHITE, m=68) #raton selectedEnemy
        self.sprite4 = cargarSprites(MOUSE_PATH + "tile0", 65, True, WHITE, m=51) #raton selectedMineral

        self.clickSprite = pygame.image.load(MOUSE_PATH + "click.png").convert_alpha()
        self.image = self.sprite[0]
        self.rect = self.image.get_rect() #Para posicionar el sprite
        pygame.mouse.set_visible(False)
        self.point = point(MOUSE_PATH)
        self.player = player
        self.enemy = enemy
        self.escena = None
        self.enable = True
        self.interface = None
        self.mapa = mapa
        self.id = takeID()
        #print("raton: ", self.id)

    def update(self, camera):
        self.point.update()
        self.rel_pos = pygame.mouse.get_pos()
        self.real_pos = (self.rel_pos[0] + camera.x, self.rel_pos[1] + camera.y)
        self.rect.x = self.rel_pos[0] - self.rect.width / 2
        self.rect.y = self.rel_pos[1] - self.rect.height / 2

        if Utils.state2 == System_State.PLAYING:
            #la posicion del cursor es relativa a la camara (por que tiene dos rectangulos? (self.rect y mouseRect))
            #mouseRect = pygame.Rect(self.real_pos[0], self.real_pos[1], 1, 1)
            mouse_collide = False
            self.collideAlly = False
            self.collideResourse = False
            self.collideEnemy = False

            if not self.building:
                if self.enable:
                    for unit in self.player.units:
                        ###---LOGICA
                        #pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camarax, r.y - camaray, r.w, r.h),1)
                        if collides(self.real_pos[0], self.real_pos[1], unit.getRect()):
                            self.collideAlly = True
                            mouse_collide = True
                            break
                    if not mouse_collide:
                        for structure in self.player.structures:
                            ###---LOGICA
                            #pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camarax, r.y - camaray, r.w, r.h),1)
                            if collides(self.real_pos[0], self.real_pos[1], structure.getRect()):
                                self.collideAlly = True
                                mouse_collide = True
                                break
                    if not mouse_collide:
                        for unit in self.enemy.units:
                            ###---LOGICA
                            #pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camarax, r.y - camaray, r.w, r.h),1)
                            if (self.mapa.getTile(self.real_pos[0], self.real_pos[1]).visible
                                    and collides(self.real_pos[0], self.real_pos[1], unit.getRect())):
                                self.collideEnemy = True
                                mouse_collide = True
                                break
                    if not mouse_collide:
                        for structure in self.enemy.structures:
                            ###---LOGICA
                            #pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camarax, r.y - camaray, r.w, r.h),1)
                            if (self.mapa.getTile(self.real_pos[0], self.real_pos[1]).visible
                                    and collides(self.real_pos[0], self.real_pos[1], structure.getRect())):
                                self.collideEnemy = True
                                mouse_collide = True
                                break
                    if not mouse_collide:
                        for resources in self.escena.resources:
                            ###---LOGICA
                            #pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camarax, r.y - camaray, r.w, r.h),1)
                            if (self.mapa.getTile(self.real_pos[0], self.real_pos[1]).visible
                                    and collides(self.real_pos[0], self.real_pos[1], resources.getRect())):
                                self.collideResourse = True
                                mouse_collide = True
                                break
            else:
                self.buildStructure.setPosition(self.real_pos[0], self.real_pos[1])

            type = pygame.mouse.get_pressed()
            if type[0]:
                self.image = self.clickSprite
            else:
                if frame(6) == 1:
                    self.index = (self.index+1)%5
                    self.index2 = (self.index2+1)%14
                if self.collideAlly:
                    self.image = self.sprite2[self.index2]
                elif self.collideEnemy:
                    self.image = self.sprite3[self.index2]
                elif self.collideResourse:
                    self.image = self.sprite4[self.index2]
                else:
                    self.image = self.sprite[self.index]
        else:
            self.image = self.sprite[self.index]

        #if DEBBUG:
        #    if frame(360) == 1:
        #        #print(self.rel_pos[0], self.rel_pos[1])
        if Utils.state == System_State.ONGAME:
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                minimapRect = createRect(MINIMAP_X, MINIMAP_Y, MINIMAP_X + MINIMAP_W, MINIMAP_Y + MINIMAP_H)
                if collides(mouse_pos[0], mouse_pos[1], minimapRect):
                    camera.setX(((mouse_pos[0]-MINIMAP_X)/MINIMAP_W*self.player.mapa.w) - camera.w/2, self.player.mapa.w)
                    camera.setY(((mouse_pos[1]-MINIMAP_Y)/MINIMAP_H*self.player.mapa.h) - camera.h/2, self.player.mapa.h)

    def setSelf(self, raton):
        self.player = raton.player
        self.enemy = raton.enemy
        self.mapa = raton.mapa

    def getPosition(self):
        return self.real_pos

    def getClick(self):
        return self.clicked

    def getPressed(self):
        return self.pulsado, (self.initialX, self.initialY)

    def setEscena(self, escena):
        self.escena = escena

    def setCollide(self, detected):
        self.collide = detected

    def isCollide(self, rect):
        return collides(self.real_pos[0], self.real_pos[1], rect)

    def click(self):
        self.clicked = not self.clicked

    def setEnable(self, enable):
        self.enable = enable

    def addInterface(self, interface):
        self.interface = interface

    def draw(self, screen, camera):
        if Utils.state == System_State.ONGAME:
            if self.building:
                self.buildStructure.setPosition(self.real_pos[0], self.real_pos[1])
            else:
                if self.point.getClicked():
                    self.point.draw(screen, camera)
                if self.pulsado and self.enable:
                    printRectangulo(screen, self.initialX - camera.x, self.initialY - camera.y, self.rel_pos[0], self.rel_pos[1])
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.sprite[self.index], (self.rect.x, self.rect.y))

    def drawBuildStructure(self, screen, camera):
        if self.buildStructure != None:
            self.buildStructure.drawBuildStructure(screen, camera)


    def processEvent(self, event, camera):
        command = Command.Command(Command.CommandId.NULL) # 0 es nada
        self.clicked = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_type = pygame.mouse.get_pressed()
            #la posicion del cursor es relativa a la camara
            relative_mouse_pos = pygame.mouse.get_pos()
            real_mouse_pos = (relative_mouse_pos[0] + camera.x, relative_mouse_pos[1] + camera.y)
            #print(relative_mouse_pos)

            if click_type[0]:
                if not self.pulsado:
                    self.pulsado = True
                    if Utils.state2 == System_State.WIN or Utils.state2 == System_State.GAMEOVER:
                        setGameState(System_State.MAINMENU)
                        setGameState2(System_State.PLAYING)
                    else:
                        if not self.building:
                            self.initialX = real_mouse_pos[0]
                            self.initialY = real_mouse_pos[1]

            if click_type[2]:
                if not self.derPulsado:
                    self.derPulsado = True
                    if Utils.state2 == System_State.WIN or Utils.state2 == System_State.GAMEOVER:
                        setGameState(System_State.MAINMENU)
                        setGameState2(System_State.PLAYING)
                    else:
                        if not self.building and self.enable:
                            command.setId(Command.CommandId.MOVE)
                            #print("CALCULANDO PUNTOS")
                            for unit in self.player.unitsSelected:
                                pos = unit.getPosition()
                                command.addParameter(pos)
                            self.point.click(real_mouse_pos[0], real_mouse_pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            type = pygame.mouse.get_pressed()
            relative_mouse_pos = pygame.mouse.get_pos()
            real_mouse_pos = (relative_mouse_pos[0] + camera.x, relative_mouse_pos[1] + camera.y)
            #print('click liberado', type)

            if not type[0]:
                if self.pulsado:
                    self.pulsado = False
                    self.clicked = True
                    print('click izq liberado', real_mouse_pos, event.type)
                    #print(self.enable)
                    if Utils.state == System_State.ONGAME:
                        if getGameState2() == System_State.PLAYING:
                            reClick = False
                            if self.enable:
                                if collides(self.rel_pos[0], self.rel_pos[1], self.interface.pauseButton.getRect()):
                                    command = self.interface.pauseButton.getCommand()
                                    return command
                                tileClicked = self.mapa.getTile(real_mouse_pos[0],real_mouse_pos[1])
                                if tileClicked.ocupante == None:
                                    tileClicked = self.mapa.getTile(real_mouse_pos[0],real_mouse_pos[1] + 40)
                                if tileClicked.ocupante != None:
                                    unidadClickada = tileClicked.ocupante
                                    if unidadClickada.getType() != -1:
                                        if unidadClickada.clicked: # Seleccionar todos los del mismo tipo
                                            reClick = True
                                            self.player.unitsSelected = []
                                            self.player.unitsSelected.append(unidadClickada) 
                                            left = 7
                                            for unit in self.player.units:
                                                if left == 0:
                                                    break
                                                elif unidadClickada != unit:
                                                    if unidadClickada.getType() == unit.getType() :
                                                        unit.setClicked(True)
                                                        self.player.unitsSelected.append(unit)
                                            left -= 1
                                if reClick == False:
                                    if self.building:
                                        if self.buildStructure.checkTiles() and self.player.resources >= self.buildStructure.mineralCost:
                                            self.player.resources -= self.buildStructure.mineralCost
                                            self.buildStructure.player = self.player
                                            self.player.addStructures(self.buildStructure)
                                            self.buildStructure.buildProcess()
                                            self.building = False
                                            self.buildStructure = None
                                            playSound(construirSound)
                                    else:
                                        unitSel = False
                                        selectedUnit = self.player.unitsSelected
                                        selectedEnemy = self.player.enemySelected
                                        selectedStructures = self.player.structureSelected
                                        selectedEnemyStructures = self.player.enemyStructureSelected
                                        selectedResources = self.player.resourceSelected
                                        self.player.unitsSelected = []
                                        self.player.enemySelected = []
                                        self.player.structureSelected = None
                                        self.player.enemyStructureSelected = None
                                        self.player.selectedResources = None

                                        mouseRect = createRect(self.initialX, self.initialY, real_mouse_pos[0], real_mouse_pos[1])

                                        for unit in self.player.units:
                                            if len(self.player.unitsSelected) < MAX_SELECTED_UNIT and collideRect(mouseRect, unit.getRect()):
                                                unit.setClicked(True)
                                                self.player.unitsSelected.append(unit)
                                                unitSel = True
                                                #print("CLICKADO" + str(terran.id))
                                                self.player.resourceSelected = None

                                        if not unitSel:
                                            for unit in self.enemy.units:
                                                #print(unit.getRect())
                                                pos = unit.getPosition()
                                                if (collideRect(mouseRect, unit.getRect()) and 
                                                        self.mapa.getTile(pos[0] - camera.x, pos[1] - camera.y).visible):
                                                    unit.setClicked(True)
                                                    self.player.enemySelected.append(unit)
                                                    unitSel = True
                                                    #print("CLICKADO" + str(terran.id))
                                                    self.player.resourceSelected = None
                                                    break

                                        if not unitSel:
                                            for structure in self.player.structures:
                                                if collideRect(mouseRect, structure.getRect()):
                                                    playSound(structure.selectedSound)
                                                    structure.setClicked(True)
                                                    unitSel = True
                                                    self.player.structureSelected = structure
                                                    #print("CLICKADO ")
                                                    self.player.resourceSelected = None
                                                    break

                                        if not unitSel:
                                            for structure in self.enemy.structures:
                                                pos = structure.getPosition()
                                                if (collideRect(mouseRect, structure.getRect())
                                                        and self.mapa.getTile(pos[0], pos[1]).visible):
                                                    structure.setClicked(True)
                                                    unitSel = True
                                                    self.player.enemyStructureSelected = structure
                                                    #print("CLICKADO ")
                                                    self.player.resourceSelected = None
                                                    break

                                        if not unitSel:
                                            for resource in self.escena.resources:
                                                pos = resource.getPosition()
                                                if (collideRect(mouseRect, resource.getRect())
                                                        and self.mapa.getTile(pos[0], pos[1]).visible):
                                                    resource.setClicked(True)
                                                    unitSel = True
                                                    self.player.resourceSelected = resource
                                                    #print("CLICKADO aaaa")
                                                    break

                                        if unitSel:
                                            for unit in (self.player.units + self.player.structures + self.enemy.units + self.enemy.structures + self.escena.resources):
                                                if unit not in (self.player.unitsSelected + self.player.enemySelected + [self.player.structureSelected] + [self.player.enemyStructureSelected] + [self.player.resourceSelected]):
                                                    #print(unit)
                                                    unit.setClicked(False)
                                        else:
                                            self.player.unitsSelected = selectedUnit
                                            self.player.enemySelected = selectedEnemy
                                            self.player.structuresSelected = selectedStructures
                                            self.player.enemyStructuresSelected = selectedEnemyStructures
                                            self.player.resourceSelected = selectedResources
                            else: #si estoy en GUI
                                #comprobar colision con los botones
                                for b in self.interface.button:
                                    if collides(self.rel_pos[0], self.rel_pos[1], b.getRect()):
                                        command = b.getCommand()
                                        #print(command.id)
                                        break
                        elif getGameState2() == System_State.HELP:
                            for b in self.interface.helpButtons:
                                if b != None and collides(self.rel_pos[0], self.rel_pos[1], b.getRect()):
                                    command = b.getCommand()
                                    #print(command.id)
                                    break
                        elif getGameState2() == System_State.PAUSED:
                            for b in self.interface.pauseButtons:
                                if b != None and collides(self.rel_pos[0], self.rel_pos[1], b.getRect()):
                                    command = b.getCommand()
                                    #print(command.id)
                                    break

                elif not type[2]:
                    if self.derPulsado:
                        #print('click der liberado', real_mouse_pos[0], real_mouse_pos[1], event.type)
                        self.derPulsado = False
                        if self.enable:
                            if self.building:
                                self.buildStructure = None
                                self.building = False
        return command

class point(pygame.sprite.Sprite):
    #Constructor
    sprite = []
    index = 0
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
            if frame(6) == 1:
                self.index = self.index+1
                self.image = self.sprite[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.realX-self.rect.width/2
                self.rect.y = self.realY-self.rect.height/2
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
