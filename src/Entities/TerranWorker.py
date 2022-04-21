import pygame as pg
import math

from .. import Command

from . import Worker, Entity
from .. import Utils

# Constantes
HP = 40
MINERAL_COST = 20
TIME_TO_MINE = 1000
GENERATION_TIME = 2
SPEED = 4
FRAMES_TO_REFRESH = 10
SPRITES = "scvJusto.bmp"
SPRITE_PIXEL_ROWS = 72
FACES = 8
FRAME = 0
TOTAL_FRAMES = 296  # [0:15] MOVERSE Y STILL
                    # [16:31] MOVER ORE
                    # [32:47] MOVER BARRIL
                    # [48:217] ATACAR Y MINAR
                    # [289:295] MORICION
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)), 
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)), 
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)), 
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(205, 221)), list(range(289, 296))]
STILL_FRAMES = 0
ORE_TRANSPORTING_FRAMES = 3
BARREL_TRANSPORTING_FRAMES = 4
ATTACK_FRAMES = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
MOVE_FRAMES = [0]
DIE_FRAMES = 13
DIE_OFFSET = [0, 1, 2, 3, 4, 5, 6]

INVERSIBLE_FRAMES = len(FRAMES) - 1 # los die frames no se invierten
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-flist(range(289, 296))rame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
WEIGHT_PADDING =    64
HEIGHT_PADDING =    60
X_PADDING =         40
Y_PADDING =         47
PADDING = 110

class TerranWorker(Worker.Worker):
    def __init__(self, xIni, yIni, id, player):
        Worker.Worker.__init__(self, HP, xIni * 40 + 20, yIni * 40 + 20, MINERAL_COST, 
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME, 
                PADDING, id, player)
        spritesheet = pg.image.load("./sprites/" + self.spritesName).convert()
        spritesheet.set_colorkey((Utils.BLACK))
        self.sprites = Entity.Entity.divideSpritesheetByRows(spritesheet, 
                SPRITE_PIXEL_ROWS)
        self.mirrorTheChosen()
        self.dir = 0
        self.changeToStill()
        self.minePower = 8
        print(self.x, self.y,self.image.get_width(),self.image.get_height() )
        print(self.getRect().x - self.getRect().w,self.getRect().y - self.getRect().h)
        #self.imageRect = Utils.rect(self.x, self.y, self.image.get_width() - WEIGHT_PADDING, 
                #self.image.get_height() - HEIGHT_PADDING)
        #self.imageRect = Utils.rect(self.x - self.image.get_width()/2, self.y -self.image.get_height() , self.image.get_width(), self.image.get_height())
        #self.imageRect = Utils.rect(self.x, self.y, self.image.get_width(), self.image.get_height())
    def setOrder(self, order):
        self.order = order
    def setCristal(self, cristal):
        self.cristal = cristal
    def setCaminoABase(self, path):
        self.basePath = path
    
    def getPosition(self):
        r = self.getRect()
        return(r.x + r.w/2, r.y + r.h)
    def getDrawPosition(self):
        return(self.x - self.image.get_width()/2,  self.y - self.image.get_height()/2)
    # Devuelve el rectangulo que conforma su imagen, creo, esto lo hizo otro
    def getRect(self):
        rectAux = pg.Rect(self.x - X_PADDING, 
                self.y - Y_PADDING, self.image.get_width() - WEIGHT_PADDING, self.image.get_height()  - HEIGHT_PADDING)
        return rectAux
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
        elif self.state == Utils.State.ORE_TRANSPORTING: # Esta muerto
            pass
        elif self.state == Utils.State.BARREL_TRANSPORTING: # Esta muerto
            pass
        elif self.state == Utils.State.MINING: # Esta minando
              self.updateMinig()  
    # Aplica un frame a la unidad quieta(LO DE COUNT LO TENGO DE DEBUG)
    def updateStill(self):
        if len(self.paths) > 0:
            self.state = Utils.State.MOVING
        #aqui vendria un elif de si te atacan pasas a atacando
    
    def updateMinig(self):
        self.count += pg.time.Clock().tick(Utils.CLOCK_PER_SEC)
        if self.count > TIME_TO_MINE: #Termina de minar
            self.order = {'order':Command.CommandId.TRANSPORTAR_ORE}
            self.cristal.getMined(self.minePower)
            print(self.basePath.__len__())
            self.paths = self.basePath
            self.state = Utils.State.MOVING
        if Utils.frame(FRAMES_TO_REFRESH):
            self.updateMiningImage()
        if len(self.paths) > 0:
            self.state = Utils.State.MOVING

    # Aplica un frame de la unidad en movimiento
    def updateMoving(self):
        if self.paths.__len__() != 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                if actualPath.angle < 0:
                    self.angle = -actualPath.angle
                else:
                    self.angle = 2 * math.pi - actualPath.angle          
                
                self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
                self.dirx = math.cos(actualPath.angle)
                self.diry = math.sin(actualPath.angle)
                pos = self.getPosition()
                distrec = math.hypot((pos[0] + self.dirx * self.speed) - 
                        pos[0], (pos[1] + self.diry * self.speed) 
                        - pos[1])
                actualPath.dist -= distrec
                self.x += self.dirx * self.speed
                self.y += self.diry * self.speed

                self.count += 1
                if self.count >= self.framesToRefresh:
                    self.count = 0
                    self.updateMovingImage()
            else: # Se acaba este camino
                self.paths.pop(0)
                if len(self.paths) == 0:
                    print(self.order)
                    if self.order != 0:
                        if self.order['order'] == Command.CommandId.MOVER:
                            self.dir = 8
                            self.changeToStill()
                        elif self.order['order'] == Command.CommandId.MINAR:
                            angle = self.order['angle']
                            self.basePath = self.order['basePath']
                            self.cristal = self.order['cristal']
                            for path in self.basePath:
                                print("Posicion final a casa: ",path.posFin, path.angle)
                            if angle < 0:
                                self.angle = -angle
                            else:
                                self.angle = 2 * math.pi - angle
                            self.dir = int(4 - (self.angle * 8 / math.pi)) % 16          
                            self.count = 0
                            self.changeToMining()
                        elif self.order['order'] == Command.CommandId.TRANSPORTAR_ORE:
                            #sumar minerales al jugador
                            self.order = 0
                            self.player.resources += self.minePower
                            self.changeToStill()
                    else:
                        self.changeToStill()
        else:
            self.changeToStill()
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


    

    # No es por meter mierda, pero a mi Zergling no lo cancela nadie, desgraciados
    def cancel(self):
        self.paths = []
        
    # Introduce un nuevo camino a la lista de caminos
    def addPath(self, path):
        self.paths.append(path)

    # Genera los sprites que son inversos, es todo un artista
    def mirrorTheChosen(self):
        print(INVERSIBLE_FRAMES)
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

    def changeToMining(self):
        self.state = Utils.State.MINING
        self.image = self.sprites[FRAMES[ATTACK_FRAMES[self.frame]][DIR_OFFSET[self.dir]]]
    # Pasa a estado quieto
    def changeToStill(self):
        self.state = Utils.State.STILL
        self.image = self.sprites[FRAMES[STILL_FRAMES][DIR_OFFSET[self.dir]]]

    # Pasa a estado moverse
    def changeToMove(self):
        self.state = Utils.State.MOVING
        self.frame = 0
        self.image = self.sprites[FRAMES[MOVE_FRAMES[self.frame]][DIR_OFFSET[self.dir]]]
        
    # Pasa al ataque HYAAAA!! >:c
    def changeToAttack(self):
        self.state = Utils.State.ATTACKING
        self.frame = 0
        self.image = self.sprites[FRAMES[ATTACK_FRAMES[self.frame]][DIR_OFFSET[self.dir]]]

    # Pasa a morirse (chof)
    def changeToDying(self):
        self.state = Utils.State.DYING
        self.frame = 0
        self.image = self.sprites[FRAMES[DIE_FRAMES][DIE_OFFSET[self.frame]]]

    # Pasa a muerto (chof del todo)
    def changeToDead(self):
        self.state = Utils.State.DEAD
        self.frame += 1
        self.image = self.sprites[FRAMES[DIE_FRAMES][DIE_OFFSET[self.frame]]]

    # Pasa de frame en los frames quietos, no cambia nada puesto que esta quieto
    def updateStillImage(self):
        self.frame = (self.frame + 1) % len(STILL_FRAMES)
        self.image = self.sprites[FRAMES[STILL_FRAMES][DIR_OFFSET[self.dir]]]
        
    # Pasa de frame en animaciones de movimiento
    def updateMovingImage(self):
        self.frame = (self.frame + 1) % len(MOVE_FRAMES)
        self.image = self.sprites[FRAMES[MOVE_FRAMES[self.frame]][DIR_OFFSET[self.dir]]]
    
    # Pasa de frame en una animacion de ataque
    def updateAttackingImage(self):
        self.frame = (self.frame + 1) % len(ATTACK_FRAMES)
        self.image = self.sprites[FRAMES[ATTACK_FRAMES[self.frame]][DIR_OFFSET[self.dir]]]

    # Pasa de frame en una animacion de minado
    def updateMiningImage(self):
        self.frame = (self.frame + 1) % len(ATTACK_FRAMES)
        self.image = self.sprites[FRAMES[ATTACK_FRAMES[self.frame]][DIR_OFFSET[self.dir]]]

    # Pasa de frame en una animacion mortal
    def updateDyingImage(self):
        if self.frame == len(DIE_OFFSET): # el ultimo frame es de muerte definitiva
            print("ERROR: Zergling muerto, como que matarlo mas?")
            exit(1)
        self.frame = self.frame + 1
        self.image = self.sprites[FRAMES[DIE_FRAMES][DIR_OFFSET[self.dir]]]