import pygame as pg
import math
from .Entity import *
from ..Utils import *
from ..Command import *

class Unit(Entity):
    def __init__(self, hp, xIni, yIni, mineral_cost, generation_time, speed, framesToRefresh, 
                    sprites, face, frame, padding, id, player, minePower, timeToMine, dieOffset, inversibleFrames,
                        frames, dirOffset, attackFrames, stillFrames, moveFrames, dieFrames,  xPadding, yPadding, wPadding, hPadding):
        Entity.__init__(self, hp, xIni, yIni, mineral_cost, generation_time, id, player)
        # Relativo al movimiento de la unidad
        self.paths = []
        #self.basePath camino a la base para cuando este minando(Se setea cuando se da la orden de minar)
        #self.cristalPath camino al cristal para cuando este minando(Se setea cuando se da la orden de minar)
        self.speed = speed
        self.angle = 0

        #Relativo a estado
        self.state = State.STILL
        self.clicked = False
        self.face = face
        self.frame = frame
        self.count = 0
        self.rectOffY = padding
        self.order = {'order': 0}
        
        #Relativo a los frames
        self.dieOffset = dieOffset
        self.inversibleFrames = inversibleFrames
        self.framesToRefresh = framesToRefresh
        self.spritesName = sprites
        self.sprites = []
        self.frames = frames
        self.dirOffset = dirOffset
        self.attackFrames = attackFrames
        self.stillFrames = stillFrames
        self.moveFrames = moveFrames
        self.dieFrames = dieFrames
        self.xPadding = xPadding
        self.yPadding = yPadding
        self.wPadding = wPadding
        self.hPadding = hPadding
        #self.distanceToPoint = 0

        self.minePower = minePower
        self.timeToMine = timeToMine

    def update(self):
        #print(self.state)
        if self.state == State.STILL: # Esta quieto
            self.updateStill()
        elif self.state == State.MOVING: # Esta moviendose
            self.updateMoving()
        elif self.state == State.ATTACKING: # Esta atacando
            self.updateAttacking()
        elif self.state == State.DYING: # Esta muriendose
            self.updateDying()
        elif self.state == State.DEAD: # Esta muerto
            pass
        elif self.state == State.ORE_TRANSPORTING: # Esta transportando mineral
            self.updateOreTransporting()
        elif self.state == State.BARREL_TRANSPORTING: # Esta transportando barril
            pass
        elif self.state == State.MINING: # Esta minando
            self.updateMining()

    #COMUN A TODAS LAS UNIDADES
    def updateStill(self):
        if len(self.paths) > 0:
            self.state = State.MOVING
        #aqui vendria un elif de si te atacan pasas a atacando(ESTA PARTE QUIZA NO, SE ESPECIFICARTA EN CLASES MAS ESPECIFICAS(WORKER/SOLDIER))
    
    def updateMoving(self):
        if self.paths.__len__() != 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
            else: # Se acaba este camino
                self.finishPath()
        else:
            self.changeToStill()

    def updatePath(self, actualPath):
        if actualPath.angle < 0:
            self.angle = -actualPath.angle
        else:
            self.angle = 2 * math.pi - actualPath.angle          
                
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
        self.dirx = math.cos(actualPath.angle)
        self.diry = math.sin(actualPath.angle)
        pos = self.getPosition()
        distrec = math.hypot((pos[0] + self.dirx * self.speed) - pos[0], 
                (pos[1] + self.diry * self.speed) - pos[1])
        actualPath.dist -= distrec
        self.x += self.dirx * self.speed
        self.y += self.diry * self.speed

        self.count += 1
        if self.count >= self.framesToRefresh:
            self.count = 0
            self.updateMovingImage()

    def finishPath(self):
        self.paths.pop(0)
        if len(self.paths) == 0:
            print("ORDEN AL FINALIZAR CAMINO:" ,self.order['order'])
            if self.order != 0:
                if self.order['order'] == CommandId.MOVER:
                    self.changeToStill()
                elif self.order['order'] == CommandId.MINAR:
                    self.miningAngle = self.order['angle']
                    self.basePath = self.order['basePath']
                    self.cristalPath = self.order['cristalPath']
                    self.cristal = self.order['cristal']
                    #for path in self.basePath:
                        #print("Posicion final a casa: ",path.posFin, path.angle)
                    if self.miningAngle < 0:
                        self.angle = -self.miningAngle
                    else:
                        self.angle = 2 * math.pi - self.miningAngle
                    self.miningAngle = self.angle
                    self.changeToMining()
                elif self.order['order'] == CommandId.TRANSPORTAR_ORE:
                    #sumar minerales al jugador
                    if self.cristal.capacidad < 0:
                        self.player.resources += self.minePower + self.cristal.capacidad
                        self.changeToStill()
                        del self.cristal
                    else:
                        self.order = {'order': CommandId.MINAR_BUCLE}
                        self.player.resources += self.minePower
                        self.paths = []
                        for path in self.cristalPath:
                            self.paths.append(path.copy())
                        self.changeToMove()
                elif self.order['order'] == CommandId.MINAR_BUCLE:
                    #sumar minerales al jugador         
                    self.changeToMining()
            else:
                self.changeToStill()

    # Aplica un frame a la unidad muriendo
    def updateDying(self):
        self.count += 1
        if self.count >= self.framesToRefresh:
            self.count = 0
            if self.frame < (len(self.dieOffset) - 2): # el ultimo frame es muerto del todo
                self.updateDyingImage()
            else: # muerto del todo:
                self.changeToDead()

    # Mining es especifica de worker por lo que lo implementa worker
    def updateMining(self):
        pass

    # Aplica un frame a la unidad atacando
    def updateAttacking(self):
        pass

    # No es por meter mierda, pero a mi Zergling no lo cancela nadie, desgraciados(PUES YO SI :P) D:
    def cancel(self):
        self.paths = []
    
    # Para crear los sprites invertidos, los guarda en el mismo sitio que se indica
    def mirrorTheChosen(self):
        for i in range(self.inversibleFrames):
            for j in range(9, 16):
                self.sprites[self.frames[i][self.dirOffset[j]]] = pg.transform.flip(
                        self.sprites[self.frames[i][self.dirOffset[j]]], True, False)

    # Es darle un valor a un booleano, nada mas y nada menos
    def setClicked(self, click):
        self.clicked = click
    
    # Es leer el valor del booleano de antes, se le suele llamar get
    def isClicked(self):
        return self.clicked
    
    #Solo los worker pasan a minar
    def changeToMining(self):
        pass

    # Pasa a estado quieto
    def changeToStill(self):
        self.state = State.STILL
        self.image = self.sprites[self.frames[self.stillFrames][self.dirOffset[self.dir]]]

    # Pasa a estado moverse
    def changeToMove(self):
        self.state = State.MOVING
        self.frame = 0
        self.image = self.sprites[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]
        
    # Pasa al ataque HYAAAA!! >:c
    def changeToAttack(self):
        self.state = State.ATTACKING
        self.frame = 0
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    # Pasa a morirse (chof)
    def changeToDying(self):
        self.state = State.DYING
        self.frame = 0
        self.image = self.sprites[self.frames[self.dieFrames][self.dieOffset[self.frame]]]

    # Pasa a muerto (chof del todo)
    def changeToDead(self):
        self.state = State.DEAD
        self.frame += 1
        self.image = self.sprites[self.frames[self.dieFrames][self.dieOffset[self.frame]]]

    def changeToOreTransporting(self):
        pass
    
    # Pasa de frame en los frames quietos, no cambia nada puesto que esta quieto
    def updateStillImage(self):
        self.frame = (self.frame + 1) % len(self.stillFrames)
        self.image = self.sprites[self.frames[self.stillFrames][self.dirOffset[self.dir]]]
        
    # Pasa de frame en animaciones de movimiento
    def updateMovingImage(self):
        self.frame = (self.frame + 1) % len(self.moveFrames)
        self.image = self.sprites[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]
    
    # Pasa de frame en una animacion de ataque
    def updateAttackingImage(self):
        self.frame = (self.frame + 1) % len(self.attackFrames)
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    # Pasa de frame en una animacion de ataque
    def updateMiningImage(self):
        self.frame = (self.frame + 1) % len(self.attackFrames)
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    # Pasa de frame en una animacion mortal
    def updateDyingImage(self):
        if self.frame == len(self.dieOffset): # el ultimo frame es de muerte definitiva
            print("ERROR: Unidad muerta, como que matarla mas?")
            exit(1)
        self.frame = self.frame + 1
        print(self.frame, self.frames[self.dieFrames][self.dieOffset[self.frame]])
        self.image = self.sprites[self.frames[self.dieFrames][self.dieOffset[self.frame]]]
    
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

    def getRect(self):
        rectAux = pg.Rect(self.x - self.xPadding, 
                self.y - self.yPadding, self.image.get_width() - self.wPadding, self.image.get_height()  - self.hPadding)
        return rectAux
    
    
