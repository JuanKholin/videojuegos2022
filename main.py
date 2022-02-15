import pygame, sys

pygame.init()

# Definir colores

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

size =(SCREEN_WIDTH,SCREEN_HEIGHT)



screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()

#Coordenadas figura
cord_x = 400
cord_y = 200

#Velocidad figura
speed_x = 3
speed_y = 3

bckg = pygame.image.load("assets/background.jpg").convert()
kurisu = pygame.image.load("assets/kurisu.png").convert()
kurisu.set_colorkey(BLACK)


while True:
    for event in pygame.event.get(): #Identificar lo sucedido en la ventana
        #print(event)
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            bckg = pygame.transform.scale(bckg,(SCREEN_WIDTH, SCREEN_HEIGHT))


    ###---LOGICA
    #Movimiento de cuadrado

    
    if cord_x > (SCREEN_WIDTH - kurisu.get_width()) or cord_x < 0:
        speed_x = -speed_x
    if cord_y > (SCREEN_HEIGHT - kurisu.get_height()) or cord_y < 0:
        speed_y = -speed_y

    cord_x += speed_x
    cord_y += speed_y

    ###---LOGICA

    #Poner color de fondo
    screen.fill(WHITE)
    
    ###--- ZONA DE DIBUJO
    screen.blit(bckg, [0,0])
    screen.blit(kurisu, [cord_x,cord_y])

    ###--- ZONA DE DIBUJO

    #ACtualizar pantalla
    pygame.display.flip()
    clock.tick(60)