import pygame as pg
import math
from .Entity import *
from ..Utils import *
from .. import Utils
from ..Command import *

class Unit(Entity):
    def __init__(self, hp, xIni, yIni, mineral_cost, generation_time, speed, framesToRefresh, 
                    sprites, face, frame, padding, id, player, minePower, timeToMine, inversibleFrames,
                        frames, dirOffset, attackFrames, stillFrames, moveFrames, dieFrames,  xPadding, yPadding, wPadding, hPadding, attackInfo):
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
        self.attackedOne = None
        
        #Relativo a los frames
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
        self.damage = attackInfo[DAMAGE_IND]
        self.cooldown = attackInfo[COOLDOWN_IND]
        self.range = attackInfo[RANGE_IND]
        self.attackedOne = None

    def update(self):
        #print(self.state)
        self.updateUnit()
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
        elif self.state == State.MOVING_TO_MINING: # Esta minando
            self.updateMovingToMining()

    #COMUN A TODAS LAS UNIDADES
    def updateStill(self):
        if len(self.paths) > 0:
            self.changeToMove()
        else:
            self.updateStillImage()
        #aqui vendria un elif de si te atacan pasas a atacando(ESTA PARTE QUIZA NO, SE ESPECIFICARTA EN CLASES MAS ESPECIFICAS(WORKER/SOLDIER))
    
    def updateMoving(self):
        if self.paths.__len__() != 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
            else: # Se acaba este camino
                self.finishPath()
            self.count += 1
            if self.count >= self.framesToRefresh:
                self.count = 0
                self.updateMovingImage()
        else:
            self.changeToStill()

    def updateMovingToMining():
        pass

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

    def finishPath(self):
        self.paths.pop(0)
        if len(self.paths) == 0:
            #print("ORDEN AL FINALIZAR CAMINO:" ,self.order['order'])
            if self.order != 0:
                if self.order['order'] == CommandId.MOVER:
                    if self.attackedOne == None:
                        self.changeToStill()
                    #else keepmoving xdxdxd
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
                    self.startTimeMining = getGlobalTime()
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
                    self.startTimeMining = getGlobalTime()     
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
        #MOVIMIENTO


        if self.attackedOne.getHP() > 0:
            if self.distance(self.attackedOne) <= self.rango:
                self.paths = [] #Me quedo quieto y ataco
                self.attackCD -= 1
                if self.attackCD == 0:
                    self.attack()
                    self.attackCD = self.cooldown
            else:
                # Recalcular camino
                self.changeToMove()
        else: # Se murio el objetivo, pasa a estar quieto
            self.attackedOne = None
            self.changeToStill()


    # Para inflingir un ataque a una unidad
    def attack(self):
        hpLeft = self.attackedOne.beingAttacked(self.damage)
        if hpLeft < 0:
            self.changeToStill()

    # Para reflejar sobre una unidad que recibe un ataque
    def beingAttacked(self, damage):
        if self.hp < damage:
            self.hp = 0
            self.changeToDying()
        else:
            self.hp -= damage
        return self.hp

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
        print("PASO AL ESTAR QUIETO")
        self.state = State.STILL
        self.frame = 0
        self.image = self.sprites[self.frames[self.stillFrames[self.frame]][self.dirOffset[self.dir]]]
        unitPos = self.getPosition()
        tileActual = self.mapa.getTile(unitPos[0], unitPos[1])
        tiles = self.mapa.getAllTileVecinas(tileActual)
        for tile in tiles:
            if tile.type != OBSTACLE:
                self.mapa.setLibre(tile)

    # Pasa a estado moverse
    def changeToMove(self):
        print("PASO AL MOVIMIENTO")
        self.state = State.MOVING
        self.frame = 0
        self.image = self.sprites[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]
        
    # Pasa al ataque HYAAAA!! >:c
    def changeToAttack(self, attackedOne):
        print("PASO AL ATAQUE")
        self.attackedOne = attackedOne
        self.state = State.ATTACKING
        self.attackCD = self.cooldown
        self.frame = 0
        self.image = self.sprites[self.frames[self.attackFrames[self.frame]][self.dirOffset[self.dir]]]

    # Pasa a morirse (chof)
    def changeToDying(self):
        self.state = State.DYING
        self.frame = 0
        self.image = self.sprites[self.frames[self.dieFrames[self.frame]][self.dirOffset[self.dir]]]

    # Pasa a muerto (chof del todo)
    def changeToDead(self):
        self.state = State.DEAD
        self.frame += 1
        self.image = self.sprites[self.frames[self.dieFrames[self.frame]]]

    def changeToOreTransporting(self):
        pass
    
    # Pasa de frame en los frames quietos, no cambia nada puesto que esta quieto
    def updateStillImage(self):
        self.frame = (self.frame + 1) % len(self.stillFrames)
        self.image = self.sprites[self.frames[self.stillFrames[self.frame]][self.dirOffset[self.dir]]]
        
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
        return(r.x + r.w/2, r.y + r.h) #!!!

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getDrawPosition(self):
        return(self.x - self.image.get_width()/2,  self.y - self.image.get_height()/2)

    def getRect(self):
        rectAux = pg.Rect(self.x - self.xPadding, 
                self.y - self.yPadding, self.image.get_width() - self.wPadding, self.image.get_height()  - self.hPadding)
        return rectAux

    # Getter de la HP
    def getHp(self):
        return self.hp
    
    #Getter del player
    def getPlayer(self):
        return self.player

    def updateUnit(self):
        #OBTENEMOS LA TILE EN LA QUE SE ENCUENTRAN
        unitPos = self.getPosition()
        tileActual = self.mapa.getTile(unitPos[0], unitPos[1])
        #SI ESTA MOVIENDOSE HAY QUE CALCULAR COLISIONES Y CAMBIAR LAS TILES QUE OCUPAN
        if self.paths.__len__() > 0:

            #CON POSFIN DEL PATH ACTUAL Y EL PATH FINAL(OBJETIVO) CALCULO LAS TILES DE LA SIGUIENTE Y OBJETIVO
            path = self.paths[0]
            pathObj = self.paths[self.paths.__len__() - 1]
            tilePath = self.mapa.getTile(path.posFin[0],path.posFin[1])
            tileObj = self.mapa.getTile(pathObj.posFin[0],pathObj.posFin[1])

            #SI LA SIGUIENTE NO ESTA OCUPADA HAY QUE ACTUALIZAR LAS TILES
            if tilePath.type != UNIT or ((tilePath.id == self.id) and (tilePath.type == UNIT)):
                dirX = math.cos(path.angle)
                dirY = math.sin(path.angle)
                tileSiguiente = self.mapa.getTile(int(unitPos[0] + dirX*self.speed + 0.5), int(unitPos[1] + dirY*self.speed + 0.5))
                if tileActual != tileSiguiente :
                    if tileActual.type != OBSTACLE and tileActual.type != CRYSTAL:
                        self.mapa.setLibre(tileActual)
                        if tileSiguiente.type != OBSTACLE and tileSiguiente.type != CRYSTAL:
                            self.mapa.setVecina(tileSiguiente, self.id)
                            tileSiguiente.setOcupante(self)
                    tiles = self.mapa.getAllTileVecinas(tileActual)
                    for tile in tiles:
                        if tile.type != OBSTACLE:
                            self.mapa.setLibre(tile)
                            #print("SETEO LIBRE POR UNIDAD: ", tile.tileid)
                else:
                    if tileActual.type != OBSTACLE and tileActual.type != CRYSTAL:
                        self.mapa.setVecina(tileActual, self.id)
                        tileActual.setOcupante(self)
            #LA SIGUIENTE TILE ESTA OCUPADA HAY QUE TRATAR COLISIONES
            else:
                if tilePath.tileid != tileObj.tileid:
                    if tilePath.ocupante.paths.__len__() == 0: # ME bloquea y ademas no se mueve
                        print("Me bloque y no se mueve el tio")
                        path = calcPath(tileActual,tileObj, self.mapa)
                        posFin = (tileObj.centerx, tileObj.centery)
                        self.paths = path
                    else: #Es majo y se va a mover
                            bestTile = self.mapa.getTileVecinaCercana(tileObj,tileActual)
                            #NO TIENE A DONDE IR
                            if bestTile.tileid == -1:
                                self.paths = []
                            else:
                                if bestTile.heur(tileObj) > tileActual.heur(tileObj):
                                    print("Me tengo que replegar por lo que mejor recalculo")
                                    path = calcPath(tileActual,tileObj, self.mapa)
                                    posFin = (tileObj.centerx, tileObj.centery)
                                    self.paths = path
                                else: #HACEMOS EL CAMBIO A LOS PATHS
                                    self.paths.pop(0) #quitamos el path a la ocupada
                                    #CAMINO A LA MEJOR TILE
                                    posFin = (bestTile.centerx, bestTile.centery)
                                    posIni = self.getPosition()
                                    path1 = Path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]),
                                            int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)

                                    self.paths.insert(0, path1)

                                    #CAMINO A LA TILE DESOCUPADA
                                    posIni = posFin
                                    posFin = (tilePath.centerx, tilePath.centery)
                                    path1 = Path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)
                                    self.paths.insert(1, path1)
                else: #La siguiente es mi objetivo
                    self.resolverObjetivoOcupado()
        else:
            self.mapa.setVecina(tileActual, self.id)
            tileActual.setOcupante(self)

    def resolverObjetivoOcupado(self):
        print(self.state)
        if self.state == State.MOVING:
            self.paths = []
        elif self.state == State.MOVING_TO_MINING:
            tilesCristal = self.tilesCristal()
            if tilesCristal.__len__() == 0: # Me he quedado sin sitio
                self.changeToStill()
            else:
                posicionActual = self.getPosition()
                tileActual = self.mapa.getTile(posicionActual[0], posicionActual[1])
                tileObj = tilesCristal[0]
                for tile in tilesCristal:
                    if tile.heur(tileActual) < tileObj.heur(tileActual):
                        tileObj = tile
                self.paths = calcPath(tileActual, tileObj, self.mapa)
        elif self.state == State.ORE_TRANSPORTING:
            tilesCasa = self.tilesCasa()
            if tilesCasa.__len__() == 0: # Me he quedado sin sitio
                self.paths = []
            else:
                posicionActual = self.getPosition()
                tileActual = self.mapa.getTile(posicionActual[0], posicionActual[1])
                tileObj = tilesCasa[0]
                for tile in tilesCasa:
                    if tile.heur(tileActual) < tileObj.heur(tileActual):
                        tileObj = tile
                self.paths = calcPath(tileActual, tileObj, self.mapa)

    def tilesCasa(self):
        tilesCasa = []
        rect = self.player.base.getRect()
        x = self.mapa.getTile(rect.x, rect.y).centerx
        finx = x + rect.w
        y = self.mapa.getTile(rect.x, rect.y).centery
        finy = y + rect.h
        while x <= finx:
            tileUp = self.mapa.getTile(x,y - 40)
            tileDown = self.mapa.getTile(x,finy + 40)
            #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
            if tileUp.type == 0:
                tilesCasa.append(tileUp)
            if tileDown.type == 0:
                tilesCasa.append(tileDown)
            x += 40
        while y <= finy:
            tileUp = self.mapa.getTile(x - 40,y)
            tileDown = self.mapa.getTile(finx + 40,y)
            #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
            if tileUp.type == 0:
                tilesCasa.append(tileUp)
            if tileDown.type == 0:
                tilesCasa.append(tileDown)
            y += 40
        return tilesCasa