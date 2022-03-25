import pygame, sys
import math
from src import Terran, Map, Raton, Escena

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

screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()

units = []
unitsClicked = []

map = Map.Map(10,20)

escena = Escena.Escena()

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
