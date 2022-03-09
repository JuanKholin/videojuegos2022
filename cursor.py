from email.mime import image
from pygame.locals import *
import pygame, sys, math, time

# Definir colores

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

size =(SCREEN_WIDTH,SCREEN_HEIGHT)

sprite_ruta = "./SPRITE/raton/"
kurisu_dir = "kurisu.png"
dvd_dir = "dvd.png" 


def moveXY(rect1, rect2):
    x = rect2.x - rect1.x
    y = rect2.y - rect1.y
    angle = math.atan2(y, x) * (180.0 / math.pi)
    return math.sin(math.radians(angle)), math.cos(math.radians(angle))

def collide(rect1, rect2):
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
            if self.frame > 10:
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

class raton(pygame.sprite.Sprite):
    #Constructor
    sprite = []
    sprite2 = []
    index = 0
    index2 = 0
    frame = 0
    clicked = False
    collide = False
    def __init__(self, ruta):
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
        
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - self.rect.width/2
        self.rect.y = pos[1] - self.rect.height/2
        type = pygame.mouse.get_pressed()
        if type[0]:
            self.image = self.clickSprite
        elif self.collide:
            self.frame += 1
            if self.frame > 10:
                self.index2 = (self.index2+1)%14
                self.index = (self.index+1)%5
                self.image = self.sprite2[self.index2]
                self.frame = 0
        else:
            self.frame += 1
            if self.frame > 10:
                self.index = (self.index+1)%5
                self.index2 = (self.index2+1)%14
                self.image = self.sprite[self.index]
                self.frame = 0
    
    def click(self):
        self.clicked = not self.clicked

    def setCollide(self, detected):
        self.collide = detected
            
        


#Clase meteoro(Sub clase de Sprite)
class imagen(pygame.sprite.Sprite):
    imageW = 0
    imageH = 0
    clicked = False
    moveX = 1
    moveY = 1
    haveDest = False
    #Constructor
    def __init__(self, ruta, x, y, speed):
        super().__init__()
        self.image = pygame.image.load(ruta).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect() #Para posicionar el sprite
        self.rect.x = x
        self.rect.y = y
        self.posX = self.rect.x
        self.posY = self.rect.y
        self.speed = speed

    def update(self):
        if self.haveDest and (self.distanceX > 0 or self.distanceY > 0):
            self.posX += self.moveX
            self.posY += self.moveY
            self.distanceX -= abs(self.moveX)
            self.distanceY -= abs(self.moveY)
            self.rect.x = self.posX
            self.rect.y = self.posY
        else:
            self.haveDest = False
    def setNewDestination(self, x, y):
        if self.clicked:
            self.distanceX = abs(x - self.rect.x)
            self.distanceY = abs(y - self.rect.y)
            self.haveDest = True
    def setSpeed(self, sX, sY):
        if self.clicked:
            self.moveX = self.speed*sX
            self.moveY = self.speed*sY
            print(self.moveX, self.moveY)

        
        
        

def main():
    pygame.init()
    screen =  pygame.display.set_mode(size, pygame.RESIZABLE)

    kurisu = imagen(kurisu_dir, 100, 100, 5)
    dvd = imagen(dvd_dir, 200, 200, 2)
    mouse = raton(sprite_ruta)
    p = point(sprite_ruta)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while True:
        ###---LOGICA
        #Actualizar objetos
        screen.fill((BLACK))

        pos = pygame.mouse.get_pos()    
    
        mouseRect = pygame.Rect(pos[0], pos[1], 1, 1)
        if collide(kurisu.rect, mouseRect):
            mouse.setCollide(True)
        elif collide(mouseRect, dvd.rect):
            mouse.setCollide(True)
        else:
            mouse.setCollide(False)

        kurisu.update()
        dvd.update()
        p.update()
        mouse.update()
            
        screen.blit(kurisu.image, (kurisu.rect.x, kurisu.rect.y))
        screen.blit(dvd.image, (dvd.rect.x, dvd.rect.y))
        if p.getClicked():
            screen.blit(p.image, (p.rect.x, p.rect.y))
        screen.blit(mouse.image, (mouse.rect.x, mouse.rect.y))
            
        ###--- ZONA DE DIBUJO
        #ACtualizar pantalla
        pygame.display.flip()
        clock.tick(120)   

        for event in pygame.event.get(): #Identificar lo sucedido en la ventana
            #print(event)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                SCREEN_HEIGHT = event.h
                SCREEN_WIDTH = event.w
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                type = pygame.key.get_pressed()
                if type[K_SPACE]:
                    kurisu.update()
                    dvd.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                type = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()
                if type[0]: 
                    mouseRect = pygame.Rect(pos[0], pos[1], 1, 1)
                    if collide(kurisu.rect, mouseRect):
                        print("kurisu clicked")
                        kurisu.clicked = True
                        dvd.clicked = False
                    elif collide(mouseRect, dvd.rect):
                        print("dvd clicked")
                        dvd.clicked = True
                        kurisu.clicked = False
                    else:
                        dvd.clicked = False
                        kurisu.clicked = False
                if type[2]:
                    p.click(pos[0], pos[1])
                    kurisu.setNewDestination(pos[0]-(kurisu.rect.width/2), pos[1]-(kurisu.rect.height/2))
                    y, x = moveXY(kurisu.rect, pygame.Rect(pos[0]-(kurisu.rect.width/2), pos[1]-(kurisu.rect.height/2), 1, 1))
                    kurisu.setSpeed(x, y)
                    dvd.setNewDestination(pos[0]-(dvd.rect.width/2), pos[1]-(dvd.rect.height/2))
                    y, x = moveXY(dvd.rect, pygame.Rect(pos[0]-(dvd.rect.width/2), pos[1]-(dvd.rect.height/2), 1, 1))
                    dvd.setSpeed(x, y)             
            if event.type == pygame.MOUSEBUTTONUP:
                print('click liberado', pos[0], pos[1], event.type)
                
                      


if __name__ == "__main__":
    main()
