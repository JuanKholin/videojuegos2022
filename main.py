import pygame, sys
import math
from src import Map, Raton, Escena, Player, Camera
from src.Entities import Terran

pygame.init()

# Definir colores

BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
BLUE    = (0, 0, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

size =(SCREEN_WIDTH, SCREEN_HEIGHT)

screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()

terran1 = Terran.Terran(40, 20, 20, 20, 20, 2, 5, "terranSprites", 0, 0)
p1Units = []
p1Units.append(terran1)
player1 = Player.Player(p1Units,[],5,[])
sprite_ruta = "./SPRITE/raton/"
raton = Raton.raton(sprite_ruta)
mapa = Map.Map(10, 20)
camera = Camera.Camera(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT)
escena = Escena.Escena(player1,[],[],mapa, camera, raton)




def procesarInput():
    for event in pygame.event.get(): #Identificar lo sucedido en la ventana
        #print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        else:
            escena.procesarEvent(event)
        
while True:

    #Procesar inputs
    procesarInput()

    #Actualizar entidades del juego
    escena.update()

    #Dibujar
    screen.fill(WHITE)
    escena.draw(screen)
    pygame.display.flip()

    clock.tick(60)
