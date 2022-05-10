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
from src.Entities.TerranRefinery import *


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
            escena.camera.h = SCREEN_HEIGHT - 160
            escena.camera.w = SCREEN_WIDTH
            screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        elif event.type == pg.KEYUP:
            escena.procesarEvent(event)
            escena.checkUnHoldButton(event.key)
        else:
            escena.procesarEvent(event)
    if getGameState() == System_State.ONGAME: #si pulsamos en los menus peta por lo que
        escena.checkPressedButtons()


'''
def setEntity(player, ai):

    structure1 = TerranBuilder(10, 72, player, mapa, False, raton)
    #structure2 = TerranBarracks(17, 67, player, mapa, False)
    structure1z = TerranBuilder(70, 8, ai, mapa, False, raton)
    drone = TerranWorker(ai, 67,11)
    scv = TerranWorker(player, 13, 69)
    ai.addUnits(drone)
    ai.addStructures(structure1z)
    ai.setBasePlayer(structure1z)
    player.addStructures(structure1)
    player.setBasePlayer(structure1)
    player.addUnits(scv)

    #Recursos del mapa
    resources = []

    crystal = Crystal(30, 70, 400)
    crystal3 = Crystal(30, 66, 400)

    crystalz = Crystal(50, 10, 400)
    crystalz3 = Crystal(50, 14, 400)


    crystal4 = Crystal(36, 40, 800)
    crystal5 = Crystal(36, 36, 800)
    crystal6 = Crystal(41, 36, 800)
    crystal2 = Crystal(41, 40, 800)

    crystal7 = Crystal(60, 60, 400)
    crystal8 = Crystal(60, 56, 400)
    crystal9 = Crystal(20, 20, 400)
    crystal10 = Crystal(20, 16, 400)


    resources.append(crystal3)
    resources.append(crystal)

    resources.append(crystalz3)
    resources.append(crystalz)


    resources.append(crystal2)
    resources.append(crystal4)
    resources.append(crystal5)
    resources.append(crystal6)

    resources.append(crystal7)
    resources.append(crystal8)
    resources.append(crystal9)
    resources.append(crystal10)




    gas = Geyser(65, 65, 500)
    resources.append(gas)
    gas = Geyser(70, 65, 500)
    resources.append(gas)
    gas = Geyser(15, 15, 500)
    resources.append(gas)
    gas = Geyser(10, 15, 500)
    resources.append(gas)
    gas = Geyser(6, 61, 500)
    resources.append(gas)
    gas = Geyser(4, 64, 500)
    resources.append(gas)
    gas = Geyser(74, 19, 500)
    resources.append(gas)
    gas = Geyser(76, 16, 500)
    resources.append(gas)
    escena.resources = resources'''

def setEntity(player, ai):

    structure1 = TerranBuilder(5, 4, player, mapa, False, raton)
    #structure2 = TerranBarracks(17, 67, player, mapa, False)
    structure1z = TerranBuilder(35, 4, ai, mapa, False, raton)
    drone = TerranWorker(ai, 35,6)
    scv = TerranWorker(player, 5, 6)
    ai.addUnits(drone)
    ai.addStructures(structure1z)
    ai.setBasePlayer(structure1z)
    player.addStructures(structure1)
    player.setBasePlayer(structure1)
    player.addUnits(scv)

    #Recursos del mapa
    resources = []

    crystal = Crystal(5, 11, 800)
    crystal3 = Crystal(9, 11, 800)
    crystala = Crystal(13, 11, 800)
    crystalb = Crystal(17, 11, 800)
    crystalc = Crystal(21, 11, 800)

    crystalz = Crystal(35, 11, 400)
    crystalz3 = Crystal(31, 11, 400)


    resources.append(crystal3)
    resources.append(crystal)
    resources.append(crystala)
    resources.append(crystalb)
    resources.append(crystalc)

    resources.append(crystalz3)
    resources.append(crystalz)





    gas = Geyser(15, 6, 800)
    resources.append(gas)
    gas = Geyser(25, 6, 800)
    resources.append(gas)
    escena.resources = resources

def update():
    clock_update()
    raton.update(camera)

    if getGameState() == System_State.MAINMENU:
        playMusic(mainMenuBGM, pos = 5)
        #playSound(mainMenuBGM)
        escena.interfaz.update(escena,raton, camera)
    elif getGameState() == System_State.MAP1:
        #playMusic(map1BGM)
        #cargar mapa
        escena.mapa = mapa
        escena.mapa.load()
        escena.mapa.loadMinimap()
        camera.x = 0
        camera.y = 0
        setEntity(player1, player2)
        setGameState(System_State.ONGAME)
    elif getGameState() == System_State.ONGAME:
        escena.update()
    elif getGameState() == System_State.GAMESELECT:
        #Cargar las partidas
        escena.interfaz.update(escena,raton, camera)
    elif getGameState() == System_State.NEWGAME:
        escena.interfaz.update(escena,raton, camera)
    else: #STATE == System_State.EXIT:
        pg.quit()
        sys.exit()

def draw():
    screen.fill(WHITE)
    if Utils.state == System_State.MAINMENU:
        escena.interfaz.draw(screen, camera)
    elif Utils.state == System_State.ONGAME:
        escena.draw(screen)
    elif Utils.state == System_State.GAMESELECT or Utils.state == System_State.NEWGAME:
        escena.interfaz.draw(screen, camera)
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
  pg.K_UP: CommandId.MOVE_CAMERA_UP,
  pg.K_DOWN: CommandId.MOVE_CAMERA_DOWN,
  pg.K_RIGHT: CommandId.MOVE_CAMERA_RIGHT,
  pg.K_LEFT: CommandId.MOVE_CAMERA_LEFT,
  pg.K_r: CommandId.ROTATE,
  pg.K_v: CommandId.GENERATE_UNIT,
  pg.K_c: CommandId.BUILD_BARRACKS,
  pg.K_x: CommandId.BUILD_REFINERY,
  pg.K_d: CommandId.UPGRADE_SOLDIER_DAMAGE,
  pg.K_a: CommandId.UPGRADE_SOLDIER_ARMOR,
  pg.K_m: CommandId.UPGRADE_WORKER_MINING,
  pg.K_g: CommandId.SAVE_GAME,
}
commandMap ={
  CommandId.MOVE_CAMERA_UP: pg.K_UP,
  CommandId.MOVE_CAMERA_DOWN: pg.K_DOWN,
  CommandId.MOVE_CAMERA_RIGHT: pg.K_RIGHT,
  CommandId.MOVE_CAMERA_LEFT: pg.K_LEFT,
  CommandId.ROTATE: pg.K_r,
}

print(MAPA_CHIKITO.__len__(), MAPA_CHIKITO[0].__len__())
mapa = Map.Map( MAPA_CHIKITO[0].__len__(),MAPA_CHIKITO.__len__(), True, MAPA_CHIKITO)
'''
mapa.setElevacion(0, 55)
mapa.setElevacion(8, 55)
mapa.setElevacion(16, 55)
mapa.setElevacion(24, 55)
mapa.setElevacion(32, 60)
mapa.setElevacion(32, 65)
mapa.setElevacion(32, 70)
mapa.setElevacion(32, 75)


mapa.setElevacion(72, 20)
mapa.setElevacion(64, 20)
mapa.setElevacion(56, 20)
mapa.setElevacion(48, 20)
mapa.setElevacion(40, 15)
mapa.setElevacion(40, 10)
mapa.setElevacion(40, 5)
mapa.setElevacion(40, 0)'''



player1 = Player.Player([], [], 400, keyMap, commandMap, mapa, True)

# Raton


# Player 2 AKA IA
player2 = Player.Player([], [], 4000, {}, {}, mapa, False)


# Camara
# pre: mapa tan grande como ventana
camera = Camera(0, 0, SCREEN_HEIGHT - 160, SCREEN_WIDTH)

# Escena



raton = Raton.Raton(player1, player2, mapa)
p1Interface = Interface(player1, player2, raton)
raton.addInterface(p1Interface)
if Utils.DEBBUG == False:
    aI = AI(player2, Race.TERRAN, EASY)

else:
    aI = AI(player2, Race.TERRAN, NULA)
escena = Escena(player1, player2, aI, [], camera, raton, p1Interface, [])
raton.setEscena(escena)

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
