import pygame as pg
import math
from . import Entity
from .. import Utils, Command

class Unit(Entity.Entity):
    def __init__(self, hp, xIni, yIni, mineral_cost, generation_time, speed, framesToRefresh, 
                    sprites, face, frame, padding, id, player, minePower, timeToMine, dieOffset, inersibleFrames,
                        frames, dirOffset, attackFrames, stillFrames, moveFrames, dieFrames,  xPadding, yPadding, wPadding, hPadding):
        Entity.Entity.__init__(self, hp, xIni, yIni, mineral_cost, generation_time, id, player)
        # Relativo al movimiento de la unidad
        self.paths = []
        #self.basePath camino a la base para cuando este minando(Se setea cuando se da la orden de minar)
        #self.cristalPath camino al cristal para cuando este minando(Se setea cuando se da la orden de minar)
        self.speed = speed
        self.angle = 0

        #Relativo a estado
        self.clicked = False
        self.face = face
        self.frame = frame
        self.count = 0
        self.rectOffY = padding
        #self.order (se seteara cuando se de una orden)
        
        #Relativo a los frames
        self.dieOffset = dieOffset
        self.inersibleFrames = inersibleFrames
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
        elif self.state == Utils.State.ORE_TRANSPORTING: # Esta transportando mineral
            pass
        elif self.state == Utils.State.BARREL_TRANSPORTING: # Esta transportando barril
            pass
        elif self.state == Utils.State.MINING: # Esta minando
            self.updateMining()  

    #COMUN A TODAS LAS UNIDADES
    def updateStill(self):
        if len(self.paths) > 0:
            self.state = Utils.State.MOVING
        #aqui vendria un elif de si te atacan pasas a atacando(ESTA PARTE QUIZA NO, SE ESPECIFICARTA EN CLASES MAS ESPECIFICAS(WORKER/SOLDIER))
    
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
                    print(self.order['order'])
                    if self.order != 0:
                        if self.order['order'] == Command.CommandId.MOVER:
                            self.dir = 8
                            self.changeToStill()
                        elif self.order['order'] == Command.CommandId.MINAR:
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
                            self.dir = int(4 - (self.angle * 8 / math.pi)) % 16          
                            self.count = 0
                            self.changeToMining()
                        elif self.order['order'] == Command.CommandId.TRANSPORTAR_ORE:
                            #sumar minerales al jugador
                            if self.cristal.capacidad < 0:
                                self.player.resources += self.minePower + self.cristal.capacidad
                                self.changeToStill()
                                del self.cristal
                            else:
                                self.order = {'order': Command.CommandId.MINAR_BUCLE}
                                self.player.resources += self.minePower
                                self.paths = []
                                for path in self.cristalPath:
                                    self.paths.append(path.copy())
                                self.changeToMove()
                        elif self.order['order'] == Command.CommandId.MINAR_BUCLE:
                            #sumar minerales al jugador
                            self.dir = int(4 - (self.miningAngle * 8 / math.pi)) % 16          
                            self.count = 0
                            self.changeToMining()
                    else:
                        self.changeToStill()
        else:
            self.changeToStill()
    
    # Aplica un frame a la unidad muriendo
    def updateDying(self):
        self.count += 1
        if self.count >= self.framesToRefresh:
            self.count = 0
            if self.frame < (len(self.dieOffset) - 2):
                self.updateDyingImage()
            else:
                self.changeToDead()

    #Mining es especifica de worker por lo que lo implementa worker
    def updateMining(self):
        pass

    #Aplica un frame a la unidad atacando
    #def updateAttacking(self):


    # No es por meter mierda, pero a mi Zergling no lo cancela nadie, desgraciados(PUES YO SI :P)
    def cancel(self):
        self.paths = []
    
    def mirrorTheChosen(self):
        print(self.inersibleFrames)
        for i in range(self.inersibleFrames):
            for j in range(9, 16):
                self.sprites[self.frames[i][self.dirOffset[j]]] = pg.transform.flip(
                        self.sprites[self.frames[i][self.dirOffset[j]]], True, False)

    # Es darle un valor a un booleano, nada mas y nada menos
    def setClicked(self, click):
        self.clicked = click
    
    # Es leer el valor del booleano de antes, se le suele llamar get
    def isClicked(self):
        return self.clicked
    
    def changeToMining(self):
        self.state = Utils.State.MINING
        self.frame = 0
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]
    # Pasa a estado quieto
    def changeToStill(self):
        self.state = Utils.State.STILL
        self.image = self.sprites[self.frames[self.stillFrames][self.dirOffset[self.dir]]]

    # Pasa a estado moverse
    def changeToMove(self):
        self.state = Utils.State.MOVING
        self.frame = 0
        self.image = self.sprites[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]
        
    # Pasa al ataque HYAAAA!! >:c
    def changeToAttack(self):
        self.state = Utils.State.ATTACKING
        self.frame = 0
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    # Pasa a morirse (chof)
    def changeToDying(self):
        self.state = Utils.State.DYING
        self.frame = 0
        self.image = self.sprites[self.frames[self.dieFrames][self.dieOffset[self.frame]]]

    # Pasa a muerto (chof del todo)
    def changeToDead(self):
        self.state = Utils.State.DEAD
        self.frame += 1
        self.image = self.sprites[self.frames[self.dieFrames][self.dieOffset[self.frame]]]
    
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


    # Pasa de frame en una animacion mortal
    def updateDyingImage(self):
        if self.frame == len(self.dieOffset): # el ultimo frame es de muerte definitiva
            print("ERROR: Zergling muerto, como que matarlo mas?")
            exit(1)
        self.frame = self.frame + 1
        self.image = self.sprites[self.frames[self.dieFrames][self.dirOffset[self.dir]]]

    
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
        rectAux = pg.Rect(self.x - self.xPadding, 
                self.y - self.yPadding, self.image.get_width() - self.wPadding, self.image.get_height()  - self.hPadding)
        return rectAux
    
    
