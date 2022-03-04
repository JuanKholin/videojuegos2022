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

class Terran():
    def __init__(self, speed, xini, yini, sprites, id):
        super().__init__()
        #ATRIBUTOS
        self.id = id
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
                self.sprites[16-(i%9)].insert(int(i/9),pygame.transform.flip(pygame.image.load(sprites + "/tile0" + str(nPath) + ".png"),True,False))
            self.sprites[i%9].insert(int(i/9),pygame.image.load(sprites + "/tile0" + str(nPath) + ".png"))
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(WHITE)
        self.rectn = rect()
        self.rectn.w = self.image.get_width()
        self.rectn.h = self.image.get_height() - self.rectOffY
        self.rectn.x = xini
        self.rectn.y = yini

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
    
    def cancel(self):
        self.distanceToPoint = 0


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
 

screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()


units = []
unitsClicked = []

units.append(Terran(2, 50,50,"terranSprites",1))
units.append(Terran(2, 100,50,"terranSprites",2))
units.append(Terran(2, 300,50,"terranSprites",3))
units.append(Terran(2, 50,100,"terranSprites",4))
units.append(Terran(2, 100,200,"terranSprites",5))
units.append(Terran(2, 300,300,"terranSprites",6))



def calcPointsRound(mouse_pos):
    pointsRound = []
    pointsRound.append(mouse_pos)
    pos = (mouse_pos[0] - 40, mouse_pos[1])
    pointsRound.append(pos)
    pos = (mouse_pos[0] + 40, mouse_pos[1])
    pointsRound.append(pos)
    pos = (mouse_pos[0] - 20, mouse_pos[1] - 20)
    pointsRound.append(pos)
    pos = (mouse_pos[0] - 20, mouse_pos[1] + 20)
    pointsRound.append(pos)
    pos = (mouse_pos[0] + 20, mouse_pos[1] + 20)
    pointsRound.append(pos)
    pos = (mouse_pos[0] + 20, mouse_pos[1] - 20)
    pointsRound.append(pos)
    return pointsRound
    
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
                unitClicked = False
                for terran in units:
                    if collides(rectM, terran.getRect()):
                        unitClicked = True
                        if not terran.isClicked():
                            terran.setClicked(True)
                            unitsClicked.append(terran)
                            print("CLICKADO" + str(terran.id))
                        else:
                            terran.setClicked(False)
                            unitsClicked.remove(terran)
                            print("DESCLICKADO" + str(terran.id))
                        
                if unitClicked:
                    for terran in unitsClicked:
                        terran.setClicked(True)
                        print("Mantenemos a " + str(terran.id))
                else:
                    for terran in units:
                        terran.setClicked(False)
                        if terran in unitsClicked:
                            unitsClicked.remove(terran)
                        print("DESCLICKADO" + str(terran.id))
            if click_type[2]:
                print("CALCULANDO PUNTOS")
                points = calcPointsRound(mouse_pos)
                for terran in unitsClicked:
                    pos = points[0]
                    points.remove(points[0])
                    terran.angle = math.atan2(pos[1] - terran.rectn.y, pos[0] - terran.rectn.x)
                    print(terran.angle)
                    terran.distanceToPoint = math.hypot(pos[0] - terran.rectn.x, pos[1] - terran.rectn.y)
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
        if event.type == pygame.KEYDOWN:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_c]:
                for terran in unitsClicked:
                    print("CANCELADO" + str(terran.id))
                    terran.cancel()
                
            

    
    ###---LOGICA
    #Actualizar objetos



    
    
    #Poner color de fondo
    screen.fill(WHITE)
    for terran in units:
        ###---LOGICA
        terran.update()


        r = terran.getRect()
        screen.blit(terran.image, [r.x, r.y])
    
    ###--- ZONA DE DIBUJO


    ###--- ZONA DE DIBUJO

    #ACtualizar pantalla
    pygame.display.flip()
    clock.tick(60)

