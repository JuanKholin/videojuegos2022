import time
import pygame as pg
import sys
import math
import json
from datetime import datetime


from src.Entities.TerranSoldier import *

from src.Utils import *
from src.Command import *
from src import Player, Raton, Map
from src.Interface import *
from src.AI import *
from src.Camera import *
from src.Entities.Crystal import *
from src.Entities.Geyser import *
from src.Escena import Escena
from src.Entities.TerranBuilder import * 
from src.Entities.TerranWorker import *
from src.Entities.TerranBarracks import *
from src.Entities.Hatchery import *
from src.Entities.Drone import *
from src.Entities.Zergling import *
from src.Entities.TerranSupplyDepot import *
from src.Entities.Extractor import * 


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
            escena.procesarEvent(event)
            escena.checkUnHoldButton(event.key)
        else:
            escena.procesarEvent(event)
    escena.checkPressedButtons()

def setEntity(player):

    scv = TerranWorker(4, 10, player1)
    structure1 = TerranBuilder(5, 6, player1, mapa, False, 1)
    structure3 = TerranSupplyDepot(10, 6, player1, mapa, True, 2)

    player1.setBasePlayer(structure1)
    structure2 = TerranBarracks(15, 9, player1, mapa, False, 3)
    structure4 = Extractor(12, 27, player1, mapa, True, 4)
    player.addStructures(structure1)
    player.addStructures(structure2)
    player.addStructures(structure3)
    player.addStructures(structure4)
    player.addUnits(scv)

    hatchery = Hatchery(16, 14, player1, mapa, False, 8)
    player.addStructures(hatchery)

    drone = Drone(10, 11, player1)
    player1.addUnits(drone)

    soldierChan = TerranSoldier(6, 1, player1)
    player1.addUnits(soldierChan)

    zergling = Zergling(0, 0, player1)
    player1.addUnits(zergling)

    droneAI = Drone(3, 2, player2)
    player2.addUnits(droneAI)

def update():
    clock_update()
    raton.update(camera)

    if getGameState() == System_State.MAINMENU:
        playMusic(mainMenuBGM, pos = 5)
        #playSound(mainMenuBGM)
        p1Interface.update()
    elif getGameState() == System_State.MAP1:
        playMusic(map1BGM)
        #cargar mapa
        escena.mapa.load()
        escena.mapa.loadMinimap()
        setEntity(player1)
        setGameState(System_State.ONGAME)
    elif getGameState() == System_State.ONGAME:
        escena.update()
    else: #STATE == System_State.EXIT:
        pg.quit()
        sys.exit()

def draw():
    screen.fill(WHITE)
    if Utils.state == System_State.MAINMENU:
        p1Interface.draw(screen, camera)
    elif Utils.state == System_State.ONGAME:
        escena.draw(screen)
    raton.draw(screen, camera)
    #aux(screen)
    pg.display.flip()


# Programa principal
pg.init()

flags = pg.FULLSCREEN | pg.DOUBLEBUF
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen =  pg.display.set_mode(size)

#Controlar frames por segundo
clock = pg.time.Clock()

# Player 1
keyMap ={
  pg.K_UP: CommandId.MOVER_CAMARA_ARRIBA,
  pg.K_DOWN: CommandId.MOVER_CAMARA_ABAJO,
  pg.K_RIGHT: CommandId.MOVER_CAMARA_DERECHA,
  pg.K_LEFT: CommandId.MOVER_CAMARA_IZQUIERDA,
  pg.K_r: CommandId.ROTAR,
  pg.K_v: CommandId.GENERAR_UNIDAD,
  pg.K_c: CommandId.BUILD_STRUCTURE,
  pg.K_d: CommandId.MEJORAR_DAÑO_SOLDADO,
  pg.K_a: CommandId.MEJORAR_ARMADURA_SOLDADO,
  pg.K_m: CommandId.MEJORAR_MINADO_WORKER,
  pg.K_g: CommandId.GUARDAR_PARTIDA,
}
commandMap ={
  CommandId.MOVER_CAMARA_ARRIBA: pg.K_UP,
  CommandId.MOVER_CAMARA_ABAJO: pg.K_DOWN,
  CommandId.MOVER_CAMARA_DERECHA: pg.K_RIGHT,
  CommandId.MOVER_CAMARA_IZQUIERDA: pg.K_LEFT,
  CommandId.ROTAR: pg.K_r,
}

mapa = Map.Map(40, 40, True)
mapa.setElevacion(16, 3)
mapa.setElevacion(20, 14)
mapa.setElevacion(17, 30)
mapa.setElevacion(12, 20)
mapa.setElevacion(8, 35)
mapa.setElevacion(5, 12)
mapa.setElevacion(32, 29)

player1 = Player.Player([], [], 400, keyMap, commandMap, mapa, True)

# Raton


# Player 2 AKA IA
player2 = Player.Player([], [], 400, {}, {}, mapa, False)
aI = AI(player2, EASY)

# Camara
# pre: mapa tan grande como ventana
camera = Camera(0, 0, SCREEN_HEIGHT - 160, SCREEN_WIDTH)

# Escena

#Recursos del mapa
crystal = Crystal(2, 10, 34)
crystal2 = Crystal(2, 16, 34)

geyser1 = Geyser(10, 2, 34)
geyser2 = Geyser(2, 22, 34)


resources = []
resources.append(crystal)
resources.append(crystal2)
resources.append(geyser1)
#resources.append(geyser2)

raton = Raton.Raton(player1, player2)
p1Interface = Interface(player1, player2, raton)
raton.addInterface(p1Interface)

escena = Escena(player1, player2, aI, mapa, camera, raton, p1Interface, resources)
raton.setEscena(escena)
#escena.mapa.addOre(100,100)

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

    updateGlobalTime(clock)
