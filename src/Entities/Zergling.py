import pygame as pg
import math

from . import Zerg, Entity
from .. import Utils

# Constantes
HP = 40
MINERAL_COST = 20
GENERATION_TIME = 200
SPEED = 2 
FRAMES_TO_REFRESH = 5
SPRITES = "zergling.bmp"
SPRITE_PIXEL_ROWS = 128
FACES = 8
FRAME = 0
TOTAL_FRAMES = 296  # [0:203] MOVICION (13 ciclos de 17 frames con solo 16 utiles)
                    # ciclo 0 estar quieto, ciclos 1 2 y 3 atacacion, el resto moverse
                    # [204:288] ENTERRACION
                    # [289:295] MORICION
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)), 
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)), 
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)), 
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(289, 296))]
STILL_FRAMES = 0
ATTACK_FRAMES = [1, 2, 3]
MOVE_FRAMES = [4, 5, 6, 7, 8, 9, 10, 11]
DIE_FRAMES = 12
DIE_OFFSET = [0, 1, 2, 3, 4, 5, 6]

INVERSIBLE_FRAMES = len(FRAMES) - 1 # los die frames no se invierten
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-frame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
PADDING = 110
ID = 3

class Zergling(Zerg.Zerg):
    # Pre: xIni e yIni marcan posiciones del mapa, (ej: (3, 2) se refiere a la posicion de 
    # la cuarta columna y tercera fila del mapa)
    # Post: Crea un bichito mono que no hace practicamente nada pero tu dale tiempo
    def __init__(self, xIni, yIni):
        Zerg.Zerg.__init__(self, HP, xIni * 40 + 20, yIni * 40 + 20, MINERAL_COST, 
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME, 
                PADDING, ID)
        spritesheet = pg.image.load("./sprites/" + self.spritesName)
        spritesheet.set_colorkey(Utils.BLACK)
        self.sprites = Entity.Entity.divideSpritesheetByRows(spritesheet, 
                SPRITE_PIXEL_ROWS)
        self.mirrorTheChosen()
        self.dir = 8
        self.changeToStill()
        self.imageRect = Utils.rect(self.x, self.y, self.image.get_width(), self.image.get_height() - self.rectOffY)


    # Aplica un frame mas a la unidad
    def update(self):
        if self.state == Utils.State.STILL: # Esta quieto
            self.updateStill()
        elif self.state == Utils.State.MOVING: # Esta moviendose
            self.updateMoving()
        elif self.state == Utils.State.ATTACKING: # Esta atacando
            self.updateAttacking()
        elif self.state == Utils.State.DYING: # Esta muriendose
            self.updateDying()
        elif self.state == Utils.State.DEAD: # Esta muerto
            pass

    def updateStill(self):
        if len(self.paths) > 0:
            self.state = Utils.State.MOVING
        #aqui vendria un elif de si te atacan pasas a atacando

    def addPath(self, path):
        self.paths.apend(path)

    def updateMoving(self):
        actualPath = self.paths[0]
        if actualPath.dist > 0: # Aun queda trecho
            if actualPath.angle < 0:
                self.angle = -actualPath.angle
            else:
                self.angle = 2 * math.pi - actualPath.angle            
            
            self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
            self.x = math.cos(actualPath.angle)
            self.y = math.sin(actualPath.angle)

            distrec = math.hypot((self.imageRect.x + self.x * self.speed) - 
                    self.imageRect.x, (self.imageRect.y + self.y * self.speed) 
                    - self.imageRect.y)
            actualPath.dist -= distrec
            self.imageRect.x += self.x * self.speed
            self.imageRect.y += self.y * self.speed

            self.count += 1
            if self.count >= self.framesToRefresh:
                self.count = 0
                self.updateMovingImage()
        else: # Se acaba este camino
            self.paths.pop(0)
            if len(self.paths) == 0:
                self.changeToStill()

    # Devuelve la posicion en coordenadas del propio mapa
    def getPosition(self):
        return (self.imageRect.x, self.imageRect.y)

    # Devuelve el rectangulo que conforma su imagen, creo, esto lo hizo otro
    def getRect(self):
        rectAux = pg.Rect(self.imageRect.x - self.imageRect.w / 2, 
                self.imageRect.y - self.imageRect.h, self.imageRect.w, self.imageRect.h)
        return rectAux

    def cancel(self):
        self.paths = []

    # Genera los sprites que son inversos, es todo un artista
    def mirrorTheChosen(self):
        for i in range(INVERSIBLE_FRAMES):
            for j in range(9, 16):
                self.sprites[FRAMES[i][DIR_OFFSET[j]]] = pg.transform.flip(
                        self.sprites[FRAMES[i][DIR_OFFSET[j]]], True, False)

    # Es darle un valor a un booleano, nada mas y nada menos
    def setClicked(self, click):
        self.clicked = click
        
    # Es leer el valor del booleano de antes, se le suele llamar get
    def isClicked(self):
        return self.clicked

    def changeToStill(self):
        self.state = Utils.State.STILL
        self.image = self.sprites[FRAMES[STILL_FRAMES][DIR_OFFSET[self.dir]]]

    def changeToMove(self):
        self.state = Utils.State.MOVING
        self.frame = 0
        self.image = self.sprites[FRAMES[MOVE_FRAMES[self.frame]][DIR_OFFSET[self.dir]]]
        
    def changeToAttack(self):
        self.state = Utils.State.ATTACKING
        self.frame = 0
        self.image = self.sprites[FRAMES[ATTACK_FRAMES[self.frame]][DIR_OFFSET[self.dir]]]

    def changeToDying(self):
        self.state = Utils.State.DYING
        self.frame = 0
        self.image = self.sprites[FRAMES[DIE_FRAMES][DIE_OFFSET[self.frame]]]

    def die(self):
        self.state = Utils.State.DEAD
        self.frame = len(DIE_OFFSET)
        self.image = self.sprites[FRAMES[DIE_FRAMES][DIE_OFFSET[self.frame]]]

    def updateStillImage(self):
        self.frame = (self.frame + 1) % len(STILL_FRAMES)
        self.image = self.sprites[FRAMES[STILL_FRAMES][DIR_OFFSET[self.dir]]]
        
    def updateMovingImage(self):
        self.frame = (self.frame + 1) % len(MOVE_FRAMES)
        self.image = self.sprites[FRAMES[MOVE_FRAMES[self.frame]][DIR_OFFSET[self.dir]]]
    
    def updateAttackingImage(self):
        self.frame = (self.frame + 1) % len(ATTACK_FRAMES)
        self.image = self.sprites[FRAMES[ATTACK_FRAMES[self.frame]][DIR_OFFSET[self.dir]]]

    def updateDyingImage(self):
        if self.frame == len(DIE_FRAMES):
            print("ERROR: Zergling muerto, como que matarlo mas?")
            exit(1)
        self.frame = self.frame + 1
        self.image = self.sprites[FRAMES[DIE_FRAMES][DIR_OFFSET[self.dir]]]