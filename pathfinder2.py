import pygame, sys, random, time
import math
from src import Terran, Map, Raton

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












#Inicializo el mapa



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

#DECLARACION DE VARIABLES----------------------------------

screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()

units = []
unitsClicked = []

units.append(Terran.Terran(2, 200,200,"SPRITE/terranSprites",1))
units.append(Terran.Terran(2, 100,50,"SPRITE/terranSprites",2))
#units.append(Terran.Terran(2, 300,50,"terranSprites",3))
#units.append(Terran.Terran(2, 50,100,"terranSprites",4))
#units.append(Terran.Terran(2, 100,200,"terranSprites",5))
#units.append(Terran.Terran(2, 300,300,"terranSprites",6))

map = Map.Map(10,20)
map.addObstacle(240,40,3,3)
map.addObstacle(240,240,3,3)
map.addObstacle(400,160,3,3)
map.addObstacle(100,160,3,3)

sprite_ruta = "./SPRITE/raton/"

mouse = Raton.raton(sprite_ruta)
p = Raton.point(sprite_ruta)
pygame.mouse.set_visible(False)

initialX = 0
initialY = 0
pulsado = False
    

while True:
    rectM = Terran.rect()

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
            
            if click_type[0]:     
                if not pulsado:
                    pulsado = True
                    initialX = mouse_pos[0]
                    initialY = mouse_pos[1]
            if click_type[2]:
                if not pulsado:
                    #print("CALCULANDO PUNTOS")
                    points = calcPointsRound(mouse_pos)
                    p.click(mouse_pos[0], mouse_pos[1])
                    for terran in unitsClicked:
                        pathA = map.calcPath(terran.rectn.x,terran.rectn.y,mouse_pos[0],mouse_pos[1])
                        tileIni = map.getTile(terran.rectn.x,terran.rectn.y)
                        posIni = (tileIni.centerx, tileIni.centery)
                        terran.paths = []
                        for tile in pathA:
                            posFin = (tile.centerx, tile.centery)
                            path1 = Terran.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])))
                            terran.paths.append(path1)
                            posIni = posFin 

        if event.type == pygame.MOUSEBUTTONUP:
            type = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()  
            #print('click liberado', type)
            if not type[0]:   
                if pulsado: 
                    pulsado = False
                    #print('click izq liberado', mouse_pos[0], mouse_pos[1], event.type)
                    unitsClicked = []
                    mouseRect = createRect(initialX, initialY, mouse_pos[0], mouse_pos[1])
                    for terran in units:
                        if collides(terran.getRect(), mouseRect):
                            terran.setClicked(True)
                            unitsClicked.append(terran)
                            
                            #print("CLICKADO" + str(terran.id))
                        else:
                            terran.setClicked(False)
                            #unitsClicked.remove(terran)
                            #print("DESCLICKADO" + str(terran.id)) 
            if type[2]:
                print('click der liberado', mouse_pos[0], mouse_pos[1], event.type)           

        if event.type == pygame.KEYDOWN:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_c]:
                for terran in unitsClicked:
                    #print("CANCELADO" + str(terran.id))
                    terran.cancel()
                
            

    
    ###---LOGICA
    #Actualizar objetos



    
    
    #Poner color de fondo
    screen.fill(WHITE)
    map.drawMap(screen)
    pos = pygame.mouse.get_pos()    
    mouseRect = pygame.Rect(pos[0], pos[1], 1, 1)
    mouse_collide = False
    for terran in units:
        ###---LOGICA
        terran.update()
        r = terran.getRect()
        pygame.draw.rect(screen, BLACK, pygame.Rect(r.x, r.y, r.w, r.h),1)
        screen.blit(terran.image, [r.x, r.y])
        if collides(terran.getRect(), mouseRect):
            mouse_collide = True

    if mouse_collide:
        mouse.setCollide(True)
    else:
        mouse.setCollide(False)
    
    p.update()
    mouse.update()

    if p.getClicked():
        screen.blit(p.image, (p.rect.x, p.rect.y))
    if pulsado:
        printRectangulo(screen, initialX, initialY, pos[0], pos[1])
    screen.blit(mouse.image, (mouse.rect.x, mouse.rect.y))

    
    ###--- ZONA DE DIBUJO


    ###--- ZONA DE DIBUJO

    #ACtualizar pantalla
    pygame.display.flip()
    clock.tick(60)

    # YO movimiento de unidad y colision con otra
    # UNIDAD ZERG BASICA ANTONIO
    # ESTRUCTURA QUE PERMITA CREAR TERRAN Y RATON ALEX
    # CAMARA ALONSO