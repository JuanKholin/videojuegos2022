import datetime
import random
import pygame
import math
from tokenize import Double
from .Utils import *
from . import Tile

class Map():
    def __init__(self, w, h, load, codedMap = None): #load true si quieres que cargue el codedMap
        self.tw = 40
        self.th = 40
        self.mapa = []
        #matriz de tiles codificadas para guardar en fichero. Formato: "tipoSprite" + "numSprite"
        self.codedMap = codedMap
        self.w = w
        self.h = h
        self.tiles = [[], []]
        self.tiles.insert(0, cargarSprites(TERRENO_PATH, 8, False))
        self.tiles.insert(1, cargarSprites(ELEVACION_PATH, 40, True))
        if load:
            if codedMap == None:
                self.generateRandomMap()
            self.load()
            
    #Dibuja el mapa
    def drawMap(self, screen, camera):
        firstTileX, firstTileY = self.getTileIndex(camera.x, camera.y)
        lastTileX, lastTileY = self.getTileIndex(camera.x + camera.w, camera.y + camera.h)
        for i in range(firstTileY, lastTileY + 1):
            for j in range(firstTileX, lastTileX + 1):
                self.mapa[i][j].draw(screen, camera)

    #Pone a true las Tiles del rectangulo que forman x,y,w,h
    def addObstacle(self, x, y, w, h):
        for i in range(h): #Recorro el mapa  por las filas
            for j in range(w): #En la fila i recorro las columnas
                self.mapa[i + int(y / self.th)][j + int(x / self.tw)].type = 1

    def addOre(self, x, y):
        #print(int(y / self.th), int(x / self.tw))
        self.mapa[int(y / self.th)][int(x / self.tw)].type = 3

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
        x = self.getTile(rect.x, rect.y).centerx
        finx = rect.x + rect.w
        y = self.getTile(rect.x, rect.y).centery
        finy = rect.y + rect.h
        #print(rect.x, rect.y, rect.w, rect.h)
        while x <= finx:
            tileUp = self.getTile(x,y - 40)
            tileDown = self.getTile(x,finy + 40)
            print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
            if tileUp.type == 0:
                print("tileUp:", tileUp.tileid)
                tiles.append(tileUp)
            if tileDown.type == 0:
                print("tileDown: ", tileDown.tileid)
                tiles.append(tileDown)
            x += 40
        x = self.getTile(rect.x, rect.y).centerx
        while y <= finy:
            tileUp = self.getTile(x - 40,y)
            tileDown = self.getTile(finx + 40,y)
            print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
            if tileUp.type == 0:
                print("tileUp:", tileUp.tileid)
                tiles.append(tileUp)
            if tileDown.type == 0:
                print("tileDown: ", tileDown.tileid)
                tiles.append(tileDown)
            y += 40
        input()
        #FALTAN LAS ESQUINA
        x = self.getTile(rect.x, rect.y).centerx
        finx = rect.x + rect.w
        y = self.getTile(rect.x, rect.y).centery
        finy = rect.y + rect.h
        tileUp = self.getTile(x - 40,y - 40)
        tileDown = self.getTile(finx + 40,y - 40)
        #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
        if tileUp.type == 0:
            tiles.append(tileUp)
        if tileDown.type == 0:
            tiles.append(tileDown)
        tileUp = self.getTile(x - 40,finy + 40)
        tileDown = self.getTile(finx + 40,finy + 40)
        #print("tileUp:", tileUp.tileid, "tileDown: ", tileDown.tileid)
        if tileUp.type == 0:
            tiles.append(tileUp)
        if tileDown.type == 0:
            tiles.append(tileDown)
        return tiles

    def getEntityTilesVecinas(self, tile):
        tilesObj = []
        if tile.ocupante != None:
            r = tile.ocupante.getRect()
            tiles = self.getRectTiles(r) #se puede mejorar
            for t in tiles:
                tilesObj.append(t)
        else:
            tilesObj.append(tile)
        return list(set(tilesObj))

    def drawTiles(self, screen, camera, tiles):
        for tile in tiles:
            r = tile.getRect()
            if tile.type == 0:
                pygame.draw.rect(screen, GREEN, pygame.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)
            else:
                pygame.draw.rect(screen, RED, pygame.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)

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
        tile.setOcupada(id)

    #Pone la tile como recurso
    def setRecurso(self, tile):
        self.mapa[int(tile.centery / self.th)][int(tile.centerx / self.tw)].type = RESOURCE

    #Pone la tile como libre
    def setLibre(self, tile):
        self.mapa[int(tile.centery / self.th)][int(tile.centerx / self.tw)].type = EMPTY
        self.mapa[int(tile.centery / self.th)][int(tile.centerx / self.tw)].ocupante = None

    #Devuelve una lista de tiles vecinas libres a la dada
    def getTileVecinas(self, tile):
        tilesVecinas = []
        aux = self.getTile(tile.centerx + self.tw,tile.centery)#tile derecha
        if aux.type == 0:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx + self.tw,tile.centery + self.th) #tile esquina superior derecha
        if aux.type == 0:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx + self.tw,tile.centery - self.th) #tile esquina inferior derecha
        if aux.type == 0:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx,tile.centery - self.th) #tile inferior
        if aux.type == 0:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx,tile.centery + self.th) #tile superior
        if aux.type == 0:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery) #tile izquierda
        if aux.type == 0:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery + self.th) #tile esquina superior izquierda
        if aux.type == 0:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery - self.th) #tile esquina inferior izquierda
        if aux.type == 0:
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
        aux = self.getTile(tile.centerx,tile.centery - self.th) #tile inferior
        tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx,tile.centery + self.th) #tile superior
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
        tiles = self.getTileVecinas(tileObj)
        if tiles.__len__() == 0:
            return Tile.Tile(-1,0,0,0,0,0,0)
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
        if(tileObj.type != 0):
            tileObj = self.getTileVecinaCercana(tileIni, tileObj)
        nodosAbiertos = []
        nodosCerrados = []
        nodosAbiertos.append(tileIni)
        nodosAbiertos[0].padre = nodosAbiertos[0]
        while nodosAbiertos.__len__() != 0:
            currentTile = Tile.Tile(nodosAbiertos[0].tileid, nodosAbiertos[0].centerx, nodosAbiertos[0].centery,
                    0, 0, 1, 0, nodosAbiertos[0].g, nodosAbiertos[0].padre)
            #print("heur: ",currentTile.heur(tileObj))
            currentF = currentTile.g + currentTile.heur(tileObj)
            currentId = 0
            for id, tile in enumerate(nodosAbiertos):
                tileF = tile.g + tile.heur(tileObj)
                #print(currentTile.tileid ,":", currentTile.g,currentTile.heur(tileObj) ,tile.tileid,":", tile.g,tile.heur(tileObj))
                if float(currentF) > float(tileF):
                    currentTile = Tile.Tile(tile.tileid, tile.centerx, tile.centery, 0, 0, 1, 0, tile.g, tile.padre)
                    currentF = tileF
                    currentId = id
            #Tenemos la tile con menos f
            #print("estamos en", currentTile.tileid , currentTile.padre.tileid )
#input()

            nodosCerrados.append(currentTile)
            nodosAbiertos.pop(currentId)
            if currentTile.tileid == tileObj.tileid:
                #print("EH VOS")

                break
            for tile in self.getTileVecinas(currentTile):
                #print("miro tile: ", tile.tileid , tile.g)
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
                             0, 0, 1, 0, currentTile.g + currentTile.heur(tile), tileMapa.padre)
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
                             0, 0, 1, 0, currentTile.g + currentTile.heur(tile), tileMapa.padre)
                            nodosAbiertos.append(tileAppend)

        path = []
        pathReturn = []
        for tile in nodosAbiertos:
            tile.g = 0
        if nodosAbiertos.__len__() == 0:
            print("camino no encontrado")
        else:
            currentTile = self.getTile(tileObj.centerx, tileObj.centery)
            while currentTile != tileIni:
                #print(currentTile.tileid)
                path.append(currentTile)
                currentTile = currentTile.padre
            #print(currentTile.tileid)
            i = path.__len__() - 1
            #print("AAAAAAAAAAAA")
            while i >= 0:
                pathReturn.append(path[i])
                i = i - 1

        return pathReturn

    def load(self):
        if self.codedMap == None:
            self.generateRandomMap()
        self.w = len(self.codedMap[0]) * self.tw
        self.h = len(self.codedMap) * self.th
        
        for i in range(len(self.codedMap)):
            self.mapa.insert(i,[])#Es una matriz que representa el mapa(0 es suelo, 1 es obstaculo, 2 vecino)
            for j in range(len(self.codedMap[0])):
                tile_sprite, type = self.loadTile(str(self.codedMap[i][j]))
                tile = Tile.Tile(i*len(self.codedMap) + j, self.tw * j, self.th * i, self.tw, self.th, tile_sprite, type)
                self.mapa[i].insert(j,tile)

    def loadTile(self, code):
        if code[0] == '1': #terreno
            index = int(code[1:])
            return self.tiles[0][index], 0
        elif code[0] == '2': #elevacion
            index = int(code[1:])
            return self.tiles[1][index], 1
        
    def generateRandomMap(self):
        random.seed(datetime.datetime.now())
        self.codedMap = []
        for i in range(self.h):
            self.codedMap.insert(i,[])
            for j in range(self.w):
                self.codedMap[i].insert(j, str(100 + random.randint(0, 7)))
                
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
            
    def toDictionary(self):
        return {
            "w": int(self.w / self.tw),
            "h": int(self.h / self.th),
            "map": self.codedMap
        }