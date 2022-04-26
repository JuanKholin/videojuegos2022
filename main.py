import time
import pygame as pg
import sys
import math

from src.Utils import *
from src.Command import *
from src import Player, Raton, Map
from src.Interface import *
from src.AI import *
from src.Camera import *
from src.Entities.Cristal import *
from src.Escena import Escena
from src.Entities.TerranWorker import *
from src.Entities.TerranBuilder import *
from src.Entities.TerranBarracks import *
from src.Entities.ZergBuilder import *
from src.Entities.Drone import *
from src.Entities.Zergling import *

# Auxiliar del bucle principal
def procesarInput():
    for event in pg.event.get(): #Identificar lo sucedido en la ventana
        #print(event)
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            escena.camera.h = event.h
            escena.camera.w = event.w
            screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        elif event.type == pg.KEYUP:
            print("·")
            escena.procesarEvent(event)
            escena.checkUnHoldButton(event.key)
        else:
            escena.procesarEvent(event)
    escena.checkPressedButtons()

# Programa principal

pg.init()

flags = pg.FULLSCREEN | pg.DOUBLEBUF
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen =  pg.display.set_mode(size)

#Controlar frames por segundo

mapa = Map.Map(40, 20)

# Player 1
keyMap ={
  pg.K_UP: CommandId.MOVER_CAMARA_ARRIBA,
  pg.K_DOWN: CommandId.MOVER_CAMARA_ABAJO,
  pg.K_RIGHT: CommandId.MOVER_CAMARA_DERECHA,
  pg.K_LEFT: CommandId.MOVER_CAMARA_IZQUIERDA,
  pg.K_r: CommandId.ROTAR,
  pg.K_v: CommandId.GENERAR_UNIDAD,
}
commandMap ={
  CommandId.MOVER_CAMARA_ARRIBA: pg.K_UP,
  CommandId.MOVER_CAMARA_ABAJO: pg.K_DOWN,
  CommandId.MOVER_CAMARA_DERECHA: pg.K_RIGHT,
  CommandId.MOVER_CAMARA_IZQUIERDA: pg.K_LEFT,
  CommandId.ROTAR: pg.K_r,
}

player1 = Player.Player([], [], 100, keyMap, commandMap)

# Raton
sprite_ruta = "./SPRITE/raton/"
raton = Raton.Raton(sprite_ruta, player1)

p1Interface = Interface(player1, raton)

# Player 2 AKA IA
player2 = Player.Player([], [], 100, [], [])
aI = AI(player2)

# Camara
# pre: mapa tan grande como ventana
camera = Camera(0, 0, SCREEN_HEIGHT, SCREEN_WIDTH)

# Escena

#Recursos del mapa
cristal = Cristal(7,1,200,700)
resources = []
resources.append(cristal)
escena = Escena(player1, player2, aI, mapa, camera, raton, p1Interface, resources)
#escena.mapa.addOre(100,100)

def setEntity(player):
    scv = TerranWorker.TerranWorker(5, 12, player1)
    scv2 = TerranWorker.TerranWorker(6, 12, player1)
    structure1 = TerranBuilder(200, 40, 600, 5, 6, player1, mapa, False, 2)
    escena.setBasePlayer1(structure1)
    structure2 = TerranBarracks(200, 40, 600, 15, 9, player1, mapa, False, 3)
    player.addStructures(structure1)
    player.addStructures(structure2)
    player.addUnits(scv)
    player.addUnits(scv2)


    zergBuilder = ZergBuilder(200, 50, 10, 15, 15, player2, mapa, False, 8)
    player1.addStructures(zergBuilder)

    drone = Drone(10, 11, player1)
    player1.addUnits(drone)

    zergling = Zergling(8, 9, player1)
    player1.addUnits(zergling)

    

def update():
    clock_update()
    raton.update(camera)
    
    if Utils.state == System_State.MAINMENU:
        #playMusic(mainMenuBGM, pos = 5)
        #playSound(mainMenuBGM)
        p1Interface.update()
    elif Utils.state == System_State.MAP1:
        #playMusic(map1BGM)
        #cargar mapa
        escena.mapa.load(Utils.MAPA1)
        setEntity(player1)
        Utils.state = System_State.ONGAME
    elif Utils.state == System_State.ONGAME:
        escena.update()
    else: #Utils.STATE == Utils.System_State.EXIT:
        pg.quit()
        sys.exit()

def draw():
    screen.fill(WHITE)
    if Utils.state == System_State.MAINMENU:
        p1Interface.draw(screen)
    elif Utils.state == System_State.ONGAME:
        escena.draw(screen)
    raton.draw(screen, camera)
    #Utils.aux(screen)
    pg.display.flip()

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

    Utils.GLOBAL_TIME += Utils.clock.tick(Utils.CLOCK_PER_SEC)

