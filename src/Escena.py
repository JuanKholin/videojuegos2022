import pygame as pg
import math
import json
from . import Player, Raton
from .Utils import *
from .Command import *
from .Entities import TerranBarracks
from .Entities.TerranRefinery import *
from .Entities import TerranWorker
from datetime import datetime


class Escena():
    def __init__(self, p1, p2, aI, mapa, camera, raton, interfaz, resources, nombre = "PartidaDefault"):
        self.p1 = p1
        self.p2 = p2
        self.aI = aI
        self.mapa = mapa
        self.camera = camera
        self.raton = raton
        self.interfaz = interfaz
        self.resources = resources
        self.nombre = nombre

    def setSelf(self, escena):
        self.p1 = escena.p1
        self.p2 = escena.p2
        self.aI = escena.aI
        self.mapa = escena.mapa
        self.camera = escena.camera
        self.raton = escena.raton
        self.interfaz = escena.interfaz
        self.resources = escena.resources
        self.nombre = escena.nombre

    def procesarEvent(self, event):
        #Conseguir el comando
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.MOUSEBUTTONUP:
            command = self.raton.processEvent(event, self.camera)
            print("ENABLE DE ESCENA: ", self.raton.enable, self.raton.id)
        else:
            command = self.p1.processEvent(event)
        if getGameState() == System_State.ONGAME:
            #ejecutar el comando
            if command.id == CommandId.UPGRADE_WORKER_MINING:
                #print(command.id)
                pass
            if not self.raton.building:
                if command.id == CommandId.GENERATE_UNIT:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.GENERATE_WORKER:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.GENERATE_SOLDIER:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.UPGRADE_SOLDIER_DAMAGE:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.UPGRADE_SOLDIER_ARMOR:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.UPGRADE_WORKER_MINING:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.BUILD_BARRACKS:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.BUILD_HATCHERY:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.BUILD_REFINERY:
                    self.p1.execute(command.id, [], None)
                elif command.id == CommandId.SAVE_GAME:
                    self.saveScene()
                elif command.id == CommandId.MOVE:
                    #path = [] ## !!!!
                    relative_mouse_pos = pg.mouse.get_pos()
                    real_mouse_pos = (relative_mouse_pos[0] + self.camera.x, relative_mouse_pos[1] + self.camera.y)
                    tileClicked = self.mapa.getTile(real_mouse_pos[0], real_mouse_pos[1])
                    print("TILE CLICKED: ", tileClicked.tileid, tileClicked.type)
                    orderForPlayer = []
                    for param in command.params:
                        self.processParam(param, tileClicked, tileClicked, orderForPlayer)
                    self.p1.execute(CommandId.ORDER, orderForPlayer, tileClicked)

                    #for param in commandp2.params:
                    #   self.processParam(param, tilesObj, tilesCasa, tileClicked, pathsForPlayer, orderForPlayer)
                    #self.p2.execute(CommandId.ORDENAR, orderForPlayer)

    def processParam(self, param, tileObj, tileClicked , orderForPlayer):
        tileIni = self.mapa.getTile(param[0], param[1])
        if tileObj.type != 0: #Esta ocupada
            tileObj = self.mapa.getTileCercana(tileIni, tileObj)
        path = calcPath(param, tileIni, tileObj, self.mapa)
        # COMPROBAR SI HA CLICKADO UN ORE
        order = {'order': CommandId.MOVE, 'angle': 0, 'path': path}
        if tileClicked.type == RESOURCE:
            print("CLICKO UN RECURSO")
            resource = tileClicked.getOcupante()
            order['order'] = CommandId.MINE
            order['resource'] = resource
        elif tileClicked.type == UNIT: # Ataque?
            print("CLICKO UNA UNIDAD")
            attacked = tileClicked.ocupante

            if attacked.getPlayer() != self.p1:
                order['order'] = CommandId.ATTACK
                order['attackedOne'] = attacked
        else:
            print("CLICKO UNA ESTRUCTURA")
            if tileClicked.type == STRUCTURE and tileClicked.ocupante.player != self.p1:
                order['order'] = CommandId.ATTACK
                order['attackedOne'] = tileClicked.ocupante
            else:
                rectClicked = Raton.createRect(tileClicked.centerx, tileClicked.centery, tileClicked.centerx + 1, tileClicked.centery + 1)
                for struct in self.p1.structures:
                    if Raton.collideRect(struct.getRect(), rectClicked):
                        order = struct.getOrder()
                        order = {'order': order}
        orderForPlayer.append(order)

    def checkPressedButtons(self):
        key = pg.key.get_pressed()
        if key[self.p1.commandMap[CommandId.MOVE_CAMERA_UP]]:
            self.camera.moverArriba()
        if key[self.p1.commandMap[CommandId.MOVE_CAMERA_DOWN]]:
            self.camera.moverAbajo(self.mapa.h - 160)
        if key[self.p1.commandMap[CommandId.MOVE_CAMERA_LEFT]]:
            self.camera.moverIzquierda()
        if key[self.p1.commandMap[CommandId.MOVE_CAMERA_RIGHT]]:
            self.camera.moverDerecha(self.mapa.w)

    def checkUnHoldButton(self, key):
        if self.p1.commandMap[CommandId.ROTATE] == key:
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
        self.mapa.updateNiebla(self.camera, self.p1.getEntitesLocation(self.camera))
        self.interfaz.update(self, self.raton, self.camera)
        #self.raton.update(self.camera)
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
                        self.mapa.setType(tileActual, STRUCTURE)
                        #print("SETEO VECINA POR ESTRUCTURA: ", tileActual.tileid)
        structure.setTilesOcupados()

    def updateResource(self, res):
        rect = res.getRect()
        x = rect.x
        finx = x + rect.w
        y = rect.y + 1
        finy = y + rect.h
        if(res.capacity <= 0 and res.getType() == RESOURCE):
            while x <= finx:
                while y <= finy:
                    self.mapa.setLibre(self.mapa.getTile(x,y))
                    y = y + self.mapa.th
                y = rect.y + 1
                x = x + self.mapa.tw
            self.resources.remove(res)
            del res
        else:
            if res.enable:
                while x <= finx:
                    while y <= finy:
                        self.mapa.setType(self.mapa.getTile(x,y), res.getType())
                        self.mapa.getTile(x,y).setOcupante(res)
                        y = y + self.mapa.th
                    y = rect.y + 1
                    x = x + self.mapa.tw

    def draw(self, screen):
        #importa el orden porfavor
        self.mapa.drawMap(screen, self.camera)

        for res in self.resources:
            res.draw(screen, self.camera)

        self.p1.draw(screen, self.camera)
        self.p2.draw(screen, self.camera)
        self.mapa.drawNiebla(screen, self.camera)
        self.raton.drawBuildStructure(screen, self.camera)
        self.interfaz.draw(screen, self.camera)

    def getTerranBarrack(self):
        return TerranBarracks(0, 0, None, self.mapa, True)

    def getHatchery(self):
        return Hatchery(0, 0, None, self.mapa, False)

    def getTerranRefinery(self):
        return TerranRefinery(0, 0, None, self.mapa, True)

    def toDictionary(self):
        return{
            "nombre": self.nombre,
            "p1": self.p1.toDictionary(self.mapa),
            "p2": self.p2.toDictionary(self.mapa),
            "mapa": self.mapa.toDictionary(),
            "camera": self.camera.toDictionary(),
            "resources": [r.toDictionary() for r in self.resources],
        }

    def saveScene(self):
        print(self.toDictionary())
        string = json.dumps(self.toDictionary(), indent = 2)

        textFile = open("games/" + self.nombre + ".json", "w")
        textFile.write(string)
        textFile.close()

    '''def loadScene(self):
        textFile = open("save_file.json", "r")
        data = json.load(textFile)
        self.mapa = loadMap(data["mapa"])
        self.p1 = loadPlayer(data["p1"], self.mapa, True)
        self.p2 = loadPlayer(data["p2"], self.mapa, False)
        self.camera = loadCamera(data["camera"])
        self.resources = loadResources(data["resources"])
        self.setBasePlayer1(self.p1.structures[0])
    '''
