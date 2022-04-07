import pygame, math

from . import Command
from . import Player


GREEN   = (0,255,0)

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
class raton(pygame.sprite.Sprite):
    #Constructor
    sprite = []
    sprite2 = []
    index = 0
    index2 = 0
    frame = 0
    clicked = False
    collide = False
    pulsado = False
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
        
    def update(self, cameraX, cameraY):
        self.point.update()
        self.rel_pos = pygame.mouse.get_pos()
        self.real_pos = (self.rel_pos[0] + cameraX, self.rel_pos[1] + cameraY)
        self.rect.x = self.rel_pos[0] - self.rect.width/2
        self.rect.y = self.rel_pos[1] - self.rect.height/2

        #la posicion del cursor es relativa a la camara (por que tiene dos rectangulos? (self.rect y mouseRect))
        mouseRect = pygame.Rect(self.real_pos[0], self.real_pos[1], 1, 1)
        mouse_collide = False
        for unit in self.player.units:
            ###---LOGICA
            r = unit.getRect()
            #pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camarax, r.y - camaray, r.w, r.h),1)
            if Player.collides(self.real_pos[0], self.real_pos[1],unit.getRect()):
                mouse_collide = True
        for structure in self.player.structures:
            ###---LOGICA
            #pygame.draw.rect(screen, BLACK, pygame.Rect(r.x - camarax, r.y - camaray, r.w, r.h),1)
            if Player.collides(self.real_pos[0], self.real_pos[1],structure.getRect()):
                mouse_collide = True

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
    
    def click(self):
        self.clicked = not self.clicked

    def setCollide(self, detected):
        self.collide = detected
    def draw(self, screen, camera):
        if self.point.getClicked() :
            self.point.draw(screen, camera)
        if self.pulsado:
            printRectangulo(screen, self.initialX - camera.x, self.initialY - camera.y, self.rel_pos[0], self.rel_pos[1])
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def processEvent(self, event, cameraX, cameraY):
        command = Command.Command(0) # 0 es nada
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_type = pygame.mouse.get_pressed()
            #la posicion del cursor es relativa a la camara
            relative_mouse_pos = pygame.mouse.get_pos()
            real_mouse_pos = (relative_mouse_pos[0] + cameraX, relative_mouse_pos[1] + cameraY)
            #print(relative_mouse_pos)
            
            if click_type[0]:     
                if not self.pulsado:
                    self.pulsado = True                    
                    self.initialX = real_mouse_pos[0] 
                    self.initialY = real_mouse_pos[1]
            if click_type[2]:
                if not self.pulsado:
                    command.setId(1)
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
                    #print('click izq liberado', mouse_pos[0], mouse_pos[1], event.type)
                    mouseRect = Player.createRect(self.initialX, self.initialY, real_mouse_pos[0], real_mouse_pos[1])
                    for unit in self.player.units:
                        #print(unit.getRect())
                        if Player.collides(self.real_pos[0], self.real_pos[1],unit.getRect()):
                            unit.setClicked(True)
                            self.player.unitsSelected.append(unit)
                            
                            #print("CLICKADO" + str(terran.id))
                        else:
                            unit.setClicked(False)
                            if unit in self.player.unitsSelected:
                                self.player.unitsSelected.remove(unit)
                            #unitsClicked.remove(terran)
                            #print("DESCLICKADO" + str(terran.id)) 
                    for structure in self.player.structures:
                        if Player.collides(self.real_pos[0], self.real_pos[1],structure.getRect()):
                            structure.setClicked(True)
                            #self.player.unitsSelected.append(unit)
                            
                            #print("CLICKADO" + str(terran.id))
                        else:
                            structure.setClicked(False)
                            #if unit in self.player.unitsSelected:
                            #    self.player.unitsSelected.remove(unit)
                            #unitsClicked.remove(terran)
                            #print("DESCLICKADO" + str(terran.id)) 
            if type[2]:
                print('click der liberado', real_mouse_pos[0], real_mouse_pos[1], event.type)
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