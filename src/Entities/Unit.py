import pygame as pg
import math
from .Entity import *
from ..Utils import *
from ..Command import *

# Representa a una unidad movil de cualquiera de las razas
class Unit(Entity):
    def __init__(self, hp, xIni, yIni, mineral_cost, generation_time, speed, framesToRefresh, 
                    sprites, face, frame, padding, id, player, minePower, timeToMine, inversibleFrames,
                        frames, dirOffset, attackFrames, stillFrames, moveFrames, dieFrames,  xPadding, yPadding, wPadding, hPadding, attackInfo):
        Entity.__init__(self, hp, xIni, yIni, mineral_cost, generation_time, id, player)
        # Relativo al movimiento de la unidad
        self.paths = []
        self.speed = speed
        self.angle = 0

        # Relativo a estado
        self.state = State.STILL
        self.clicked = False
        self.face = face
        self.frame = frame
        self.count = 0
        self.rectOffY = padding
        self.order = {'order': 0}
        self.attackedOne = None
        
        # Relativo a los frames
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

        # Info minado
        self.minePower = minePower
        self.timeToMine = timeToMine

        # Info ataque
        self.damage = attackInfo[DAMAGE_IND]
        self.cooldown = attackInfo[COOLDOWN_IND]
        self.range = attackInfo[RANGE_IND]
        self.attackedOne = None

    ##########
    # ORDERS #
    ##########

    # Indica a la unidad que se mueva a la tile especificada, si se encuentra un
    # obstaculo de camino lo esquivara y si la tile objetivo esta ocupada se detiene
    # lo mas cerca posible de esta
    def move(self, objectiveTile):
        self.changeToMoving(objectiveTile)

    # Indica a la unidad que ataque al objetivo seleccionado, si se encuentra un
    # obstaculo de camino lo esquivara y si el objetivo se desplaza este le seguira
    def attack(self, objective):
        self.changeToAttacking(objective)

    # Indica a la unidad que recolecte mineral o gas del objetivo, si se encuentra
    # un obstaculo de camino lo esquivara. Recolecta desde la tile libre mas cercana
    def mine(self, resource):
        pos = resource.getPosition()
        tile = self.playerMapa.getTile(pos[0], pos[1])
        tiles = self.playerMapa.getEntityTilesVecinas(tile)
        if len(tiles) > 0:
            ownTile = self.getTile()
            bestTile = tiles[0]
            for tile in tiles:
                if tile.heur(ownTile) < bestTile.heur(ownTile):
                    bestTile = tile
            self.move(self, bestTile)

    # Pinta la unidad C:
    def draw(self, screen, camera):
        if self.state != State.DEAD:
            r = self.getRect()
            if DEBBUG:
                pg.draw.rect(screen, BLACK, pygame.Rect(self.x - camera.x, r.y  - camera.y, r.w, r.h), 1)
            drawPos = self.getDrawPosition()
            if self.clicked:
                pg.draw.ellipse(screen, GREEN, [r.x - camera.x, r.y + (0.7*r.h)- camera.y,r.w , 0.3*r.h], 2)
            #screen.blit(unit.image, [r.x - camera.x, r.y - camera.y])
            screen.blit(self.image, [drawPos[0] - camera.x, drawPos[1] - camera.y])
            if self.clicked:
                hp = pygame.transform.chop(pg.transform.scale(HP, (50, 8)), ((self.hp / self.maxHp) * 50, 0, 50, 0))
                screen.blit(hp, [self.x - camera.x - hp.get_rect().w / 2, self.y + r.h / 2 - camera.y])

    ###########
    # UPDATES #
    ###########

    # Aplica un frame a la unidad en funcion de su estado
    def update(self):
        if self.state == State.STILL: # Esta quieto
            self.updateStill()
        elif self.state == State.MOVING: # Esta moviendose
            self.updateUnit()
            self.updateMoving()
        elif self.state == State.ATTACKING: # Esta atacando
            self.updateAttacking()
        elif self.state == State.MINING: # Esta minando
            self.updateUnit()
            self.updateMining()
        elif self.state == State.ORE_TRANSPORTING: # Esta transportando mineral
            self.updateUnit()
            self.updateOreTransporting()
        elif self.state == State.GAS_TRANSPORTING: # Esta transportando gas
            self.updateUnit()
            self.updateGasTransporting()
        elif self.state == State.DYING: # Esta muriendose
            self.updateDying()
        elif self.state == State.DEAD: # Esta muerta
            self.updateDead()
    
    # Aplica un frame a la unidad que esta quieta
    def updateStill(self):
        # Marca como ocupada la propia tile
        self.updateOwnSpace()
        # Actualiza la animacion
        self.updateStillImage()
    
    # Aplica un frame a la unidad que esta moviendose
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


    # Aplica un frame a la unidad que esta atacando
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

    # Aplica un frame a la unidad que esta minando
    # El minado es especifico de worker por lo que lo implementa worker
    def updateMining(self):
        pass

    # Aplica un frame a la unidad que esta llevando mineral
    # El minado es especifico de worker por lo que lo implementa worker
    def updateOreTransporting(self):
        pass

    # Aplica un frame a la unidad que esta llevando gas
    # El recolectar gas es especifico de worker por lo que lo implementa worker
    def updateGasTransporting(self):
        pass

    # Aplica un frame a la unidad muriendo
    def updateDying(self):
        self.updateOwnSpace()
        self.count += 1
        if self.count >= self.framesToRefresh:
            self.count = 0
            if self.frame < (len(self.dieFrames) - 1):
                self.updateDyingImage()
            else:
                self.changeToDead()

    # Aplica un frame a la unidad muerta, deberia eliminarse
    def updateDead(self):
        pass

    # Refleja en el mapa el espacio reservado por la propia unidad para este frame
    def updateOwnSpace(self):
        unitPos = self.getPosition()
        tileActual = self.playerMapa.getTile(unitPos[0], unitPos[1])
        self.playerMapa.setVecina(tileActual, self.id)
        tileActual.setOcupante(self)
    
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
       
    # Pasa de frame en una animacion de muerte
    def updateDyingImage(self):
        self.frame = (self.frame + 1)
        self.image = self.sprites[self.frames[self.dieFrames[self.frame]][self.dirOffset[self.dir]]]

    # esto debe morir, pero esta en ello
    def updateUnit(self):
        #SI ESTA MOVIENDOSE HAY QUE CALCULAR COLISIONES Y CAMBIAR LAS TILES QUE OCUPAN
        if self.paths.__len__() > 0:
            unitPos = self.getPosition()
            tileActual = self.playerMapa.getTile(unitPos[0], unitPos[1])
            #CON POSFIN DEL PATH ACTUAL Y EL PATH FINAL(OBJETIVO) CALCULO LAS TILES DE LA SIGUIENTE Y OBJETIVO
            path = self.paths[0]
            pathObj = self.paths[self.paths.__len__() - 1]
            tilePath = self.playerMapa.getTile(path.posFin[0],path.posFin[1])
            tileObj = self.playerMapa.getTile(pathObj.posFin[0],pathObj.posFin[1])

            #SI LA SIGUIENTE NO ESTA OCUPADA HAY QUE ACTUALIZAR LAS TILES
            if tilePath.type != UNIT or ((tilePath.id == self.id) and (tilePath.type == UNIT)):
                dirX = math.cos(path.angle)
                dirY = math.sin(path.angle)
                tileSiguiente = self.playerMapa.getTile(int(unitPos[0] + dirX*self.speed + 0.5), int(unitPos[1] + dirY*self.speed + 0.5))
                if tileActual != tileSiguiente :
                    if tileActual.type != OBSTACLE and tileActual.type != RESOURCE:
                        self.playerMapa.setLibre(tileActual)
                        if tileSiguiente.type != OBSTACLE and tileSiguiente.type != RESOURCE:
                            self.playerMapa.setVecina(tileSiguiente, self.id)
                            tileSiguiente.setOcupante(self)
                    tiles = self.playerMapa.getAllTileVecinas(tileActual)
                    for tile in tiles:
                        if tile.type != OBSTACLE:
                            self.playerMapa.setLibre(tile)
                            #print("SETEO LIBRE POR UNIDAD: ", tile.tileid)
                else:
                    if tileActual.type != OBSTACLE and tileActual.type != RESOURCE:
                        self.playerMapa.setVecina(tileActual, self.id)
                        tileActual.setOcupante(self)
            #LA SIGUIENTE TILE ESTA OCUPADA HAY QUE TRATAR COLISIONES
            else:
                if tilePath.tileid != tileObj.tileid:
                    if tilePath.ocupante.paths.__len__() == 0: # ME bloquea y ademas no se mueve
                        print("Me bloque y no se mueve el tio")
                        path = calcPath(tileActual,tileObj, self.playerMapa)
                        posFin = (tileObj.centerx, tileObj.centery)
                        self.paths = path
                    else: #Es majo y se va a mover
                            bestTile = self.playerMapa.getTileVecinaCercana(tileObj,tileActual)
                            #NO TIENE A DONDE IR
                            if bestTile.tileid == -1:
                                self.paths = []
                            else:
                                if bestTile.heur(tileObj) > tileActual.heur(tileObj):
                                    print("Me tengo que replegar por lo que mejor recalculo")
                                    path = calcPath(tileActual,tileObj, self.playerMapa)
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
            unitPos = self.getPosition()
            tileActual = self.playerMapa.getTile(unitPos[0], unitPos[1])
            self.playerMapa.setVecina(tileActual, self.id)
            tileActual.setOcupante(self)

    ################
    # TRANSICIONES #
    ################

    # Pasa a estado quieto
    def changeToStill(self):
        self.state = State.STILL
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.stillFrames[self.frame]][self.dirOffset[self.dir]]]
        #WHAT IS THIS?:
        #unitPos = self.getPosition()
        #tileActual = self.playerMapaa.getTile(unitPos[0], unitPos[1])
        #tiles = self.playerMapaa.getAllTileVecinas(tileActual)
        #for tile in tiles:
        #    if tile.type != OBSTACLE:
        #        self.playerMapaa.setLibre(tile)

    # Pasa a estado moverse
    def changeToMoving(self, objectiveTile):
        self.paths = calcPath(self.getTile(), objectiveTile, self.playerMapa)
        if len(self.paths) > 0:
            self.state = State.MOVING
            actualPath = self.paths[len(self.paths) - 1]
            if actualPath.angle < 0:
                self.angle = -actualPath.angle
            else:
                self.angle = 2 * math.pi - actualPath.angle
            self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
            self.frame = 0
            self.count = 0
            self.image = self.sprites[self.frames[self.moveFrames[self.frame]][self.dirOffset[self.dir]]]
        
    # Pasa al ataque HYAAAA!! >:c
    def changeToAttacking(self, attackedOne):
        self.state = State.ATTACKING
        self.attackedOne = attackedOne
        self.attackCD = self.cooldown
        self.frame = 0
        self.count = 0

    # Pasa a recolectar mineral o gas
    def changeToMining(self):
        pass
    
    # Pasa a transportar mineral
    def changeToOreTransporting(self):
        pass

    # Pasa a transportar gas
    def changeToGasTransporting(self):
        pass

    # Pasa a morirse (chof)
    def changeToDying(self):
        self.hp = 0
        self.state = State.DYING
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.dieFrames[self.frame]][self.dirOffset[self.dir]]]

    # Pasa a estar muerto del todo (puf, a lo Thanos)
    def changeToDead(self):
        self.state = State.DEAD
        self.playerMapa.setLibre(self.getTile())
        self.clicked = False

    ##############
    # AUXILIARES #
    ##############

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

    # Para inflingir un ataque a una unidad
    def makeAnAttack(self):
        hpLeft = self.attackedOne.beingAttacked(self.damage, self)
        if hpLeft < 0:
            self.changeToStill()

    # Para reflejar sobre una unidad que recibe un ataque
    def beingAttacked(self, damage, attacker):
        if self.hp < damage:
            self.hp = 0
            self.changeToDying()
        else:
            self.hp -= damage
        if self.state == State.STILL: # Cambiar a atacar si no esta haciendo nada
            self.changeToAttack(attacker)
        return self.hp
    
    # Para crear los sprites invertidos, los guarda en el mismo sitio que se indica
    def mirrorTheChosen(self):
        for i in range(self.inversibleFrames):
            for j in range(9, 16):
                self.sprites[self.frames[i][self.dirOffset[j]]] = pg.transform.flip(
                        self.sprites[self.frames[i][self.dirOffset[j]]], True, False)

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
                tileActual = self.playerMapa.getTile(posicionActual[0], posicionActual[1])
                tileObj = tilesCristal[0]
                for tile in tilesCristal:
                    if tile.heur(tileActual) < tileObj.heur(tileActual):
                        tileObj = tile
                self.paths = calcPath(tileActual, tileObj, self.playerMapa)
        elif self.state == State.ORE_TRANSPORTING:
            tilesCasa = self.tilesCasa()
            if tilesCasa.__len__() == 0: # Me he quedado sin sitio
                self.paths = []
            else:
                posicionActual = self.getPosition()
                tileActual = self.playerMapa.getTile(posicionActual[0], posicionActual[1])
                tileObj = tilesCasa[0]
                for tile in tilesCasa:
                    if tile.heur(tileActual) < tileObj.heur(tileActual):
                        tileObj = tile
                self.paths = calcPath(tileActual, tileObj, self.playerMapa)

    def tilesCasa(self):
        tilesCasa = []
        rect = self.player.base.getRect()
        x = self.playerMapa.getTile(rect.x, rect.y).centerx
        finx = x + rect.w
        y = self.playerMapa.getTile(rect.x, rect.y).centery
        finy = y + rect.h
        while x <= finx:
            tileUp = self.playerMapa.getTile(x,y - 40)
            tileDown = self.playerMapa.getTile(x,finy + 40)
            #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
            if tileUp.type == 0:
                tilesCasa.append(tileUp)
            if tileDown.type == 0:
                tilesCasa.append(tileDown)
            x += 40
        while y <= finy:
            tileUp = self.playerMapa.getTile(x - 40,y)
            tileDown = self.playerMapa.getTile(finx + 40,y)
            #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
            if tileUp.type == 0:
                tilesCasa.append(tileUp)
            if tileDown.type == 0:
                tilesCasa.append(tileDown)
            y += 40
        return tilesCasa
    
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
        
    #####################
    # GETTERS Y SETTERS #
    #####################

    # Es leer el valor del booleano de antes, se le suele llamar get
    def getClicked(self):
        return self.clicked

    def getPosition(self):
        r = self.getRect()
        return (r.x + r.w/2, r.y + r.h) #!!!

    def getTile(self):
        return self.playerMapa.getTile(self.x, self.y)

    # Getter de la coordenada X en valores reales
    def getX(self):
        return self.x

    # Getter de la coordenada Y en valores reales
    def getY(self):
        return self.y

    def getDrawPosition(self):
        return (self.x - self.image.get_width()/2,  self.y - self.image.get_height()/2)

    def getRect(self):
        rectAux = pg.Rect(self.x - self.xPadding, self.y - self.yPadding, 
                self.image.get_width() - self.wPadding, self.image.get_height()  - self.hPadding)
        return rectAux

    # Getter de la HP de la unidad
    def getHP(self):
        return self.hp
    
    # Getter del player que posee la unidad
    def getPlayer(self):
        return self.player

    def setOrder(self, order):
        self.order = order

    def setCristal(self, cristal):
        self.cristal = cristal

    def setCaminoABase(self, path):
        self.basePath = path

    # Es darle un valor a un booleano, nada mas y nada menos
    def setClicked(self, click):
        self.clicked = click
