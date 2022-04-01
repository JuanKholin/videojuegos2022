import pygame, sys
import math
from src import Map, Raton, Escena, Player, Camera, AI
from src.Entities import Terran, TerranBuilder, Zerg

pygame.init()

# Definir colores

BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
BLUE    = (0, 0, 255)

SCREEN_WIDTH = 20*40
SCREEN_HEIGHT = 10*40

size =(SCREEN_WIDTH, SCREEN_HEIGHT)

screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()

# Mapa
mapa = Map.Map(10, 20)

# Jugador
player1 = Player.Player([],[],5,[])
terran1 = Terran.Terran(40, 20, 20, 20, 200, 2, 5, "terranSprites", 0, 0,1)
structure1 = TerranBuilder.TerranBuilder(200, 40, 600, 200, 300, player1, mapa, "SPRITE/builder",2)

player1.addStructures(structure1)
player1.addUnits(terran1)

# IA
player2 = Player.Player([], [], 5, [])
# Hasta que encuentre los Zergs, los Zergs son Terranos
zerg1 = Zerg.Zerg(40, 100, 100, 20, 200, 2, 5, "terranSprites", 0, 0, 1)
aI = AI.AI(player2)
player2.addUnits(zerg1)

# Raton
sprite_ruta = "./SPRITE/raton/"
raton = Raton.raton(sprite_ruta, player1)

# Camara
camera = Camera.Camera(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT)

# Escena
escena = Escena.Escena(player1, player2, aI, mapa, camera, raton)


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
    #now = datetime.now()
    #Procesar inputs
    procesarInput()

    #Actualizar entidades del juego
    escena.update()
    #print((datetime.now() - now).microseconds)
    
    #Dibujar
    screen.fill(WHITE)
    escena.draw(screen)
    pygame.display.flip()

    clock.tick(60)
