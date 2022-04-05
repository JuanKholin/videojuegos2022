import pygame, sys
import math
from src import Map, Raton, Escena, Player, Camera, AI, Command, Utils
from src.Entities import Terran, TerranBuilder, Zergling

pygame.init()

# Definir colores

X_TILES = 20
Y_TILES = 10

SCREEN_WIDTH = X_TILES * 40
SCREEN_HEIGHT = Y_TILES * 40

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen =  pygame.display.set_mode(size, pygame.RESIZABLE)

#Controlar frames por segundo
clock = pygame.time.Clock()

mapa = Map.Map(20, 40)
player1 = Player.Player([],[],5,
{
  pygame.K_UP: Command.CommandId.MOVER_CAMARA_ARRIBA,
  pygame.K_DOWN: Command.CommandId.MOVER_CAMARA_ABAJO,
  pygame.K_RIGHT: Command.CommandId.MOVER_CAMARA_DERECHA,
  pygame.K_LEFT: Command.CommandId.MOVER_CAMARA_IZQUIERDA,
},
{
    Command.CommandId.MOVER_CAMARA_ARRIBA: pygame.K_UP,
  Command.CommandId.MOVER_CAMARA_ABAJO: pygame.K_DOWN,
  Command.CommandId.MOVER_CAMARA_DERECHA: pygame.K_RIGHT,
  Command.CommandId.MOVER_CAMARA_IZQUIERDA: pygame.K_LEFT,
}
)

terran1 = Terran.Terran(40, 80, 80, 20, 200, 1, 5, "terranSprites", 8, 6,1)
terran2 = Terran.Terran(40, 200, 200, 20, 200, 1, 5, "terranSprites", 8, 6,2)
zergling2 = Zergling.Zergling(10, 10)
structure1 = TerranBuilder.TerranBuilder(200, 40, 600, 200, 300, player1, mapa, "SPRITE/builder",2)

player1.addStructures(structure1)
player1.addUnits(terran1)
player1.addUnits(terran2)
player1.addUnits(zergling2)

# IA
player2 = Player.Player([], [], 5, [], [])
zergling1 = Zergling.Zergling(9, 8)
aI = AI.AI(player2)
player2.addUnits(zergling1)

# Raton
sprite_ruta = "./SPRITE/raton/"
raton = Raton.raton(sprite_ruta, player1)

#pre: mapa tan grande como ventana
camera = Camera.Camera(20, 20, SCREEN_HEIGHT, SCREEN_WIDTH)

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
            escena.camera.h = event.h
            escena.camera.w = event.w
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        else:
            escena.procesarEvent(event)
    escena.checkPressedButtons()

while True:
    #now = datetime.now()
    #Procesar inputs
    procesarInput()

    #Actualizar entidades del juego
    escena.update()
    #print((datetime.now() - now).microseconds)

    #Dibujar
    screen.fill(Utils.WHITE)
    escena.draw(screen)
    pygame.display.flip()

    clock.tick(60)
