import pygame, sys, random, time
import math

pygame.init()

# Definir colores

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

size =(SCREEN_WIDTH,SCREEN_HEIGHT)

def collides(rect1, rect2):
    print("RECTANGULO 1", rect1.x, rect1.y, rect1.w, rect1.h)
    print("RECTANGULO 2", rect2.x, rect2.y, rect2.w, rect2.h)
    if (rect1.x + rect1.w) >= rect2.x and  (rect1.x + rect1.w) <= (rect2.x + rect2.w) and (rect1.y + rect1.h) >= rect2.y and  (rect1.y + rect1.h) <= (rect2.y + rect2.h):
        return True
    if (rect1.x + rect1.w) >= rect2.x and  (rect1.x + rect1.w) <= (rect2.x + rect2.w) and (rect1.y + rect1.h) >= rect2.y and  rect1.y <= (rect2.y + rect2.h):
        return True
    if rect1.x >= rect2.x and  rect1.x <= (rect2.x + rect2.w) and rect1.y >= rect2.y and  rect1.y <= (rect2.y + rect2.h):
        return True
    if rect1.x >= rect2.x and  rect1.x <= (rect2.x + rect2.w) and (rect1.y + rect1.h) >= rect2.y and  (rect1.y + rect1.h) <= (rect2.y + rect2.h):
        return True
    return False
class rect():
    def __init__(self):
        pass
    def setDim(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Terran(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        #ATRIBUTOS
        self.rectOffY = 8
        self.clicked = False
        self.angle = 0
        self.speed = speed
        self.face = 0
        self.frame = 0
        self.framesToRefresh = 5
        self.count = 0
        self.sprites = []
        self.dirX = 0
        self.dirY = 0
        self.distanceToPoint = 0


        #INICIALIZACION DE LOS MISMOS
        for i in range(16):
            self.sprites.insert(i,[])
        for i in range(72):
            if i < 10:
                nPath = "0" + str(i)
            else:
                nPath = i
            if i%9 != 0 and i%9 != 8:
                self.sprites[16-(i%9)].insert(int(i/9),pygame.transform.flip(pygame.image.load("terranSprites/tile0" + str(nPath) + ".png"),True,False))
            self.sprites[i%9].insert(int(i/9),pygame.image.load("terranSprites/tile0" + str(nPath) + ".png"))
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(WHITE)
        self.rectn = rect()
        self.rectn.w = self.image.get_width()
        self.rectn.h = self.image.get_height() - self.rectOffY
        self.rectn.x = SCREEN_WIDTH/2 + self.rectn.w/2
        self.rectn.y = SCREEN_HEIGHT/2 + self.rectn.h

        self.prevX = self.rectn.x
        self.prevY = self.rectn.y

    def isClicked(self):
        return self.clicked
    def setClicked(self, click):
        self.clicked = click
    def update(self):
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(WHITE)
        self.resize()
        if self.distanceToPoint > 0:
            distrec = math.hypot((self.rectn.x + self.dirX*self.speed) - self.rectn.x, (self.rectn.y + self.dirY*self.speed) - self.rectn.y)
            self.distanceToPoint -= distrec
            self.rectn.x += self.dirX*self.speed
            self.rectn.y += self.dirY*self.speed
            self.count += 1
            if self.count >= self.framesToRefresh:
                self.frame = (self.frame + 1)%8
                self.count = 0
        else:
            self.frame = 6
            self.face = 8
            
                
                
    def resize(self):
        self.rectn.x -= self.rectn.w
        self.rectn.y -= self.rectn.h
        self.image = pygame.transform.scale2x(self.image)
        self.rectn.w = self.image.get_width()
        self.rectn.h = self.image.get_height() - self.rectOffY
        self.rectn.x += self.rectn.w
        self.rectn.y += self.rectn.h
    
    def getRect(self):
        rectAux = rect()
        rectAux.x = self.rectn.x - self.rectn.w/2
        rectAux.y = self.rectn.y - self.rectn.h
        rectAux.w = self.rectn.w
        rectAux.h = self.rectn.h
        return rectAux

class TerranGeneric(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        #ATRIBUTOS
        self.rectOffY = 8
        self.clicked = False
        self.angle = 0
        self.speed = speed
        self.face = 0
        self.frame = 0
        self.framesToRefresh = 5
        self.count = 0
        self.sprites = []
        self.dirX = 0
        self.dirY = 0
        self.distanceToPoint = 0


        #INICIALIZACION DE LOS MISMOS
        for i in range(16):
            self.sprites.insert(i,[])
        for i in range(72):
            if i < 10:
                nPath = "0" + str(i)
            else:
                nPath = i
            if i%9 != 0 and i%9 != 8:
                self.sprites[16-(i%9)].insert(int(i/9),pygame.transform.flip(pygame.image.load("terranSprites/tile0" + str(nPath) + ".png"),True,False))
            self.sprites[i%9].insert(int(i/9),pygame.image.load("terranSprites/tile0" + str(nPath) + ".png"))
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(WHITE)
        self.rectn = rect()
        self.rectn.w = self.image.get_width()
        self.rectn.h = self.image.get_height() - self.rectOffY
        self.rectn.x = SCREEN_WIDTH/2 + self.rectn.w/2
        self.rectn.y = SCREEN_HEIGHT/2 + self.rectn.h

        self.prevX = self.rectn.x
        self.prevY = self.rectn.y

    def isClicked(self):
        return self.clicked
    def setClicked(self, click):
        self.clicked = click
    def update(self):
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(WHITE)
        self.resize()
        if self.distanceToPoint > 0:
            distrec = math.hypot((self.rectn.x + self.dirX*self.speed) - self.rectn.x, (self.rectn.y + self.dirY*self.speed) - self.rectn.y)
            self.distanceToPoint -= distrec
            self.rectn.x += self.dirX*self.speed
            self.rectn.y += self.dirY*self.speed
            self.count += 1
            if self.count >= self.framesToRefresh:
                self.frame = (self.frame + 1)%8
                self.count = 0
        else:
            self.frame = 6
            self.face = 8
            
                
                
    def resize(self):
        self.rectn.x -= self.rectn.w
        self.rectn.y -= self.rectn.h
        self.image = pygame.transform.scale2x(self.image)
        self.rectn.w = self.image.get_width()
        self.rectn.h = self.image.get_height() - self.rectOffY
        self.rectn.x += self.rectn.w
        self.rectn.y += self.rectn.h
    
    def getRect(self):
        rectAux = rect()
        rectAux.x = self.rectn.x - self.rectn.w/2
        rectAux.y = self.rectn.y - self.rectn.h
        rectAux.w = self.rectn.w
        rectAux.h = self.rectn.h
        return rectAux

screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()

terran = Terran(2)

terran.resize()
while True:
    rectM = rect()

    for event in pygame.event.get(): #Identificar lo sucedido en la ventana
        #print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_type = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            rectM.x = mouse_pos[0]
            print(rectM.x)
            rectM.y = mouse_pos[1]
            print(rectM.y)
            rectM.h = 1
            rectM.w = 1
            if click_type[0]:
                if collides(rectM, terran.getRect()):
                    terran.setClicked(True)
                    print("CLICKADO")
                    
                else:
                    terran.setClicked(False)
                    print("DESCLICKADO")
            if click_type[2] and terran.isClicked():

                terran.angle = math.atan2(mouse_pos[1] - terran.rectn.y, mouse_pos[0] - terran.rectn.x)
                print(terran.angle)
                terran.distanceToPoint = math.hypot(mouse_pos[0] - terran.rectn.x, mouse_pos[1] - terran.rectn.y)
                terran.distanceToPoint = int(terran.distanceToPoint)

                terran.dirX = math.cos(terran.angle)
                terran.dirY = math.sin(terran.angle)
                if terran.angle < 0:
                    terran.angle = -terran.angle
                else:
                    terran.angle = 2*math.pi - terran.angle
                terran.face = int(4 - (terran.angle*8/math.pi))%16
                print(terran.angle)
                print(terran.face) 
            
                
            

    
    ###---LOGICA
    #Actualizar objetos



    ###---LOGICA
    terran.update()
    #Poner color de fondo
    screen.fill(WHITE)
    r = terran.getRect()
    screen.blit(terran.image, [r.x, r.y])
    ###--- ZONA DE DIBUJO


    ###--- ZONA DE DIBUJO

    #ACtualizar pantalla
    pygame.display.flip()
    clock.tick(60)

