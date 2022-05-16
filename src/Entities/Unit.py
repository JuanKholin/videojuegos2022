import pygame as pg
import math
from .Entity import *
from ..Utils import *
from ..Command import *
from ..Lib import *
from ..Camera import *
from ..Music import *

# Representa a una unidad movil de cualquiera de las razas
class Unit(Entity):
    
    generateSound = soldierGenerateSound
    deadSound = soldierDeadSound
    attackSound = soldierAttackSound
    
    def __init__(self, hp, xIni, yIni, mineral_cost, generation_time, speed, framesToRefresh,
                    sprites, face, frame, padding, id, player, inversibleFrames,
                        frames, dirOffset, attackFrames, stillFrames, moveFrames, dieFrames,  xPadding, yPadding, wPadding, hPadding, attackInfo):
        Entity.__init__(self, hp, xIni, yIni, mineral_cost, generation_time, id, player)
        # Relativo al movimiento de la unidad
        self.paths = []
        self.speed = speed
        self.angle = 0
        self.dir = 8

        # Relativo a estado
        self.clicked = False
        self.face = face
        self.frame = frame
        self.count = 0
        self.rectOffY = padding
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

        # Info ataque
        self.damage = attackInfo[DAMAGE_IND]
        self.cooldown = attackInfo[COOLDOWN_IND]
        self.range = attackInfo[RANGE_IND]
        self.attackedOne = None

        self.occupiedTile = None

        self.esEstructura = False

        self.siendoAtacado = False

        self.runningAway = False
    
    def spawn(self, x, y):
        self.x = x * TILE_WIDTH + 20
        self.y = y * TILE_HEIGHT
        self.updateOwnSpace()
        self.changeToStill()

    ##########
    # ORDERS #
    ##########

    # Indica a la unidad que se mueva a la tile especificada, si se encuentra un
    # obstaculo de camino lo esquivara y si la tile objetivo esta ocupada se detiene
    # lo mas cerca posible de esta
    def move(self, objectiveTile):
        if self.state != UnitState.DYING and self.state != UnitState.DEAD:
            self.siendoAtacado = False
            if objectiveTile.type == OBSTACLE:
                objectiveTile = self.mapa.getTileCercana(self.getTile(), objectiveTile)
            elif objectiveTile.type != EMPTY and objectiveTile.type != UNIT:
                #print("AAAAAAAAAAAAAAAAAAAAAAAAA")
                tilesRound = self.mapa.getEntityTilesVecinas(objectiveTile, self.getTile())
                objectiveTile = tilesRound[0]
                for tile in tilesRound:
                    if tile.heur(self.getTile()) < objectiveTile.heur(self.getTile()):
                        objectiveTile = tile
            self.mapa.setLibre(self.occupiedTile)
            self.paths = calcPath(self.getPosition(), self.getTile(), objectiveTile, self.mapa)
            self.mapa.setVecina(self.occupiedTile, self.id)
            self.occupiedTile.setOcupante(self)
            if len(self.paths) > 0 and (self.state != UnitState.ORE_TRANSPORTING and self.state != UnitState.GAS_TRANSPORTING) :
                self.changeToMoving(self.paths)
            else:
                self.updateOwnSpace()
                self.changeToStill()

    # Indica a la unidad que ataque al objetivo seleccionado, si se encuentra un
    # obstaculo de camino lo esquivara y si el objetivo se desplaza este le seguira
    def attack(self, objective):
        if (self.attackedOne != objective) or (self.state != UnitState.ATTACKING) and self.state != UnitState.DYING and self.state != UnitState.DEAD:
            self.mapa.setLibre(self.occupiedTile)
            if objective.esEstructura == False:
                #print("Atacamos a una unidad")
                self.tileAAtacar = objective.getTile()
                self.paths = calcPath(self.getPosition(), self.getTile(), self.tileAAtacar, self.mapa)
            else:
                #print("Atacamos a una estructura")
                tilesAAtacar = self.mapa.getAttackRoundTiles(objective.getRect())
                self.tileAAtacar = tilesAAtacar[0]
                for tile in tilesAAtacar:
                    if tile.heur(self.getTile()) < self.tileAAtacar.heur(self.getTile()):
                        self.tileAAtacar = tile
                self.paths = calcPath(self.getPosition(), self.getTile(), self.tileAAtacar, self.mapa)
            #print("CAMINOS:" ,len(self.paths))
            self.changeToAttacking(objective)
            if len(self.paths) == 1:
                #LO MEJOR ES MOVERSE AL CENTRO DE LA TILE, SINO NO ATOMICO
                unitPos = self.getPosition()
                tilePos = (self.getTile().centerx,self.getTile().centery)
                path = Path(math.atan2(tilePos[1] - unitPos[1], tilePos[0] - unitPos[0]), int(math.hypot(tilePos[0] - unitPos[0], tilePos[1] - unitPos[1])),tilePos)
                self.paths = [path]
            elif len(self.paths) == 0:
                self.updateOwnSpace()
            else:
                self.changeObjectiveTile()

    # Indica a la unidad que se acerque lo mas posible a un recurso mineral
    def mine(self, resource):
        if self.state != UnitState.DYING and self.state != UnitState.DEAD:
            pos = resource.getPosition()
            tile = self.mapa.getTile(pos[0], pos[1])
            tiles = self.mapa.getEntityTilesVecinas(tile, self.getTile())
            if len(tiles) > 0:
                ownTile = self.getTile()
                bestTile = tiles[0]
                for tile in tiles:
                    if tile.heur(ownTile) < bestTile.heur(ownTile):
                        bestTile = tile
                self.move(bestTile)

    # Indica a la unidad que se acerque lo mas posible a un recurso gas
    def extract(self, resource):
        pos = resource.getPosition()
        tile = self.mapa.getTile(pos[0], pos[1])
        tiles = self.mapa.getEntityTilesVecinas(tile, self.getTile())
        if len(tiles) > 0:
            ownTile = self.getTile()
            bestTile = tiles[0]
            for tile in tiles:
                if tile.heur(ownTile) < bestTile.heur(ownTile):
                    bestTile = tile
            self.move(bestTile)

    # Pinta la unidad C:
    def draw(self, screen, camera):
        t = self.mapa.getTile(self.x, self.y)
        if not t.visible:
            return
        if self.state != UnitState.DEAD:
            r = self.getRect()
            if DEBBUG:
                pg.draw.rect(screen, BLACK, pygame.Rect(r.x - camera.x, r.y  - camera.y, r.w, r.h), 1)
            drawPos = self.getDrawPosition()
            if self.clicked:
                pg.draw.ellipse(screen, GREEN, [r.x - camera.x, r.y + (0.7*r.h)- camera.y,r.w , 0.3*r.h], 2)

            aux = pygame.mask.from_surface(self.image, 0)
            mask = aux.to_surface(setcolor=(1, 0, 0))
            mask.set_colorkey(BLACK)
            mask.set_alpha(150)
            screen.blit(mask, [drawPos[0] - camera.x - 5, drawPos[1] - camera.y - 5])
            #screen.blit(unit.image, [r.x - camera.x, r.y - camera.y])
            screen.blit(self.image, [drawPos[0] - camera.x, drawPos[1] - camera.y])
            if self.clicked or self.hp < self.maxHp:
                if self.player.isPlayer:
                    hp = pygame.transform.chop(pg.transform.scale(HP, (50, 8)), ((self.hp / self.maxHp) * 50, 0, 50, 0))
                    screen.blit(hp, [self.x - camera.x - hp.get_rect().w / 2, self.y + r.h / 2 - camera.y])
                else:
                    hp = pygame.transform.chop(pg.transform.scale(HP2, (50, 8)), ((self.hp / self.maxHp) * 50, 0, 50, 0))
                    screen.blit(hp, [self.x - camera.x - hp.get_rect().w / 2, self.y + r.h / 2 - camera.y])

    def drawInfo(self, screen, color):
        dic = self.toDictionary(self.mapa)
        muestra_texto(screen, str('monotypecorsiva'), dic['nombre'], color, 25, [GUI_INFO_X2, GUI_INFO_Y2])
        muestra_texto(screen, str('monotypecorsiva'), dic['funcion'], color, 20, [GUI_INFO_X2, GUI_INFO_Y2 + 50])

    ###########
    # UPDATES #
    ###########

    # Aplica un frame a la unidad en funcion de su estado
    def update(self):
        if self.state == UnitState.STILL: # Esta quieto
            self.updateStill()
        elif self.state == UnitState.MOVING: # Esta moviendose
            self.updateMoving()
        elif self.state == UnitState.ATTACKING: # Esta atacando
            self.updateAttacking()
        elif self.state == UnitState.MINING: # Esta minando
            self.updateMining()
        elif self.state == UnitState.EXTRACTING: # Esta extrayendo gas
            self.updateExtracting()
        elif self.state == UnitState.ORE_TRANSPORTING: # Esta transportando mineral
            self.updateOreTransporting()
        elif self.state == UnitState.GAS_TRANSPORTING: # Esta transportando gas
            self.updateGasTransporting()
        elif self.state == UnitState.DYING: # Esta muriendose
            self.updateDying()
        elif self.state == UnitState.DEAD: # Esta muerta
            self.updateDead()

    # Aplica un frame a la unidad que esta quieta
    def updateStill(self):
        # Marca como ocupada la propia tile
        #self.updateOwnSpace()
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
            #print("UPDATE MOVING")
            self.changeToStill()


    # Aplica un frame a la unidad que esta atacando
    def updateAttacking(self):
        if(self.id == 2):
            #print("ATACANDO")
            pass
        if self.attackedOne.getHP() > 0:
            '''tileActual = self.getTile()
            enemyTile = self.attackedOne.getTile()'''
            #print("Estoy en: ", tileActual.tileid, "y el enemigo en: ", enemyTile.tileid)
            #print(int(math.hypot(self.x - self.attackedOne.x, self.y - self.attackedOne.y)) )
            if len(self.paths) > 0:
                self.updateAttackingRoute()
            else:
                self.updateAttackInRange()
        else: # Se murio el objetivo, pasa a estar quieto
            self.attackedOne = None
            enemy = self.mapa.getNearbyRival(self.occupiedTile, self.player)
            #print(type(enemy))
            if enemy != None:
                #print("ataco a otro")
                self.attack(enemy)
            else:
                #print("no hay naide")
                self.changeToStill()

    # Aplica un frame a la unidad que esta minando
    # El minado es especifico de worker por lo que lo implementa worker
    def updateMining(self):
        pass

    # Aplica un frame a la unidad que esta minando
    # La extraccion de gas es especifico de worker por lo que lo implementa worker
    def updateExtracting(self):
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
        #self.updateOwnSpace()
        self.count += 1
        if frame(10) == 1:
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
        self.occupiedTile = self.mapa.getTile(unitPos[0], unitPos[1])
        self.mapa.setVecina(self.occupiedTile, self.id)
        self.occupiedTile.setOcupante(self)

    def updateAttackInRange(self):
        ownTile = self.getTile()
        if self.attackedOne.esEstructura == False:
            self.tileAAtacar = self.attackedOne.getTile()
            if self.tileAAtacar == None:
                enemy = self.mapa.getNearbyRival(self.occupiedTile, self.player)
                if enemy != None:
                    self.attack(enemy)
                else:
                    self.changeToStill()
        if int(math.hypot(ownTile.centerx - self.tileAAtacar.centerx, ownTile.centery- self.tileAAtacar.centery)) <= self.range:
            if len(self.paths) != 0:
                objectivePath = self.paths[0]
                nextTile = self.mapa.getTile(objectivePath.posFin[0], objectivePath.posFin[1])
                self.mapa.setLibre(nextTile)
                self.updateOwnSpace()
                self.paths = [] #Me quedo quieto y ataco
            if self.attackCD > 1: # Si hay CD
                self.attackCD -= 1 # Disminuye CD
            elif self.attackCD == 1: # Si acaba el CD empieza la animacion
                self.takeAim()
                self.attackCD -= 1
                self.frame = -1
                self.counter = 0
                self.updateAttackingImage()
            elif self.attackCD == 0:
                self.counter += 1
                if self.counter >= self.framesToRefresh:
                    self.counter = 0
                    self.updateAttackingImage()
                    if self.frame == 0:
                        if inCamera(self.getPosition()):
                            playSound(self.attackSound)
                        self.makeAnAttack()
                        self.attackCD = self.cooldown
        else:
            self.recalcAttackPaths()

    def updateAttackingRoute(self):
        if self.paths.__len__() != 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0: # Aun queda trecho
                self.updatePath(actualPath)
            else: # Se acaba este camino
                ownTile = self.getTile()
                if int(math.hypot(ownTile.centerx - self.tileAAtacar.centerx, ownTile.centery- self.tileAAtacar.centery)) <= self.range:
                    #print(type(self), "estoy en rango")
                    self.updateAttackInRange()
                else:
                    lastPath = self.paths[len(self.paths) - 1]
                    lastTile = self.mapa.getTile(lastPath.posFin[0], lastPath.posFin[1])
                    if lastTile != self.attackedOne.getTile():
                        self.recalcAttackPaths()
                    else:
                        self.finishPath()


            self.count += 1
            if self.count >= self.framesToRefresh:
                self.count = 0
                self.updateMovingImage()
        else:
            #print("UPDATE ARAAK ROUTE")
            self.changeToStill()

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

    ################
    # TRANSICIONES #
    ################

    # Pasa a estado quieto
    def changeToStill(self):
        #print("STILL", type(self))
        self.state = UnitState.STILL
        self.runningAway = False
        self.attackedOne = None
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.stillFrames[self.frame]][self.dirOffset[self.dir]]]

    # Pasa a estado moverse
    def changeToMoving(self, paths):
        #print("MOVING", self.x, self.y, paths.__len__())
        if self.state == UnitState.ATTACKING:
            self.runningAway = True
        self.state = UnitState.MOVING
        self.attackedOne = None
        self.changeObjectiveTile()

        actualPath = paths[0]

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
        #print("Pasa al ataque HYAAAA!! >:c")
        self.state = UnitState.ATTACKING
        self.runningAway = False

        if(len(self.paths) > 1):
            #print("changeToAttacking objetiveTile")
            self.changeObjectiveTile()
        if self.attackedOne != None:
            if self.attackedOne.esEstructura:
                self.attackedOne.lastAttacker = None
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
        print("DYING", self.x, self.y)
        self.state = UnitState.DYING
        self.attackedOne = None
        self.runningAway = False
        self.mapa.setLibre(self.getTile())
        if self.occupiedTile != None:
            self.mapa.setLibre(self.occupiedTile)
        self.hp = 0
        if self.clicked:
            self.player.removeUnit(self)
            self.clicked = False
        self.frame = 0
        self.count = 0
        self.image = self.sprites[self.frames[self.dieFrames[self.frame]][self.dirOffset[self.dir]]]
        if inCamera(self.getPosition()):
            playSound(self.deadSound)

    # Pasa a estar muerto del todo (puf, a lo Thanos)
    def changeToDead(self):
        #print("DEAD", self.x, self.y)
        self.state = UnitState.DEAD
        self.runningAway = False
        self.attackedOne = None
        self.player.units.remove(self)
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

    def takeAim(self):
        self.angle = math.atan2(self.attackedOne.y - self.y, self.attackedOne.x - self.x)
        if self.angle < 0:
            self.angle = -self.angle
        else:
            self.angle = 2 * math.pi - self.angle
        self.dir = int(4 - (self.angle * 8 / math.pi)) % 16

    # Para inflingir un ataque a una unidad
    def makeAnAttack(self):
        hpLeft = self.attackedOne.beingAttacked(self.damage + self.player.dañoUpgrade, self)
        if hpLeft <= 0:
            #print("Se queda sin vida")
            enemy = self.mapa.getNearbyRival(self.occupiedTile, self.player)
            if enemy != None:
                self.attack(enemy)
            else:
                self.changeToStill()

    # Para reflejar sobre una unidad que recibe un ataque
    def beingAttacked(self, damage, attacker):
        if self.hp <= (damage - self.player.armorUpgrade):
            self.attackedOne = None
            self.changeToDying()
        else:
            self.hp -= (damage - self.player.armorUpgrade)
            #if self.state != UnitState.ATTACKING and self.state != UnitState.STILL: # Cambiar a atacar si no esta haciendo nada ASI GUAY
            if self.state != UnitState.ATTACKING and self.state != UnitState.STILL:
                self.siendoAtacado = True
                self.atacante = attacker
            elif self.state == UnitState.STILL:
                print("AL <TAKE")
                self.attack(attacker)
        return self.hp

    # Para crear los sprites invertidos, los guarda en el mismo sitio que se indica
    def mirrorTheChosen(self):
        for i in range(self.inversibleFrames):
            for j in range(9, 16):
                self.sprites[self.frames[i][self.dirOffset[j]]] = pg.transform.flip(
                        self.sprites[self.frames[i][self.dirOffset[j]]], True, False)

    def resolverObjetivoOcupado(self):
        #print("RESOLVER OCUAPDO: ", self.state)
        if self.state == UnitState.MOVING:
            self.paths = []
        elif self.state == UnitState.MINING or self.state == UnitState.EXTRACTING:
            tilesResource = self.tilesResource(self.getTile())
            if tilesResource.__len__() == 0: # Me he quedado sin sitio
                self.changeToStill()
            else:
                posicionActual = self.getPosition()
                tileActual = self.mapa.getTile(posicionActual[0], posicionActual[1])
                tileObj = tilesResource[0]
                for tile in tilesResource:
                    if tile.heur(tileActual) < tileObj.heur(tileActual):
                        tileObj = tile
                self.mapa.setLibre(self.occupiedTile)
                self.paths = calcPathNoLimit(self.getPosition(), tileActual, tileObj, self.mapa)
                self.mapa.setVecina(self.occupiedTile, self.id)
                self.occupiedTile.setOcupante(self)
                if len(self.paths) != 0:
                    self.changeObjectiveTile()
        elif self.state == UnitState.ORE_TRANSPORTING or self.state == UnitState.GAS_TRANSPORTING:
            tilesCasa = self.tilesCasa(self.getTile())
            if tilesCasa.__len__() == 0: # Me he quedado sin sitio
                #print("Me he quedado sin sitio")
                self.paths = []
            else:
                posicionActual = self.getPosition()
                tileActual = self.mapa.getTile(posicionActual[0], posicionActual[1])
                tileObj = tilesCasa[0]
                for tile in tilesCasa:
                    if tile.heur(tileActual) < tileObj.heur(tileActual):
                        tileObj = tile
                self.mapa.setLibre(self.occupiedTile)
                self.paths = calcPathNoLimit(self.getPosition(), tileActual, tileObj, self.mapa)
                self.mapa.setVecina(self.occupiedTile, self.id)
                self.occupiedTile.setOcupante(self)
                if len(self.paths) != 0:
                    self.changeObjectiveTile()

    def tilesCasa(self, tileActual):
        rect = self.player.base.getRect()
        tile = self.mapa.getTile(rect.x, rect.y)
        tilesCasa = self.mapa.getEntityTilesVecinas(tile, tileActual)
        return tilesCasa

    def finishPath(self):
        self.paths.pop(0)
        if len(self.paths) == 0:
            if (self.siendoAtacado == True) and not self.runningAway:
                self.attack(self.atacante)
            else:
                self.changeToStill()
        else:
            actualPath = self.paths[0]
            if actualPath.angle < 0:
                self.angle = -actualPath.angle
            else:
                self.angle = 2 * math.pi - actualPath.angle

            self.dir = int(4 - (self.angle * 8 / math.pi)) % 16
            if (self.siendoAtacado == True) and not self.runningAway:
                self.attack(self.atacante)
                self.changeObjectiveTile()
            else:
                self.changeObjectiveTile()
            
        


    def recalcAttackPaths(self):
        self.mapa.setLibre(self.occupiedTile)
        if self.attackedOne.esEstructura == False:
            #print("Atacamos a una unidad")
            self.tileAAtacar = self.attackedOne.getTile()
            if self.tileAAtacar == None:
                enemy = self.mapa.getNearbyRival(self.occupiedTile, self.player)
                if enemy != None:
                    self.attack(enemy)
                else:
                    self.changeToStill()
            self.paths = calcPath(self.getPosition(), self.getTile(), self.tileAAtacar, self.mapa)
        else:
            #print("Atacamos a una estructura")
            tilesAAtacar = self.mapa.getAttackRoundTiles(self.attackedOne.getRect())
            self.tileAAtacar = tilesAAtacar[0]
            for tile in tilesAAtacar:
                if tile.heur(self.getTile()) < self.tileAAtacar.heur(self.getTile()):
                    self.tileAAtacar = tile
            self.paths = calcPath(self.getPosition(), self.getTile(), self.tileAAtacar, self.mapa)
        self.mapa.setVecina(self.occupiedTile, self.id)
        self.occupiedTile.setOcupante(self)
        if len(self.paths) > 0:
            self.changeObjectiveTile()
            ownTile = self.getTile()
            if int(math.hypot(ownTile.centerx - self.tileAAtacar.centerx, ownTile.centery- self.tileAAtacar.centery)) <= self.range:
                self.updateAttackInRange()
            else:
                #self.updatePath(self.paths[len(self.paths) - 1])
                self.updateMovingImage()

    # Indica a la IA si es soldado o worker
    def isSoldier(self):
        pass

    def changeObjectiveTile(self):
        actualPath = self.paths[0]
        objectiveTile = self.mapa.getTile(actualPath.posFin[0], actualPath.posFin[1])
        #print(objectiveTile.id, self.id)
        if objectiveTile.type == EMPTY or (objectiveTile.type == UNIT and objectiveTile.id == self.id):
            self.mapa.setVecina(objectiveTile, self.id)
            objectiveTile.setOcupante(self)
            self.mapa.setLibre(self.occupiedTile)
            self.occupiedTile = objectiveTile
        else:
            lastPath = self.paths[len(self.paths) - 1]
            lastTile = self.mapa.getTile(lastPath.posFin[0], lastPath.posFin[1])
            self.mapa.setLibre(self.occupiedTile)
            self.paths = calcPath(self.getPosition(), self.getTile(), lastTile, self.mapa)
            self.mapa.setVecina(self.occupiedTile, self.id)
            self.occupiedTile.setOcupante(self)
            if len(self.paths) > 1:
                self.changeObjectiveTile()
            else:
                self.resolverObjetivoOcupado()

    def isReadyToFight(self):
        return (self.state != UnitState.ATTACKING) and (self.hp > 0)

    #####################
    # GETTERS Y SETTERS #
    #####################

    # Es leer el valor del booleano de antes, se le suele llamar get
    def getClicked(self):
        return self.clicked

    def getPosition(self):
        r = self.getRect()
        return (r.x + r.w/2, r.y + r.h) #!!!

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

    def getDir(self):
        return self.dir

    def getRealDir(self):
        if (self.dir % 2) == 1:
            return (self.dir - 1) / 2
        return self.dir / 2

    def setCristal(self, cristal):
        self.cristal = cristal

    def setCaminoABase(self, path):
        self.basePath = path

    # Es darle un valor a un booleano, nada mas y nada menos
    def setClicked(self, click):
        self.clicked = click

    def toDictionary(self, map):
        x, y = map.getTileIndex(self.x, self.y)
        return {
            "x": x,
            "y": y,
            "hp": self.hp
        }
    def load(self, hp):
        self.hp = hp
