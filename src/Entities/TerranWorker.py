import pygame as pg
import math

from . import Worker, Entity
from .. import Utils

# Constantes
HP = 40
MINERAL_COST = 20
GENERATION_TIME = 200
SPEED = 1
FRAMES_TO_REFRESH = 5
SPRITES = "terranWorker.bmp"
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
# horario y empezando desde el norte, el mapeo dir-flist(range(289, 296))rame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
PADDING = 110

class TerranWorker(Worker.Worker):
    def __init__(self, xIni, yIni, id):
        Worker.Worker.__init__(self, HP, xIni * 40 + 20, yIni * 40 + 20, MINERAL_COST, 
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME, 
                PADDING, id)
        spritesheet = pg.image.load("./sprites/" + self.spritesName)
        spritesheet.set_colorkey(Utils.BLACK)
        self.sprites = Entity.Entity.divideSpritesheetByRows(spritesheet, 
                SPRITE_PIXEL_ROWS)
        self.mirrorTheChosen()
        self.dir = 8
        self.changeToStill()
        self.imageRect = Utils.rect(self.x, self.y, self.image.get_width(), 
                self.image.get_height() - self.rectOffY)

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
    
     # Aplica un frame a la unidad quieta
    def updateStill(self):
        if len(self.paths) > 0:
            self.state = Utils.State.MOVING
        #aqui vendria un elif de si te atacan pasas a atacando
    
     # Aplica un frame de la unidad en movimiento
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
                self.changeToDying()
        
    # Aplica un frame a la unidad atacando
    #def updateAttacking(self):

    # Aplica un frame a la unidad muriendo
    def updateDying(self):
        self.count += 1
        if self.count >= self.framesToRefresh:
            self.count = 0
            if self.frame < (len(DIE_OFFSET) - 2):
                self.updateDyingImage()
            else:
                self.changeToDead()
    
    # Devuelve la posicion en coordenadas del propio mapa
    def getPosition(self):
        return (self.imageRect.x, self.imageRect.y)