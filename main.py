import time
import pygame as pg
import sys
import math
import json
from datetime import datetime


from src.Entities.TerranSoldier import *

from src import Utils
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
from src.Entities.ZergBarracks import *
#from src.Entities.Zerg2 import *
from src.Entities.ZergSupply import *


# Auxiliar del bucle principal
def procesarInput():
    for event in pg.event.get(): #Identificar lo sucedido en la ventana
        #print(event)
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.VIDEORESIZE:
            print("resize")
            Utils.resized = True
        elif event.type == pg.KEYUP:
            escena.procesarEvent(event)
            escena.checkUnHoldButton(event.key)
        elif getGameState() == System_State.SETTINGS and getGameState2() == System_State.KEY_BINDING:
            escena.interfaz.processEvent(event)
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
    #structure3 = TerranSupplyDepot(4, 4, player, mapa, True)
    #structure7 = Hatchery(10, 23, player, mapa, True, raton)

    player.setBasePlayer(structure1)
    structure2 = ZergBarracks(15, 9, player, mapa, False)
    gas2 = Geyser(13, 20, 50)
    #structure4 = Extractor(12, 27, player, mapa, True)
    structure5 = TerranRefinery(13, 18, ai, mapa, True, gas2)

    structure6 = ZergBarracks(7, 16, ai, mapa, True)
    #structure8 = Zerg2(2, 14, ai, mapa, True)
    #structure9 = Zerg3(8, 20, ai, mapa, True)

    player.addStructures(structure1)
    player.addStructures(structure6)
    #player.addStructures(structure8)
    #player.addStructures(structure9)
    player.addStructures(structure2)
    #player.addStructures(structure4)
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
    aiStructures.append(TerranBuilder(6, 4, ai, mapa, False, raton))
    aiStructures.append(TerranBarracks(12, 6, ai, mapa, False))

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
    if Utils.resized:
        Utils.resized = False
        updateScreen(screen)
        camera.update()
    clock_update()
    raton.update(escena.camera)
    if getGameState() == System_State.MAINMENU:
        playMusic(mainMenuBGM, pos = 5)
        #playSound(mainMenuBGM)
        escena.interfaz.update(escena,raton, escena.camera)
        '''elif getGameState() == System_State.MAP1:
        stopMusic()
        playMusic(map1BGM)
        #cargar mapa
        escena.mapa = mapa
        escena.mapa.load()
        escena.mapa.loadMinimap()
        setEntity(player1, player2)
        setGameState(System_State.ONGAME)
        setGameState2(System_State.LOAD)'''
    elif getGameState() == System_State.ONGAME:
        escena.update()
    elif getGameState() == System_State.GAMESELECT:
        #Cargar las partidas
        escena.interfaz.update(escena,raton, escena.camera)
    elif getGameState() == System_State.NEWGAME:
        escena.interfaz.update(escena,raton, escena.camera)
    elif  getGameState() == System_State.SETTINGS:
        escena.interfaz.update(escena,raton, escena.camera)
    else: #STATE == System_State.EXIT:
        pg.quit()
        sys.exit()

def draw():
    screen.fill(BLACK)
    if Utils.state == System_State.MAINMENU:
        escena.interfaz.draw(screen, escena.camera)
    elif Utils.state == System_State.ONGAME:
        escena.draw(screen)
    elif Utils.state == System_State.PAUSED:
        escena.draw(screen)
    elif (Utils.state == System_State.GAMESELECT or Utils.state == System_State.NEWGAME
    or Utils.state == System_State.SETTINGS):
        escena.interfaz.draw(screen, escena.camera)
    raton.draw(screen, escena.camera)
    #aux(screen)
    pg.display.flip()

# Programa principal
pg.init()

flags = pg.FULLSCREEN | pg.DOUBLEBUF
size = (MIN_SCREEN_WIDTH, MIN_SCREEN_HEIGHT)
screen =  pg.display.set_mode(size, pg.RESIZABLE) #, pg.RESIZABLE)

Utils.init()

#Controlar frames por segundo
clock = pg.time.Clock()

# Player 1
'''
keyMap = {
  pg.K_w: CommandId.MOVE_CAMERA_UP,
  pg.K_s: CommandId.MOVE_CAMERA_DOWN,
  pg.K_d: CommandId.MOVE_CAMERA_RIGHT,
  pg.K_a: CommandId.MOVE_CAMERA_LEFT,
  pg.K_e: CommandId.BUILD_BARRACKS,
  pg.K_r: CommandId.BUILD_DEPOT,
  pg.K_t: CommandId.BUILD_REFINERY,
  pg.K_z: CommandId.GENERATE_T1,
  pg.K_x: CommandId.GENERATE_T2,
  pg.K_c: CommandId.GENERATE_T3,
  pg.K_q: CommandId.GENERATE_WORKER,
  pg.K_i: CommandId.UPGRADE_SOLDIER_DAMAGE,
  pg.K_o: CommandId.UPGRADE_SOLDIER_ARMOR,
  pg.K_p: CommandId.UPGRADE_WORKER_MINING,
  pg.K_g: CommandId.SAVE_GAME,
  pg.K_m: CommandId.ROTATE,
  pg.K_f: CommandId.DESELECT,
}
commandMap = {
  CommandId.MOVE_CAMERA_UP: pg.K_w,
  CommandId.MOVE_CAMERA_DOWN: pg.K_s,
  CommandId.MOVE_CAMERA_RIGHT: pg.K_d,
  CommandId.MOVE_CAMERA_LEFT: pg.K_a,
  CommandId.BUILD_BARRACKS: pg.K_e,
  CommandId.BUILD_DEPOT: pg.K_r,
  CommandId.BUILD_REFINERY: pg.K_t,
  CommandId.GENERATE_T1: pg.K_z,
  CommandId.GENERATE_T2: pg.K_x,
  CommandId.GENERATE_T3: pg.K_c,
  CommandId.GENERATE_WORKER: pg.K_q,
  CommandId.UPGRADE_SOLDIER_DAMAGE: pg.K_i,
  CommandId.UPGRADE_SOLDIER_ARMOR: pg.K_o,
  CommandId.UPGRADE_WORKER_MINING: pg.K_p,
  CommandId.SAVE_GAME: pg.K_g,
  CommandId.ROTATE: pg.K_m,
  CommandId.DESELECT: pg.K_f,
}
'''
mapa = Map.Map(40, 40, True)
#mapa.setElevacion(16, 3)
#mapa.setElevacion(20, 14)
#mapa.setElevacion(17, 30)
#mapa.setElevacion(12, 20)
#mapa.setElevacion(8, 35)
#mapa.setElevacion(5, 12)
#mapa.setElevacion(32, 29)

keyMap, commandMap = loadkeyShortcuts()
player1 = Player.Player([], [], 500, keyMap, commandMap, mapa, True)

# Raton


# Player 2 AKA IA
player2 = Player.Player([], [], 500, {}, {}, mapa, False)
aI = AI(player2, Race.TERRAN, HARD)

# Camara
# pre: mapa tan grande como ventana
camera = Camera(0, 0, Utils.ScreenWidth, Utils.ScreenHeight)

# Escena



raton = Raton.Raton(player1, player2, mapa)
p1Interface = Interface(player1, player2, raton, keyMap, commandMap)
raton.addInterface(p1Interface)

escena = Escena(player1, player2, aI, [], camera, raton, p1Interface, [])
raton.setEscena(escena)
#escena.mapa.addOre(100,100)

# Bucle principal
while True:

    #Procesar inputs
    procesarInput()

    #Actualizar entidades del juego
    update()


    #Dibujar
    now = datetime.now()
    draw()
    #print((datetime.now() - now).microseconds)
    updateGlobalTime(clock)
