import time
import pygame as pg
import sys
import math
import json

from src.Utils import *
from src.Command import *
from src import Raton
from src.Interface import *
from src.AI import *
from src.Escena import *
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

escena = Escena(None, None, None, None, None, None, None, None)
escena.loadScene()

# Raton
sprite_ruta = "./SPRITE/raton/"
raton = Raton.Raton(sprite_ruta, escena.p1)

p1Interface = Interface(escena.p1, raton)

aI = AI(escena.p2)

escena.raton = raton
escena.interfaz = p1Interface
escena.aI = aI

def update():
    clock_update()
    raton.update(escena.camera)

    if Utils.state == System_State.MAINMENU:
        #playMusic(mainMenuBGM, pos = 5)
        #playSound(mainMenuBGM)
        p1Interface.update()
    elif Utils.state == System_State.MAP1:
        #playMusic(map1BGM)
        #cargar mapa
        escena.mapa.load()
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
    raton.draw(screen, escena.camera)
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
    updateGlobalTime()
