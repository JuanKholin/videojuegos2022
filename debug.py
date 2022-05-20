import time
import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pg
import sys
import math
import json
from datetime import datetime
'''
import win32gui, win32con

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide , win32con.SW_HIDE)'''


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
from src.Entities.Firebat import *
from src.Entities.Goliath import *
from src.Entities.Hydralisk import *
from src.Entities.Broodling import *



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
    scv = Firebat(player, 10, 3)
    player.addUnits(scv)
    scv = TerranWorker(player, 11, 3)
    player.addUnits(scv)
    scv = TerranWorker(player, 12, 3)
    player.addUnits(scv)
    scv = TerranWorker(player, 11, 4)
    player.addUnits(Goliath(player, 13, 5))
    player.addUnits(Goliath(player, 13, 7))
    player.addUnits(Goliath(player, 13, 6))
    player.addUnits(scv)
    structure1 = Hatchery(3, 3, player, mapa, False, raton)
    player.addStructures(structure1)
    structure1 = TerranBarracks(7, 7, player, mapa, False)
    player.addStructures(structure1)
    player.setBasePlayer(structure1)
    scv = Goliath(ai, 20, 3)
    ai.addUnits(scv)
    structure1 = TerranBuilder(37, 3, ai, mapa, False, raton)
    ai.setBasePlayer(structure1)
    ai.addStructures(structure1)
    structure1 = TerranBarracks(15, 7, ai, mapa, False)
    ai.addStructures(structure1)
    structure1 = TerranBarracks(15, 3, ai, mapa, False)
    ai.addStructures(structure1)
    

    resources = []
    crystal = Crystal(3, 10, 800)
    resources.append(crystal)
    crystal = Crystal(37, 10, 800)
    resources.append(crystal)
    gas = Geyser(7, 7, 8)
    resources.append(gas)
    escena.resources = resources
    '''
    #scv = TerranWorker(player, 20, 20)
    #player.addUnits(scv)
    scv = Drone(player, 24, 32)
    player.addUnits(scv)
    structure1 = Hatchery(20, 35, player, mapa, False, raton)
    player.addStructures(structure1)
    player.setBasePlayer(structure1)

    #Recursos del mapa
    resources = []
    crystal = Crystal(33, 32, 800)
    resources.append(crystal)
    crystal = Crystal(29, 30, 800)
    resources.append(crystal)
    crystal = Crystal(25, 28, 800)
    resources.append(crystal)

    units = []
    units.append(Firebat(player, 25, 30))
    units.append(Goliath(player, 27, 30))
    units.append(Hydralisk(player, 29, 30))
    units.append(Guardian(player, 31, 30))


    for unit in units:
        player.addUnits(unit)


    gas = Geyser(30, 5, 800)
    resources.append(gas)

    scv = TerranWorker(ai, 12, 5)
    ai.addUnits(scv)
    structure1 = TerranBuilder(20, 5, ai, mapa, False, raton)
    ai.addStructures(structure1)
    ai.setBasePlayer(structure1)

    #Recursos del mapa

    crystal = Crystal(7, 8, 800)
    resources.append(crystal)
    crystal = Crystal(11, 10, 800)
    resources.append(crystal)
    crystal = Crystal(15, 12, 800)
    resources.append(crystal)


    gas = Geyser(10, 35, 800)
    resources.append(gas)


    crystal = Crystal(22, 23, 800)
    resources.append(crystal)

    crystal = Crystal(27, 20, 800)
    resources.append(crystal)

    crystal = Crystal(18, 16, 800)
    resources.append(crystal)

    crystal = Crystal(12, 19, 800)
    resources.append(crystal)

    gas = Geyser(6, 13, 800)
    resources.append(gas)

    gas = Geyser(35, 25, 800)
    resources.append(gas)
    escena.resources = resources


   '''

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
    elif getGameState() == System_State.MAP1:
        stopMusic()
        playMusic(map1BGM)
        #cargar mapa
        escena.mapa = mapa
        escena.mapa.load()
        escena.mapa.loadMinimap()
        setEntity(player1, player2)
        setGameState(System_State.ONGAME)
        setGameState2(System_State.LOAD)
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
pg.display.set_caption('Starcraft')
icon = pg.image.load('icon.png')
pg.display.set_icon(icon)
flags = pg.FULLSCREEN | pg.DOUBLEBUF
size = (Utils.ScreenWidth, Utils.ScreenHeight)
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
  pg.K_x: CommandId.DESELECT,
  pg.K_d: CommandId.UPGRADE_SOLDIER_DAMAGE,
  pg.K_s: CommandId.UPGRADE_SOLDIER_ARMOR,
  pg.K_a: CommandId.SEARCH_NEARBY_RIVAL,
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



player1 = Player.Player([], [], 600, keyMap, commandMap, mapa, True)
player1.gas = 100
# Raton


# Player 2 AKA IA
player2 = Player.Player([], [], 100, {}, {}, mapa, False)


# Camara
# pre: mapa tan grande como ventana
camera = Camera(0, 0, Utils.ScreenHeight - 160, Utils.ScreenWidth)

# Escena



raton = Raton.Raton(player1, player2, mapa)
p1Interface = Interface(player1, player2, raton, keyMap, commandMap)
raton.addInterface(p1Interface)
if Utils.DEBBUG == False:
    aI = AI(player2, Race.TERRAN, HARD)

else:
    aI = AI(player2, Race.TERRAN, NULL)
escena = Escena(player1, player2, aI, [], camera, raton, p1Interface, [])

raton.setEscena(escena)
Utils.init()


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
