import pygame as pg
import math
import json
from . import Player, Raton
from .Utils import *
from .Command import *
from .Entities import TerranBarracks, ZergBuilder
from .Loader import *
from datetime import datetime


class Escena():
    def __init__(self, p1, p2, aI, mapa, camera, raton, interfaz, resources):
        self.p1 = p1
        self.p2 = p2
        self.aI = aI
        self.mapa = mapa
        self.camera = camera
        self.raton = raton
        self.interfaz = interfaz
        self.resources = resources

    def procesarEvent(self, event):
        #Conseguir el comando
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
            command = self.raton.processEvent(event, self.camera.x, self.camera.y)
        else:
            command = self.p1.processEvent(event)
        if getGameState() == System_State.ONGAME:
            #ejecutar el comando
            if not self.raton.building:
                if command.id == CommandId.GENERAR_UNIDAD:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.GENERATE_WORKER:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.GENERATE_SOLDIER:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.BUILD_BARRACKS and self.p1.resources >= TERRAN_BARRACK_MINERAL_COST:
                    self.raton.building = True
                    self.raton.buildStructure = self.getTerranBarrack()
                elif command.id == CommandId.BUILD_ZERG_BUILDER and self.p1.resources >= TERRAN_BARRACK_MINERAL_COST:
                    self.raton.building = True
                    self.raton.buildStructure = self.getZergBuilder()
                elif command.id == CommandId.GUARDAR_PARTIDA:
                    self.saveScene()
                elif command.id == CommandId.MOVER:
                    #path = [] ## !!!!
                    relative_mouse_pos = pg.mouse.get_pos()
                    real_mouse_pos = (relative_mouse_pos[0] + self.camera.x, relative_mouse_pos[1] + self.camera.y)
                    tileClicked = self.mapa.getTile(real_mouse_pos[0], real_mouse_pos[1])
                    print("TILE CLICKED: ", tileClicked.tileid)
                    orderForPlayer = []
                    for param in command.params:
                        self.processParam(param, tileClicked, tileClicked, orderForPlayer)
                    self.p1.execute(CommandId.ORDENAR, orderForPlayer, tileClicked)

                    #for param in commandp2.params:
                    #   self.processParam(param, tilesObj, tilesCasa, tileClicked, pathsForPlayer, orderForPlayer)
                    #self.p2.execute(CommandId.ORDENAR, orderForPlayer)
                
    def processParam(self, param, tileObj, tileClicked , orderForPlayer):
        tileIni = self.mapa.getTile(param[0], param[1])
        if tileObj.type != 0: #Esta ocupada
            tileObj = self.mapa.getTileCercana(tileIni, tileObj)
        path = calcPath(tileIni, tileObj, self.mapa)
        # COMPROBAR SI HA CLICKADO UN ORE
        order = {'order': CommandId.MOVER, 'angle': 0, 'path': path}
        if tileClicked.type == RESOURCE:
            Cristal = tileClicked.ocupante
            order['order'] = CommandId.MINAR
            order['cristal'] = Cristal
        elif tileClicked.type == UNIT: # Ataque?
            attacked = tileClicked.ocupante
            if attacked.getPlayer() != self.p1:
                order['order'] = CommandId.ATTACK
                order['attackedOne'] = attacked
        else:
            rectClicked = Raton.createRect(tileClicked.centerx, tileClicked.centery, tileClicked.centerx + 1, tileClicked.centery + 1)
            for struct in self.p1.structures:
                if Raton.collideRect(struct.getRect(), rectClicked):
                    order = struct.getOrder()
                    order = {'order': order,'path': path}
        orderForPlayer.append(order)

    def checkPressedButtons(self):
        key = pg.key.get_pressed()
        if key[self.p1.commandMap[CommandId.MOVER_CAMARA_ARRIBA]]:
            self.camera.moverArriba()
        if key[self.p1.commandMap[CommandId.MOVER_CAMARA_ABAJO]]:
            self.camera.moverAbajo(self.mapa.h)
        if key[self.p1.commandMap[CommandId.MOVER_CAMARA_IZQUIERDA]]:
            self.camera.moverIzquierda()
        if key[self.p1.commandMap[CommandId.MOVER_CAMARA_DERECHA]]:
            self.camera.moverDerecha(self.mapa.w)

    def checkUnHoldButton(self, key):
        if self.p1.commandMap[CommandId.ROTAR] == key:
            for unit in self.p1.unitsSelected:
                #print(unit.getRect().x - unit.getRect().w,unit.getRect().y - unit.getRect().h)
                unit.dir = (unit.dir + 1)%16

    def update(self):
        for structure in self.p1.structures + self.p2.structures:
            self.updateStructure(structure)
        for res in self.resources:
            self.updateResource(res)

        self.p1.update()
        self.p2.update()
        self.interfaz.update()
        self.raton.update(self.camera)
        self.aI.make_commands()


    def updateStructure(self, structure):
        unitPos = structure.getPosition()
        tileActual = self.mapa.getTile(unitPos[0], unitPos[1])
        if structure.paths.__len__() > 0:
            path = structure.paths[0]
            pathObj = structure.paths[structure.paths.__len__() - 1]
            tilePath = self.mapa.getTile(path.posFin[0],path.posFin[1])
            ##print("Tilepath es: ", tilePath.centerx, tilePath.centery)
            if tilePath.type != UNIT or (tilePath.id == structure.id and tilePath.type == UNIT):
                dirX = math.cos(path.angle)
                dirY = math.sin(path.angle)
                tileSiguiente = self.mapa.getTile(unitPos[0] + dirX*structure.speed, unitPos[1] + dirY*structure.speed)
                if tileActual != tileSiguiente :
                    if tileActual.type != OBSTACLE:
                        self.mapa.setLibre(tileActual)
                        if tileSiguiente.type != 1:
                            self.mapa.setVecina(tileSiguiente, structure.id)
                            #print("SETEO VECINA POR ESTRUCTURA: ", tileSiguiente.tileid)
                else:
                    if tileActual.type != 1:
                        self.mapa.setVecina(tileActual, structure.id)
                        #print("SETEO VECINA POR ESTRUCTURA: ", tileActual.tileid)
        structure.setTilesOcupados()

    def updateResource(self, res):
        rect = res.getRect()
        x = rect.x
        finx = x + rect.w
        y = rect.y + 1
        finy = y + rect.h
        if(res.capacidad < 0):
            while x <= finx:
                while y <= finy:
                    self.mapa.setLibre(self.mapa.getTile(x,y))
                    y = y + self.mapa.th
                y = rect.y + 1
                x = x + self.mapa.tw
            self.resources.remove(res)
            del res
        else:
            while x <= finx:
                    while y <= finy:
                        self.mapa.setRecurso(self.mapa.getTile(x,y))
                        self.mapa.getTile(x,y).setOcupante(res)
                        y = y + self.mapa.th
                    y = rect.y + 1
                    x = x + self.mapa.tw

    def draw(self, screen):
        #importa el orden porfavor
        self.mapa.drawMap(screen, self.camera)
        
        for res in self.resources:
            r = res.getRect()
            pg.draw.rect(screen, BLACK, pg.Rect(r.x - self.camera.x, r.y  - self.camera.y, r.w, r.h),1)
            if (r.x + r.w >= self.camera.x and r.x <= self.camera.x + self.camera.w and
            r.y + r.h >= self.camera.y and r.y <= self.camera.y + self.camera.h):
                drawPos = res.getDrawPosition()
                if res.clicked:
                    pg.draw.ellipse(screen, GREEN, [r.x - self.camera.x, r.y + (0.7*r.h)- self.camera.y,r.w , 0.3*r.h], 2)
                #screen.blit(unit.image, [r.x - self.camera.x, r.y - self.camera.y])
                screen.blit(res.image, [drawPos[0] - self.camera.x, drawPos[1] - self.camera.y])
                
        self.p1.draw(screen, self.camera)
        self.p2.draw(screen, self.camera)
        self.raton.drawBuildStructure(screen, self.camera)
        self.interfaz.draw(screen)
        
    def getTerranBarrack(self):
        return TerranBarracks(0, 0, None, self.mapa, True, 5)

    def getZergBuilder(self):
        return ZergBuilder(0, 0, None, self.mapa, False, 8)

    def toDictionary(self):
        return{
            "p1": self.p1.toDictionary(self.mapa),
            "p2": self.p2.toDictionary(self.mapa),
            "mapa": self.mapa.toDictionary(),
            "camera": self.camera.toDictionary(),
            "resources": [r.toDictionary(self.mapa) for r in self.resources],
        }

    def saveScene(self):
        string = json.dumps(self.toDictionary(), indent = 2)

        textFile = open("save_file.json", "w")
        textFile.write(string)
        textFile.close()

    def loadScene(self):
        textFile = open("save_file.json", "r")
        data = json.load(textFile)
        self.mapa = loadMap(data["mapa"])
        self.p1 = loadPlayer(data["p1"], self.mapa)
        self.p2 = loadPlayer(data["p2"], self.mapa)
        self.camera = loadCamera(data["camera"])
        self.resources = loadResources(data["resources"])
        self.setBasePlayer1(self.p1.structures[0])
