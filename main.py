import time
import pygame, sys
import math
from src.Lib import *
from src.Music import *
from src.Entities.Cristal import Cristal
from src import Map, Raton, Escena, Player, Camera, AI, Command, Utils, Interface
from src.Entities import Terran, TerranBuilder, Zergling, ZergBuilder, TerranBarracks, TerranWorker

# Auxiliar del bucle principal
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
        elif event.type == pygame.KEYUP:
            print("·")
            escena.procesarEvent(event)
            escena.checkUnHoldButton(event.key)
        else:
            escena.procesarEvent(event)
    escena.checkPressedButtons()

# Programa principal

pygame.init()

flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
size = (Utils.SCREEN_WIDTH, Utils.SCREEN_HEIGHT)
screen =  pygame.display.set_mode(size)

#Controlar frames por segundo
clock = pygame.time.Clock()

mapa = Map.Map(40, 20)

# Player 1
keyMap ={
  pygame.K_UP: Command.CommandId.MOVER_CAMARA_ARRIBA,
  pygame.K_DOWN: Command.CommandId.MOVER_CAMARA_ABAJO,
  pygame.K_RIGHT: Command.CommandId.MOVER_CAMARA_DERECHA,
  pygame.K_LEFT: Command.CommandId.MOVER_CAMARA_IZQUIERDA,
  pygame.K_r: Command.CommandId.ROTAR,
  pygame.K_v: Command.CommandId.GENERAR_UNIDAD,
}
commandMap ={
  Command.CommandId.MOVER_CAMARA_ARRIBA: pygame.K_UP,
  Command.CommandId.MOVER_CAMARA_ABAJO: pygame.K_DOWN,
  Command.CommandId.MOVER_CAMARA_DERECHA: pygame.K_RIGHT,
  Command.CommandId.MOVER_CAMARA_IZQUIERDA: pygame.K_LEFT,
  Command.CommandId.ROTAR: pygame.K_r,
}

player1 = Player.Player([],[],100, keyMap, commandMap)

# Raton
sprite_ruta = "./SPRITE/raton/"
raton = Raton.raton(sprite_ruta, player1)

p1Interface = Interface.Interface(player1, raton)

# Player 2 AKA IA
player2 = Player.Player([], [], 100, [], [])
aI = AI.AI(player2)
#zergling1 = Zergling.Zergling(9, 8)
#player2.addUnits(zergling1)



# Camara
# pre: mapa tan grande como ventana
camera = Camera.Camera(0, 0, Utils.SCREEN_HEIGHT, Utils.SCREEN_WIDTH)

# Escena

#Recursos del mapa
cristal = Cristal(34,1,80,500)
resources = []
resources.append(cristal)
escena = Escena.Escena(player1, player2, aI, mapa, camera, raton, p1Interface, resources)
#escena.mapa.addOre(100,100)

def setEntity(player):
    #terran1 = Terran.Terran(40, 80, 80, 20, 200, 1, 5, "terranSprites", 8, 6)
    #terran2 = Terran.Terran(40, 200, 200, 20, 200, 1, 5, "terranSprites", 8, 6)
    scv = TerranWorker.TerranWorker(4, 10, player1)
    #zergling2 = Zergling.Zergling(10, 10)
    structure1 = TerranBuilder.TerranBuilder(200, 40, 600, 5, 6, player1, mapa, False, 2)
    escena.setBasePlayer1(structure1)
    structure2 = TerranBarracks.TerranBarracks(200, 40, 600, 15, 9, player1, mapa, False, 3)
    player.addStructures(structure1)
    player.addStructures(structure2)
    player.addUnits(scv)
    #player.addUnits(terran2)
    #player.addUnits(zergling2)
    #player1.addUnits(scv)

    zergBuilder = ZergBuilder.ZergBuilder(200, 50, 10, 15, 15, player2, mapa, False, 8)
    zergling2 = Zergling.Zergling(10, 10, player1)
    player1.addUnits(zergling2)
    player1.addStructures(zergBuilder)


def update():
    Utils.clock_update()
    raton.update(camera)
    
    if Utils.STATE == Utils.System_State.MAINMENU:
        playMusic(mainMenuBGM, pos = 5)
        #playSound(mainMenuBGM)
        p1Interface.update()
    elif Utils.STATE == Utils.System_State.MAP1:
        playMusic(map1BGM)
        #cargar mapa
        escena.mapa.load(Utils.MAPA1)
        setEntity(player1)
        Utils.STATE = Utils.System_State.ONGAME
    elif Utils.STATE == Utils.System_State.ONGAME:
        escena.update()
    else: #Utils.STATE == Utils.System_State.EXIT:
        pygame.quit()
        sys.exit()



def draw():
    screen.fill(Utils.WHITE)
    if Utils.STATE == Utils.System_State.MAINMENU:
        p1Interface.draw(screen)
    elif Utils.STATE == Utils.System_State.ONGAME:
        escena.draw(screen)
    raton.draw(screen, camera)
    #Utils.aux(screen)
    pygame.display.flip()



# Bucle principal
while True:
    #now = datetime.now()
    #Procesar inputs
    procesarInput()

    #Actualizar entidades del juego
    update()
    #print((datetime.now() - now).microseconds)

    #Dibujar
    draw()

    clock.tick(Utils.CLOCK_PER_SEC)
