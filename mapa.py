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



def setEntity(player, ai):

    structure1 = TerranBuilder(10, 72, player, mapa, False, raton)
    scv = TerranWorker(13, 69, player)
    
    '''
    scv2 = TerranSoldier(5, 10, player)
    scv3 = TerranSoldier(6, 10, player)
    scv4 = TerranSoldier(7, 10, player)
    scv5 = TerranSoldier(8, 10, player)
    scv6 = TerranSoldier(9, 10, player)
    scv7 = TerranSoldier(10, 10, player)
    scv8 = TerranWorker(11, 10, player)'''
    structure3 = TerranSupplyDepot(20, 7, player, mapa, True)

    player.setBasePlayer(structure1)
    structure2 = TerranBarracks(15, 9, player, mapa, False)
    structure4 = Extractor(12, 27, player, mapa, True)
    structure5 = TerranRefinery(13, 18, player, mapa, True)
    
    player.addStructures(structure1)
    '''player.addStructures(structure2)
    player.addStructures(structure3)
    
    player.addStructures(structure5)'''
    ai.addStructures(structure4)
    player.addUnits(scv)

    aiUnits = []
    #aiUnits.append(Drone(20, 10, ai))
    '''aiUnits.append(Drone(25, 11, ai))
    aiUnits.append(Zergling(27, 10, ai))
    aiUnits.append(Zergling(27, 11, ai))
    aiUnits.append(Zergling(27, 12, ai))
    aiUnits.append(Zergling(27, 13, ai))
    aiUnits.append(Zergling(27, 14, ai))'''

    for unit in aiUnits:
        ai.addUnits(unit)

    aiStructures = []
    #aiStructures.append(Hatchery(20, 12, ai, mapa, False))
    #aiStructures.append(TerranBuilder(20, 12, ai, mapa, False, raton))

    #for structure in aiStructures:
     #   ai.addStructures(structure)

    #Recursos del mapa
    resources = []
    crystal2 = Crystal(32, 74, 800)
    crystal = Crystal(30, 70, 800)
    crystal3 = Crystal(26, 66, 800)
    crystal4 = Crystal(25, 74, 800)
    crystal5 = Crystal(25, 70, 800)
    crystal6 = Crystal(28, 78, 800)
    
    
    resources.append(crystal3)
    resources.append(crystal)
    resources.append(crystal2)
    resources.append(crystal4)
    resources.append(crystal5)
    resources.append(crystal6)
    
    
    gas = Geyser(6, 61, 500)
    resources.append(gas)
    gas = Geyser(4, 64, 500)
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
        camera.x = 200
        camera.y = 2400
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

print(EMPTY_MAP.__len__(), EMPTY_MAP[0].__len__())
mapa = Map.Map( EMPTY_MAP[0].__len__(),EMPTY_MAP.__len__(), True, EMPTY_MAP)
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
mapa.setElevacion(40, 0)



player1 = Player.Player([], [], 400, keyMap, commandMap, mapa, True)

# Raton


# Player 2 AKA IA
player2 = Player.Player([], [], 4000, {}, {}, mapa, False)
aI = AI(player2, Race.TERRAN, EASY)

# Camara
# pre: mapa tan grande como ventana
camera = Camera(0, 0, SCREEN_HEIGHT - 160, SCREEN_WIDTH)

# Escena



raton = Raton.Raton(player1, player2, mapa)
p1Interface = Interface(player1, player2, raton)
raton.addInterface(p1Interface)

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
