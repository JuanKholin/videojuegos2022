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
    scv = TerranSoldier(player, 2, 2)
    scv2 = TerranSoldier(player, 5, 10)
    scv3 = TerranSoldier(player, 6, 10)
    scv4 = TerranSoldier(player, 7, 10)
    scv5 = TerranSoldier(player, 8, 10)
    scv6 = TerranSoldier(player, 9, 10)
    scv7 = TerranSoldier(player, 10, 10)
    scv8 = TerranWorker(player, 11, 10)
    structure1 = TerranBuilder(2, 7, player, mapa, False, raton)
    structure3 = TerranSupplyDepot(4, 4, player, mapa, True)
    structure7 = Hatchery(30, 30, player, mapa, True, raton)

    player.setBasePlayer(structure1)
    structure2 = TerranBarracks(15, 9, player, mapa, False)
    gas2 = Geyser(13, 20, 50)
    structure4 = Extractor(12, 27, player, mapa, True)
    structure5 = TerranRefinery(13, 18, ai, mapa, True, gas2)

    a = structure3.getPosition()
    print(a[0] / 40, a[1] /40)
    player.addStructures(structure1)
    player.addStructures(structure2)
    player.addStructures(structure3)
    
    player.addStructures(structure7)
    player.addStructures(structure4)
    ai.addStructures(structure5)
    player.addUnits(scv)
    player.addUnits(scv2)
    player.addUnits(scv3)
    player.addUnits(scv4)
    player.addUnits(scv5)
    player.addUnits(scv6)
    player.addUnits(scv7)
    player.addUnits(scv8)

    aiUnits = []
    #aiUnits.append(Drone(20, 10, ai))
    '''aiUnits.append(Drone(25, 11, ai))
    aiUnits.append(Zergling(27, 10, ai))
    aiUnits.append(Zergling(27, 11, ai))
    aiUnits.append(Zergling(27, 12, ai))
    aiUnits.append(Zergling(27, 13, ai))
    aiUnits.append(Zergling(27, 14, ai))'''

    #for unit in aiUnits:
    #    ai.addUnits(unit)

    aiStructures = []
    aiStructures.append(TerranBarracks(12, 6, ai, mapa, False))
    aiStructures.append(TerranBuilder(20, 12, ai, mapa, False, raton))

    for structure in aiStructures:
        ai.addStructures(structure)
        
    ai.setBasePlayer(aiStructures[0])

    #Recursos del mapa
    crystal = Crystal(2, 10, 34)
    crystal2 = Crystal(2, 18, 60)
    crystal3 = Crystal(2, 22, 60)
    crystal4 = Crystal(2, 26, 60)
    crystal5 = Crystal(12, 12, 200)
    gas = Geyser(16, 13, 50)

    resources = []
    resources.append(crystal)
    resources.append(crystal2)
    resources.append(crystal3)
    resources.append(crystal4)
    resources.append(crystal5)
    resources.append(gas)
    resources.append(gas2)
    escena.resources = resources

def update():
    clock_update()
    raton.update(escena.camera)

    if getGameState() == System_State.MAINMENU:
        playMusic(mainMenuBGM, pos = 5)
        #playSound(mainMenuBGM)
        escena.interfaz.update(escena,raton, escena.camera)
    elif getGameState() == System_State.MAP1:
        #playMusic(map1BGM)
        #cargar mapa
        escena.mapa = mapa
        escena.mapa.load()
        escena.mapa.loadMinimap()
        setEntity(player1, player2)
        setGameState(System_State.ONGAME)
    elif getGameState() == System_State.ONGAME:
        escena.update()
    elif getGameState() == System_State.GAMESELECT:
        #Cargar las partidas
        escena.interfaz.update(escena,raton, escena.camera)
    elif getGameState() == System_State.NEWGAME:
        escena.interfaz.update(escena,raton, escena.camera)
    else: #STATE == System_State.EXIT:
        pg.quit()
        sys.exit()

def draw():
    screen.fill(WHITE)
    if Utils.state == System_State.MAINMENU:
        escena.interfaz.draw(screen, escena.camera)
    elif Utils.state == System_State.ONGAME:
        escena.draw(screen)
    elif Utils.state == System_State.GAMESELECT or Utils.state == System_State.NEWGAME:
        escena.interfaz.draw(screen, escena.camera)
    raton.draw(screen, escena.camera)
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

mapa = Map.Map(40, 40, True)
#mapa.setElevacion(16, 3)
#mapa.setElevacion(20, 14)
#mapa.setElevacion(17, 30)
#mapa.setElevacion(12, 20)
#mapa.setElevacion(8, 35)
#mapa.setElevacion(5, 12)
#mapa.setElevacion(32, 29)

player1 = Player.Player([], [], 400, keyMap, commandMap, mapa, True)

# Raton


# Player 2 AKA IA
player2 = Player.Player([], [], 800, {}, {}, mapa, False)
aI = AI(player2, Race.TERRAN, HARD)

# Camara
# pre: mapa tan grande como ventana
camera = Camera(0, 0, SCREEN_HEIGHT - 160, SCREEN_WIDTH)

# Escena



raton = Raton.Raton(player1, player2, mapa)
p1Interface = Interface(player1, player2, raton)
raton.addInterface(p1Interface)

escena = Escena(player1, player2, aI, [], camera, raton, p1Interface, [])
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
