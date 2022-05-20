import datetime
import random
from re import A
import pygame
import math
from tokenize import Double
from .Utils import *
from . import Tile
from .Lib import *
from .Camera import *

class Map():
    def __init__(self, w, h, load, codedMap = None): #load true si quieres que cargue el codedMap
        self.tw = TILE_WIDTH
        self.th = TILE_HEIGHT
        self.mapa = []
        #matriz de tiles codificadas para guardar en fichero. Formato: "tipoSprite" + "numSprite"
        self.codedMap = codedMap
        self.w = w
        self.h = h

        self.tiles = [[], []]
        self.tiles.insert(0, cargarSprites(TERRENO_PATH, 8, False))
        self.tiles.insert(1, cargarSprites(ELEVACION_PATH, 40, True))
        self.tiles.insert(2, cargarSprites(CREEP_PATH, 8, False))
        if load:
            if codedMap == None:
                self.generateRandomMap()
            self.load()
            #self.loadMinimap()
        self.TILES_WIDTH = w
        self.TILES_HEIGHT = h

    #Dibuja el mapa
    def drawMap(self, screen, camera):
        firstTileX, firstTileY = self.getTileIndex(camera.x, camera.y)
        lastTileX, lastTileY = self.getTileIndex(camera.x + camera.w, camera.y + camera.h)
        for i in range(firstTileY, lastTileY + 1):
            for j in range(firstTileX, lastTileX + 1):
                self.mapa[i][j].draw(screen, camera)

    def drawNiebla(self, screen, camera):
        firstTileX, firstTileY = self.getTileIndex(camera.x, camera.y)
        lastTileX, lastTileY = self.getTileIndex(camera.x + camera.w, camera.y + camera.h)
        for i in range(firstTileY, lastTileY + 1):
            for j in range(firstTileX, lastTileX + 1):
                r = self.mapa[i][j].getRect()
                if (r.x + r.w >= camera.x and r.x <= camera.x + camera.w and
                    r.y + r.h >= camera.y and r.y <= camera.y + camera.h):
                    self.mapa[i][j].drawNiebla(screen, camera)


    def updateNiebla(self, camera, locationEntitiesOnCamera):
        firstTileX, firstTileY = self.getTileIndex(camera.x, camera.y)
        lastTileX, lastTileY = self.getTileIndex(camera.x + camera.w, camera.y + camera.h)
        for i in range(firstTileY, lastTileY + 1):
            for j in range(firstTileX, lastTileX + 1):
                self.mapa[i][j].visible = False

        centers = []
        for l in locationEntitiesOnCamera:
            i, j = self.getTileIndex(l[0], l[1])
            centers.append((i, j))

        maxJ, maxI = self.getTileIndex(self.w, self.h)
        for c in centers:
            for i in range(c[1] - VISION_RADIUS, c[1] + VISION_RADIUS):
                for j in range(c[0] - VISION_RADIUS, c[0] + VISION_RADIUS):
                    if ((i >= 0 and j >= 0) and (i < maxI+1 and j < maxJ+1)
                            and ((i - (c[1]))**2 + ((j - (c[0]))**2)) < VISION_RADIUS**2):
                        self.mapa[i][j].visible = True
                        self.mapa[i][j].oscura = False

    #Pone a true las Tiles del rectangulo que forman x,y,w,h
    def addObstacle(self, x, y, w, h):
        for i in range(h): #Recorro el mapa  por las filas
            for j in range(w): #En la fila i recorro las columnas
                self.mapa[i + int(y / self.th)][j + int(x / self.tw)].type = 1

    def setObstacle(self, tile):
        tile.type = 1

    def addOre(self, x, y):
        #print(int(y / self.th), int(x / self.tw))
        self.mapa[x][y].type = 3

    #Devuelve la Tile que se encuentra en las coordenadas x,y
    def getTile(self, x, y):
        xaux = int(x / self.tw)
        yaux = int(y / self.th)

        if int(x / self.tw) >= len(self.mapa[0]):
            xaux = len(self.mapa[0]) - 1
        if int(y / self.th) >= len(self.mapa):
            yaux = len(self.mapa) - 1
        #print(xaux, yaux)
        return self.mapa[yaux][xaux]

    def getRectTiles(self, rect):
        tiles = []
        x = (self.getTile(rect.x, rect.y)).centerx
        finx = rect.x + rect.w
        y = (self.getTile(rect.x, rect.y)).centery
        finy = rect.y + rect.h
        #print(rect.x, rect.y, rect.w, rect.h)
        while x <= finx:
            while y <= finy:
                tile = self.getTile(x,y)
                tiles.append(tile)
                y = y + self.th
            y = self.getTile(rect.x, rect.y).centery
            x = x + self.tw
        return tiles

    #Devuelve la Tile que se encuentra en las coordenadas x,y
    def getTile(self, x, y):
        xaux = int(x / self.tw)
        yaux = int(y / self.th)

        if int(x / self.tw) >= len(self.mapa[0]):
            xaux = len(self.mapa[0]) - 1
        elif int(x / self.tw) < 0:
            xaux = 0
        if int(y / self.th) >= len(self.mapa):
            yaux = len(self.mapa) - 1
        elif int(y / self.th) < 0:
            yaux = 0
        #print(xaux, yaux)
        if (xaux >= 0) and (yaux >= 0):
            return self.mapa[yaux][xaux]
        return None

    def getRectRoundTiles(self, rect, tileActual):
        tiles = []
        x = self.getTile(rect.x, rect.y).centerx
        finx = rect.x + rect.w
        y = self.getTile(rect.x, rect.y).centery
        finy = rect.y + rect.h
        #print(rect.x, rect.y, rect.w, rect.h)
        while x <= finx:
            tileUp = self.getTile(x, y - TILE_HEIGHT)
            tileDown = self.getTile(x, finy + TILE_HEIGHT)
            #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
            if tileUp.type == 0 or tileUp == tileActual:
                #print("tileUp:", tileUp.tileid)
                tiles.append(tileUp)
            if tileDown.type == 0 or tileDown == tileActual:
                #print("tileDown: ", tileDown.tileid)
                tiles.append(tileDown)
            x += TILE_WIDTH
        x = self.getTile(rect.x, rect.y).centerx
        while y <= finy:
            tileUp = self.getTile(x - TILE_WIDTH, y)
            tileDown = self.getTile(finx + TILE_WIDTH, y)
            #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
            if tileUp.type == 0 or tileUp == tileActual:
                #print("tileUp:", tileUp.tileid)
                tiles.append(tileUp)
            if tileDown.type == 0 or tileDown == tileActual:
                #print("tileDown: ", tileDown.tileid)
                tiles.append(tileDown)
            y += TILE_HEIGHT
        #input()
        #FALTAN LAS ESQUINA
        x = self.getTile(rect.x, rect.y).centerx
        finx = rect.x + rect.w
        y = self.getTile(rect.x, rect.y).centery
        finy = rect.y + rect.h
        tileUp = self.getTile(x - 40, y - 40)
        tileDown = self.getTile(finx + 40,y - 40)
        #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
        if tileUp.type == 0 or tileUp == tileActual:
            #print("tileUp:", tileUp.tileid)
            tiles.append(tileUp)
        if tileDown.type == 0 or tileDown == tileActual:
            #print("tileDown: ", tileDown.tileid)
            tiles.append(tileDown)
        tileUp = self.getTile(x - 40, finy + 40)
        tileDown = self.getTile(finx + 40, finy + 40)
        #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
        if tileUp.type == 0 or tileUp == tileActual:
            #print("tileUp:", tileUp.tileid)
            tiles.append(tileUp)
        if tileDown.type == 0 or tileDown == tileActual:
            #print("tileDown: ", tileDown.tileid)
            tiles.append(tileDown)
        return tiles

    def getEntityTilesVecinas(self, tile, tileActual):
        tilesObj = []
        if tile.ocupante != None:
            r = tile.ocupante.getRect()
            tiles = self.getRectRoundTiles(r, tileActual) #se puede mejorar
            for t in tiles:
                tilesObj.append(t)
        else:
            tilesObj.append(tile)
        return list(set(tilesObj))

    def getTileCenter(self, x, y):
        return ((x*self.tw - self.tw/2), (y*self.th - self.th/2))

    def getTileIndex(self, x, y):
        xaux = int(x / self.tw)
        yaux = int(y / self.th)

        if xaux >= len(self.mapa[0]):
            xaux = len(self.mapa[0]) - 1
        elif xaux < 0:
            xaux = 0
        if yaux >= len(self.mapa):
            yaux = len(self.mapa) - 1
        elif yaux < 0:
            yaux = 0
        #print(xaux, yaux)
        return xaux, yaux

    #Devuelve la funcion heuristica de una tile(Distancia al objetivo)
    def heur(self, tini, tfin):
        return int(math.hypot(tfin.centerx - tini.centerx, tfin.centery - tini.centery))

    #Pone la tile como vecina
    def setVecina(self, tile, id):

        if tile.type == EMPTY:
            tile.setOcupada(id)
        else:
            #print("HI")
            pass


    #Pone la tile como recurso
    def setRecurso(self, tile):
        self.mapa[int(tile.centery / self.th)][int(tile.centerx / self.tw)].type = RESOURCE

    def setType(self, tile, type):
        self.mapa[int(tile.centery / self.th)][int(tile.centerx / self.tw)].type = type

    #Pone la tile como libre
    def setLibre(self, tile):
        #print("CAGO EN DIOS")
        if self.mapa[int(tile.centery / self.th)][int(tile.centerx / self.tw)].type == EMPTY:
            #print("hi")
            pass
        else:
            self.mapa[int(tile.centery / self.th)][int(tile.centerx / self.tw)].type = EMPTY
            self.mapa[int(tile.centery / self.th)][int(tile.centerx / self.tw)].ocupante = None

    #Pone las tiles como libre dada la esquina inferior derecha de un rectangulo y su altura y su anchura
    def setLibres(self, structure, tile, width, height):
        #print("CAGO EN DIOS")
        x = int(tile.centerx / self.tw)
        y = int(tile.centery / self.th)
        for xAux in range(x - height, x + width):
            for yAux in range(y - height, y + height):
                if (xAux >= 0) and (xAux < self.w) and (yAux >= 0) and (yAux < self.h):
                    if self.mapa[yAux][xAux].type == EMPTY:
                        #print("hi")
                        pass
                    elif (self.mapa[yAux][xAux].type == STRUCTURE) and (self.mapa[yAux][xAux].ocupante == structure):
                        self.mapa[yAux][xAux].type = EMPTY
                        self.mapa[yAux][xAux].ocupante = None

    #Devuelve una lista de tiles vecinas libres a la dada
    def getTileVecinas(self, tile, tileObj):
        tilesVecinas = []
        aux = self.getTile(tile.centerx + self.tw, tile.centery)#tile derecha
        if aux.type == 0 or aux == tileObj:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx + self.tw, tile.centery + self.th) #tile esquina superior derecha
        if aux.type == 0 or aux == tileObj:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx + self.tw, tile.centery - self.th) #tile esquina inferior derecha
        if aux.type == 0 or aux == tileObj:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx, tile.centery - self.th) #tile inferior
        if aux.type == 0 or aux == tileObj:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx, tile.centery + self.th) #tile superior
        if aux.type == 0 or aux == tileObj:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw, tile.centery) #tile izquierda
        if aux.type == 0 or aux == tileObj:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw, tile.centery + self.th) #tile esquina superior izquierda
        if aux.type == 0 or aux == tileObj:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw, tile.centery - self.th) #tile esquina inferior izquierda
        if aux.type == 0 or aux == tileObj:
            tilesVecinas.append(aux)

        return tilesVecinas

    #Devuelve una lista de tiles vecinas a la dada
    def getAllTileVecinas(self, tile):
        tilesVecinas = []
        aux = self.getTile(tile.centerx + self.tw,tile.centery)#tile derecha
        tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx + self.tw,tile.centery + self.th) #tile esquina superior derecha
        tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx + self.tw,tile.centery - self.th) #tile esquina inferior derecha
        tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx, tile.centery - self.th) #tile inferior
        tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx, tile.centery + self.th) #tile superior
        tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery) #tile izquierda
        tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery + self.th) #tile esquina superior izquierda
        tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery - self.th) #tile esquina inferior izquierda
        tilesVecinas.append(aux)

        return tilesVecinas

    def calcDest(self, xini, yini, xfin, yfin):
        destino = self.getTile(xfin, yfin)
        xaux = xfin
        yaux = yfin
        while destino.type != 0:
            xaux = xaux - ((xfin - xini) / 10)
            yaux = yaux - ((yfin - yini) / 10)
            destino = self.getTile(xaux, yaux)
        return destino

    def calcPath(self, xini, yini, xfin, yfin):
        path = [] # Lista de TILES
        visitados = []
        tactual = self.getTile(xini, yini)
        tfin = self.calcDest(xini, yini, xfin, yfin)
        #print("Distancia a la tile final",tactual.centerx, tactual.centery, tfin.centerx, tfin.centery)
        if self.heur(tactual, tfin) != 0:
            tilePosibles = self.getTileVecinas(tactual)
            tileCandidata = tilePosibles[0]
            tileSIG = tactual
            tileAnt = tactual
            if self.heur(tileCandidata, tfin) == 0:
                path.append(tileCandidata)
            while self.heur(tileCandidata, tfin) != 0:
                tilePosibles = self.getTileVecinas(tileSIG)
                tileCandidata = tilePosibles[0]
                for tile in tilePosibles:
                    if tile not in visitados:
                        #print(tile.centerx, tile.centery, tileAnt.centerx, tileAnt.centery)
                        if  tile != tileAnt:
                            #print(self.heur(tile,tfin), self.heur(tileCandidata,tfin))
                            if self.heur(tile,tfin) < self.heur(tileCandidata, tfin):
                                tileCandidata = tile
                path.append(tileCandidata)
                visitados.append(tileCandidata)
                tileAnt = tileSIG
                tileSIG = tileCandidata
                #print("Candidata elegida", tileCandidata.centerx, tileCandidata.centery)
        return path

    def reCalcPath(self, tactual,tfin,tSaltar):
        path = [] # Lista de TILES
        visitados = []
        #print("Distancia a la tile final",tactual.centerx, tactual.centery, tfin.centerx, tfin.centery)
        if self.heur(tactual, tfin) != 0:
            tilePosibles = self.getTileVecinas(tactual)
            tileCandidata = tilePosibles[0]
            tileSIG = tactual
            tileAnt = tactual
            if self.heur(tileCandidata, tfin) == 0:
                path.append(tileCandidata)
            while self.heur(tileCandidata, tfin) != 0:
                tilePosibles = self.getTileVecinas(tileSIG)
                tileCandidata = tilePosibles[0]
                for tile in tilePosibles:
                    if tile not in visitados:
                        #print(tile.centerx, tile.centery, tileAnt.centerx, tileAnt.centery)
                        if  tile != tileAnt and tile != tSaltar:
                            #print(self.heur(tile,tfin), self.heur(tileCandidata,tfin))
                            if self.heur(tile,tfin) < self.heur(tileCandidata, tfin):
                                tileCandidata = tile
                path.append(tileCandidata)
                visitados.append(tileCandidata)
                tileAnt = tileSIG
                tileSIG = tileCandidata
                #print("Candidata elegida", tileCandidata.centerx, tileCandidata.centery)
        return path

    def setTileG(self, tile, g):
        self.mapa[int(tile.centery / self.th)][int(tile.centerx / self.tw)].g = g

    def setTilePadre(self, tile, padre):
        self.mapa[int(tile.centery / self.th)][int(tile.centerx / self.tw)].padre = padre

    def getTileVecinaCercana(self, tileIni, tileObj):
        tiles = self.getTileVecinas(tileObj, None)
        if tiles.__len__() == 0:
            return Tile.Tile(-1, 0, 0, 0, 0, 0, 0)
        bestTile = tiles[0]
        for tile in tiles:
            if tile.heur(tileIni) < bestTile.heur(tileIni):
                bestTile = tile
        return bestTile

    def getTileOcupadaCercana(self, tileIni, tileObj):
        #print("Estamos en", tileObj.tileid, tileIni.tileid)
        tiles = self.getAllTileVecinas(tileObj)
        bestTile = tiles[0]
        for tile in tiles:
            if tile.heur(tileIni) < bestTile.heur(tileIni):
                bestTile = tile
        return bestTile

    def getTileCercana(self, tileIni, tileObj):
        tileCercana = self.getTileOcupadaCercana(tileIni, tileObj)
        while tileCercana.type != 0:
            #print("TileCercana: ", tileCercana.tileid, tileCercana.type)
            if tileCercana.tileid == tileIni.tileid:
                return tileCercana
            tileCercana = self.getTileOcupadaCercana(tileIni, tileCercana)
        return tileCercana




    def Astar(self, tileIni, tileObj):
        #print("VOY DE ", tileIni.tileid, "A ",  tileObj.tileid)
#input()
        if tileIni.tileid == tileObj.tileid:
            return [tileIni]
        #if(tileObj.type != 0):
            #tileObj = self.getTileVecinaCercana(tileIni, tileObj)
        nodosAbiertos = []
        nodosCerrados = []
        nodosAbiertos.append(tileIni)
        nodosAbiertos[0].padre = nodosAbiertos[0]
        jaja = 0
        broken = False
        while (nodosAbiertos.__len__() != 0) and not broken:
            jaja += 1
            if jaja >= 400:
                broken = True
            currentTile = Tile.Tile(nodosAbiertos[0].tileid, nodosAbiertos[0].centerx, nodosAbiertos[0].centery,
                    0, 0, 1, 0, nodosAbiertos[0].g, nodosAbiertos[0].padre)
            #print("heur: ",currentTile.heur(tileObj))
            currentF = currentTile.g + currentTile.heur(tileObj)
            currentId = 0
            for id, tile in enumerate(nodosAbiertos):
                tileF = tile.g + tile.heur(tileObj)
                if float(currentF) > float(tileF):
                    currentTile = Tile.Tile(tile.tileid, tile.centerx, tile.centery, 0, 0, 1, currentTile.type, tile.g, tile.padre)
                    currentF = tileF
                    currentId = id
            #Tenemos la tile con menos f
            #print("estamos en", currentTile.tileid , currentTile.padre.tileid )

            nodosCerrados.append(currentTile)
            nodosAbiertos.pop(currentId)
            if currentTile.tileid == tileObj.tileid:
                break
            for tile in self.getTileVecinas(currentTile, tileObj):
                #if tile.tileid == 644:
                    #print("miro tile: ", tile.tileid , tile.g, tile.type)
                ##input()
                if Tile.mismoId(nodosCerrados, tile).tileid == -1:# No esta
                    #print("No esta en cerrados, miro en abiertos")
                    tileEnAbiertos = Tile.mismoId(nodosAbiertos, tile)
                    if  tileEnAbiertos.tileid == -1: #No esta
                        #print("no esta en abiertos")
                        #print(tile.g)
                        tileMapa = self.getTile(tile.centerx, tile.centery)
                        tileMapa.padre = currentTile
                        tileAppend = Tile.Tile(tile.tileid, tile.centerx, tile.centery,
                             0, 0, 1, currentTile.type, currentTile.g + currentTile.heur(tile), tileMapa.padre)
                        nodosAbiertos.append(tileAppend)
                        self.setTilePadre(tile, currentTile)
                        tile.padre = currentTile
                    else:
                        #print("esta en abiertos", tileEnAbiertos.g,"y he encontrado",currentTile.g + currentTile.heur(tile) )
                        if tileEnAbiertos.g + currentTile.heur(tileObj) > (currentTile.g + currentTile.heur(tile)):
                            #print("CHANGE")
                            nodosAbiertos.remove(tileEnAbiertos)
                            self.setTilePadre(tile, currentTile)
                            tileMapa = self.getTile(tile.centerx, tile.centery)
                            tileMapa.padre = currentTile
                            tileAppend = Tile.Tile(tile.tileid, tile.centerx, tile.centery,
                             0, 0, 1, currentTile.type, currentTile.g + currentTile.heur(tile), tileMapa.padre)
                            nodosAbiertos.append(tileAppend)

        path = []
        pathReturn = []
        if (nodosAbiertos.__len__() == 0) or broken:
            #print("camino no encontrado", tileObj.tileid)

            #input()
            pass
        else:
            #print("camino encontrado")
            currentTile = self.getTile(tileObj.centerx, tileObj.centery)
            while currentTile != tileIni:
                #print(currentTile.tileid, currentTile.type)
                path.append(currentTile)
                currentTile = currentTile.padre
            #print(currentTile.tileid)
            i = path.__len__() - 1
            #print("AAAAAAAAAAAA")
            while i >= 0:
                pathReturn.append(path[i])
                i = i - 1
        #print("nodos: ", jaja)
        return pathReturn

    def AstarNoLimit(self, tileIni, tileObj):
        #print("VOY DE ", tileIni.tileid, "A ",  tileObj.tileid)
#input()
        if tileIni.tileid == tileObj.tileid:
            return [tileIni]
        #if(tileObj.type != 0):
            #tileObj = self.getTileVecinaCercana(tileIni, tileObj)
        nodosAbiertos = []
        nodosCerrados = []
        nodosAbiertos.append(tileIni)
        nodosAbiertos[0].padre = nodosAbiertos[0]
        jaja = 0
        broken = False
        while (nodosAbiertos.__len__() != 0) and not broken:
            jaja += 1
            if jaja >= 1000:
                broken = True
            currentTile = Tile.Tile(nodosAbiertos[0].tileid, nodosAbiertos[0].centerx, nodosAbiertos[0].centery,
                    0, 0, 1, 0, nodosAbiertos[0].g, nodosAbiertos[0].padre)
            #print("heur: ",currentTile.heur(tileObj))
            currentF = currentTile.g + currentTile.heur(tileObj)
            currentId = 0
            for id, tile in enumerate(nodosAbiertos):
                tileF = tile.g + tile.heur(tileObj)
                #print(currentTile.tileid ,":", currentTile.g,currentTile.heur(tileObj) ,tile.tileid,":", tile.g,tile.heur(tileObj))
                if float(currentF) > float(tileF):
                    currentTile = Tile.Tile(tile.tileid, tile.centerx, tile.centery, 0, 0, 1, currentTile.type, tile.g, tile.padre)
                    currentF = tileF
                    currentId = id
            #Tenemos la tile con menos f
            #print("estamos en", currentTile.tileid , currentTile.padre.tileid )
#input()

            nodosCerrados.append(currentTile)
            nodosAbiertos.pop(currentId)
            if currentTile.tileid == tileObj.tileid:
                break
            for tile in self.getTileVecinas(currentTile, tileObj):
                #if tile.tileid == 644:
                    #print("miro tile: ", tile.tileid , tile.g, tile.type)
                ##input()
                if Tile.mismoId(nodosCerrados, tile).tileid == -1:# No esta
                    #print("No esta en cerrados, miro en abiertos")
                    tileEnAbiertos = Tile.mismoId(nodosAbiertos, tile)
                    if  tileEnAbiertos.tileid == -1: #No esta
                        #print("no esta en abiertos")
                        #print(tile.g)
                        tileMapa = self.getTile(tile.centerx, tile.centery)
                        tileMapa.padre = currentTile
                        tileAppend = Tile.Tile(tile.tileid, tile.centerx, tile.centery,
                             0, 0, 1, currentTile.type, currentTile.g + currentTile.heur(tile), tileMapa.padre)
                        nodosAbiertos.append(tileAppend)
                        self.setTilePadre(tile, currentTile)
                        tile.padre = currentTile
                    else:
                        #print("esta en abiertos", tileEnAbiertos.g,"y he encontrado",currentTile.g + currentTile.heur(tile) )
                        if tileEnAbiertos.g > (currentTile.g + currentTile.heur(tile)):
                            #print("CHANGE")
                            nodosAbiertos.remove(tileEnAbiertos)
                            self.setTilePadre(tile, currentTile)
                            tileMapa = self.getTile(tile.centerx, tile.centery)
                            tileMapa.padre = currentTile
                            tileAppend = Tile.Tile(tile.tileid, tile.centerx, tile.centery,
                             0, 0, 1, currentTile.type, currentTile.g + currentTile.heur(tile), tileMapa.padre)
                            nodosAbiertos.append(tileAppend)

        path = []
        pathReturn = []
        for tile in nodosAbiertos:
            tile.g = 0
        if (nodosAbiertos.__len__() == 0) or broken:
            #print("camino no encontrado", tileObj.tileid)
            pass
            #input()
        else:
            #print("camino encontrado")
            currentTile = self.getTile(tileObj.centerx, tileObj.centery)
            while currentTile != tileIni:
                #print(currentTile.tileid, currentTile.type)
                path.append(currentTile)
                currentTile = currentTile.padre
            #print(currentTile.tileid)
            i = path.__len__() - 1
            #print("--------------------")
            while i >= 0:
                pathReturn.append(path[i])
                i = i - 1

        return pathReturn

    #empieza a cargar el mapa
    def load(self):
        if self.codedMap == None:
            self.generateRandomMap()
        self.w = len(self.codedMap[0]) * self.tw
        self.h = len(self.codedMap) * self.th

        for i in range(len(self.codedMap)):
            self.mapa.insert(i,[])#Es una matriz que representa el mapa(0 es suelo, 1 es obstaculo, 2 vecino)
            for j in range(len(self.codedMap[0])):
                tile_sprite, type = self.loadTile(str(self.codedMap[i][j]))
                tile = Tile.Tile(i*len(self.codedMap[0]) + j, self.tw * j, self.th * i, self.tw, self.th, tile_sprite, type)
                self.mapa[i].insert(j,tile)

    #carga el tile con codigo code
    def loadTile(self, code):
        if code[0] == '1': #terreno
            index = int(code[1:])
            return self.tiles[0][index], 0
        elif code[0] == '2': #elevacion
            index = int(code[1:])
            return self.tiles[1][index], 1
        else: #creep
            index = int(code[1:])
            return self.tiles[2][index], 0
    #genera mapa con suelos aleatorios
    def generateRandomMap(self):
        random.seed(datetime.datetime.now())
        self.codedMap = []
        for i in range(self.h):
            self.codedMap.insert(i,[])
            for j in range(self.w):
                self.codedMap[i].insert(j, str(100 + random.randint(0, 7)))

    #setea una elevacion en la coordenada x, y
    def setElevacion(self, x, y):
        tile = 0
        for j in range(y, y+5):
            if j == y or j == y+4:
                tile+=2
                for i in range(x+2, x+6):
                    self.codedMap[j][i] = str(200 + tile)
                    tile += 1
                tile+=2
            else:
                for i in range(x, x+8):
                    self.codedMap[j][i] = str(200 + tile)
                    tile += 1
        pass

    def drawMinimap(self, screen):
        y = 0
        for i in range(len(self.minimap)):
            x = 0
            for j in range(len(self.minimap[0])):
                screen.blit(self.minimap[i][j], [round(MINIMAP_X + x), round(MINIMAP_Y + y)])
                x += round(200/len(self.mapa[0]))
                #print(205/len(self.mapa[0]))
            y += round(200/len(self.mapa))
            #print("y ", 205/len(self.mapa))

    def loadMinimap(self):
        self.minimap = []
        for i in range(len(self.mapa)):
            self.minimap.insert(i,[])#Es una matriz que representa el mapa(0 es suelo, 1 es obstaculo, 2 vecino)
            for j in range(len(self.mapa[0])):
                image = (self.mapa[i][j]).image
                tile_sprite = pg.transform.scale(image, [round(200/len(self.mapa[0])), round(200/len(self.mapa))])
                #print(tile_sprite.get_rect())
                self.minimap[i].insert(j, tile_sprite)

    #Pre: en mapa está cargado/construido
    def loadOscuridad(self, matrizOscuridad):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                self.mapa[i][j].oscura = matrizOscuridad[i][j]

    def getMinimap(self):
        return self.minimap

    def toDictionary(self):
        matrizOscuridad = []
        for i in range(len(self.mapa)):
            matrizOscuridad.insert(i,[])
            for j in range(len(self.mapa[0])):
                matrizOscuridad[i].insert(j, self.mapa[i][j].oscura)

        return {
            "w": int(self.w / self.tw),
            "h": int(self.h / self.th),
            "map": self.codedMap,
            "matrizOscuridad": matrizOscuridad
        }

    # Devuelve si existe la siguiente tile en funcion de base y desplazamiento
    def getNextTileByOffset(self, x, y, xOffset, yOffset):
        xAux = x + xOffset
        yAux = y + yOffset
        if (xAux >= 0) and (xAux < self.TILES_WIDTH) and (yAux >= 0) and (yAux < self.TILES_HEIGHT):
            return self.mapa[int(yAux)][int(xAux)]
        return None

    # Devuelve si estan libres todas las tiles entre esquina sup izq y inf der
    def checkIfEmptyZone(self, xUpLeft, yUpLeft, xBotRight, yBotRight):
        if (xUpLeft >= 0) and (xUpLeft < self.TILES_WIDTH) and (yUpLeft >= 0) and (yUpLeft < self.TILES_HEIGHT):
            if (xBotRight >= 0) and (xBotRight < self.TILES_WIDTH) and (yBotRight >= 0) and (yBotRight < self.TILES_HEIGHT):
                for x in range(int(xUpLeft), int(xBotRight)):
                    for y in range(int(yUpLeft), int(yBotRight)):
                        if self.mapa[y][x].type != EMPTY:
                            return False
                return True
        return False

    def getAttackRoundTiles(self, rect):
        tiles = []
        x = self.getTile(rect.x, rect.y).centerx
        finx = rect.x + rect.w
        y = self.getTile(rect.x, rect.y).centery
        finy = rect.y + rect.h
        #print(rect.x, rect.y, rect.w, rect.h)
        while x <= finx:
            tileUp = self.getTile(x, y)
            tileDown = self.getTile(x, finy)
            tiles.append(tileUp)
            tiles.append(tileDown)
            #tileUp.tileid, tileDown.tileid)
            x += TILE_WIDTH
        x = self.getTile(rect.x, rect.y).centerx
        while y <= finy:
            tileUp = self.getTile(x, y)
            tileDown = self.getTile(finx, y)
            #print(tileUp.tileid, tileDown.tileid)
            y += TILE_HEIGHT
        #input()
        return tiles

    # Devuelve la primera entidad enemiga (estructura o unidad) encontrada en un cuadrado de NEARBY_RANGE
    # que no sea del player player alrededor de la tile tile
    def getNearbyRival(self, tile, player, distance = NEARBY_RANGE):
        player1 = player
        x = tile.x / 40
        y = tile.y / 40
        for i in range(2 * distance + 1):
            col = int(i - distance + x)
            for j in range(2 * distance + 1):
                row = int(j - distance + y)
                if (col >= 0) and (col < self.TILES_WIDTH) and (row >= 0) and (row < self.TILES_HEIGHT):
                    aux = self.mapa[row][col]
                    if ((aux.type == UNIT) or (aux.type == STRUCTURE)) and (aux.ocupante.hp > 0):
                        #print("PLAYER2? ", aux.ocupante.player)
                        if aux.ocupante.player != player1:
                            return aux.ocupante
        return None

    # Devuelve las entidades enemigas (estructura o unidad) encontradas en un cuadrado de distance tiles
    # que no sea del player player alrededor de la tile tile
    def getNearbyRivals(self, tile, player, distance):
        player1 = player
        x = tile.x / 40
        y = tile.y / 40
        result = set()
        for i in range(2 * distance + 1):
            col = int(i - distance + x)
            for j in range(2 * distance + 1):
                row = int(j - distance + y)
                if (col >= 0) and (col < self.TILES_WIDTH) and (row >= 0) and (row < self.TILES_HEIGHT):
                    aux = self.mapa[row][col]
                    if (aux.type == UNIT) or (aux.type == STRUCTURE):
                        #print(aux.ocupante.type, " ", col, " ", row)
                        if aux.ocupante.player != player1:
                            result.add(aux.ocupante)
        return result

    # Devuelve el primer geyser encontrado libre en un cuadrado de distance tiles
    # alrededor de la tile tile
    def findNearbyGeyser(self, tile, distance):
        x = tile.x / 40
        y = tile.y / 40
        for i in range(2 * distance + 1):
            col = int(i - distance + x)
            for j in range(2 * distance + 1):
                row = int(j - distance + y)
                if (col >= 0) and (col < self.TILES_WIDTH) and (row >= 0) and (row < self.TILES_HEIGHT):
                    aux = self.mapa[row][col]
                    if aux.type == GEYSER:
                        return aux.ocupante
        return None

    # Devuelve los cristales encontrados en un cuadrado de distance tiles
    # alrededor de la tile tile
    def findCrystals(self, tile, distance):
        crystalsFound = set()
        x = tile.x / 40
        y = tile.y / 40
        for i in range(2 * distance + 1):
            col = int(i - distance + x)
            for j in range(2 * distance + 1):
                row = int(j - distance + y)
                if (col >= 0) and (col < self.TILES_WIDTH) and (row >= 0) and (row < self.TILES_HEIGHT):
                    aux = self.mapa[row][col]
                    if aux.type == RESOURCE and aux.ocupante.capacity > 0:
                        crystalsFound.add(aux.ocupante)
        return crystalsFound
