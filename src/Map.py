import pygame
import math
from tokenize import Double
from . import Utils
from . import Tile

class Map():
    def __init__(self, w, h, mapa=None):
        self.tw = 40
        self.th = 40
        self.map = []
        self.h = h * self.th
        self.w = w * self.tw
        self.tiles = [[], []]
        self.tiles.insert(0, Utils.cargarSprites(Utils.TERRENO_PATH, 8, False))
        self.tiles.insert(1, Utils.cargarSprites(Utils.ELEVACION_PATH, 40, True))
        if mapa != None:
            self.load(mapa)

    #Dibuja el mapa
    def drawMap(self, screen, camera):
        #for i in range(len(self.map)): #i es el valor de la fila
        #    for j in range(len(self.map[i])): #j es el valor de la columna
        #        tile = self.map[i][j]
        #        if tile.type == 1:
        #           pygame.draw.rect(screen, RED, pygame.Rect(tile.getRect()), 1)
        #        elif tile.type == 0:
        #            pygame.draw.rect(screen, GREEN, pygame.Rect(tile.getRect()),1)
        #        else:
        #            pygame.draw.rect(screen, BLUE, pygame.Rect(tile.getRect()),1)
        firstTileY, firstTileX = self.getTileIndex(camera.x, camera.y)
        lastTileY, lastTileX = self.getTileIndex(camera.x + camera.w, camera.y + camera.h)
        for i in range(firstTileY, lastTileY + 1):
            for j in range(firstTileX, lastTileX + 1):
                self.map[i][j].draw(screen, camera)
    
    def drawMap2(self, screen, camera):
        #for i in range(len(self.map)): #i es el valor de la fila
        #    for j in range(len(self.map[i])): #j es el valor de la columna
        #        tile = self.map[i][j]
        #        if tile.type == 1:
        #           pygame.draw.rect(screen, RED, pygame.Rect(tile.getRect()), 1)
        #        elif tile.type == 0:
        #            pygame.draw.rect(screen, GREEN, pygame.Rect(tile.getRect()),1)
        #        else:
        #            pygame.draw.rect(screen, BLUE, pygame.Rect(tile.getRect()),1)
        firstTileY, firstTileX = self.getTileIndex(camera.x, camera.y)
        lastTileY, lastTileX = self.getTileIndex(camera.x + camera.w, camera.y + camera.h)
        for i in range(firstTileY, lastTileY + 1):
            for j in range(firstTileX, lastTileX + 1):
                tile = self.map[i][j]

                #pasar las coords del rectangulo de coordenadas globales a coordenadas de la camara
                globalRectCoords = tile.getRect()
                cameraRectCoords = (globalRectCoords[0] - camera.x, globalRectCoords[1] - camera.y, globalRectCoords[2], globalRectCoords[3])
                if tile.type == 1:
                   pygame.draw.rect(screen, Utils.RED, pygame.Rect(cameraRectCoords), 1)
                elif tile.type == 0:
                    pygame.draw.rect(screen, Utils.GREEN, pygame.Rect(cameraRectCoords), 1)
                elif tile.type == 3:
                    pygame.draw.rect(screen, Utils.BLUE, pygame.Rect(cameraRectCoords), 1)
                else:
                    pygame.draw.rect(screen, Utils.PURPLE, pygame.Rect(cameraRectCoords), 1)
    
    #Pone a true las Tiles del rectangulo que forman x,y,w,h
    def addObstacle(self, x, y, w, h):
        for i in range(h): #Recorro el mapa  por las filas
            for j in range(w): #En la fila i recorro las columnas
                self.map[i + int(y / self.th)][j + int(x / self.tw)].type = 1
    
    def addOre(self, x, y):
        print(int(y / self.th), int(x / self.tw))
        self.map[int(y / self.th)][int(x / self.tw)].type = 3
    
    #Devuelve la Tile que se encuentra en las coordenadas x,y
    def getTile(self, x, y):
        xaux = int(x / self.tw)
        yaux = int(y / self.th)
        
        if int(x / self.tw) >= len(self.map[0]):
            xaux = len(self.map[0]) - 1
        if int(y / self.th) >= len(self.map):   
            yaux = len(self.map) - 1
        #print(xaux, yaux)    
        return self.map[yaux][xaux]

    def getTileIndex(self, x, y):
        xaux = int(x / self.tw)
        yaux = int(y / self.th)
        
        if int(x / self.tw) >= len(self.map[0]):
            xaux = len(self.map[0]) - 1
        if int(y / self.th) >= len(self.map):   
            yaux = len(self.map) - 1
        #print(xaux, yaux)    
        return yaux, xaux

    #Devuelve la funcion heuristica de una tile(Distancia al objetivo)
    def heur(self, tini, tfin):
        return int(math.hypot(tfin.centerx - tini.centerx, tfin.centery - tini.centery))

    #Pone la tile como vecina
    def setVecina(self, tile, id):
        self.map[int(tile.centery / self.th)][int(tile.centerx / self.tw)].type = 2
        self.map[int(tile.centery / self.th)][int(tile.centerx / self.tw)].id = id
    
    #Pone la tile como libre
    def setLibre(self, tile):
        self.map[int(tile.centery / self.th)][int(tile.centerx / self.tw)].type = 0

    #Devuelve una lista de tiles vecinas a la dada
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
        self.map[int(tile.centery / self.th)][int(tile.centerx / self.tw)].g = g

    def setTilePadre(self, tile, padre):
        self.map[int(tile.centery / self.th)][int(tile.centerx / self.tw)].padre = padre

    def Astar(self, tileIni, tileObj):
        nodosAbiertos = []
        nodosCerrados = []
        nodosAbiertos.append(tileIni)
        nodosAbiertos[0].padre = nodosAbiertos[0]
        while nodosAbiertos.__len__() != 0:
            
            currentTile = Tile(nodosAbiertos[0].tileid, nodosAbiertos[0].centerx, nodosAbiertos[0].centery, 
                    0, 0, 1, nodosAbiertos[0].g, nodosAbiertos[0].padre)
            currentF = currentTile.g + currentTile.heur(tileObj)
            currentId = 0
            for id, tile in enumerate(nodosAbiertos):
                tileF = tile.g + tile.heur(tileObj)
                #print(currentTile.tileid + 1,":", currentTile.g,currentTile.heur(tileObj) ,tile.tileid + 1,":", tile.g,tile.heur(tileObj))
                if float(currentF) > float(tileF):
                    currentTile = Tile.Tile(tile.tileid, tile.centerx, tile.centery, 0, 0, 1, tile.g, tile.padre)
                    currentF = tileF
                    currentId = id
            #Tenemos la tile con menos f
            #print("estamos en", currentTile.tileid + 1, currentTile.padre.tileid + 1)
            #input()
            nodosCerrados.append(currentTile)
            nodosAbiertos.pop(currentId)
            if currentTile.tileid == tileObj.tileid:
                #print("EH VOS")

                break
            for tile in self.getTileVecinas(currentTile):
                #print("miro tile: ", tile.tileid + 1)
                #input()
                if Tile.mismoId(nodosCerrados, tile).tileid == -1:# No esta
                    #print("No esta en cerrados, miro en abiertos")
                    tileEnAbiertos = Tile.mismoId(nodosAbiertos, tile)
                    if  tileEnAbiertos.tileid == -1: #No esta
                        #print("no esta en abiertos")
                        #print(tile.g)
                        tile.g = currentTile.g + currentTile.heur(tile)
                        nodosAbiertos.append(tile)
                        self.setTilePadre(tile, currentTile)
                        tile.padre = currentTile
                    else:
                        #print("esta en abiertos", tileEnAbiertos.g,"y he encontrado",currentTile.g + currentTile.heur(tile) )
                        if tileEnAbiertos.g > (currentTile.g + currentTile.heur(tile)):
                            #print("CHANGE")
                            nodosAbiertos.remove(tileEnAbiertos)
                            nodosAbiertos.append(tile)
                            tile.padre = currentTile
                            tile.g = currentTile.g + currentTile.heur(tile)
                            self.setTilePadre(tile, currentTile)
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
    
    def load(self, mapa):
        self.w = len(mapa[0]) * self.tw
        self.h = len(mapa) * self.th
        for i in range(len(mapa)):
            self.map.insert(i,[])#Es una matriz que representa el mapa(0 es suelo, 1 es obstaculo, 2 vecino)
            for j in range(len(mapa[0])):
                tile, type = self.loadTile(str(mapa[i][j]))
                tile = Tile.Tile(i*len(mapa) + j, self.tw * j, self.th * i, self.tw, self.th, tile, type)
                self.map[i].insert(j,tile)
            
    def loadTile(self, code):
        if code[0] == '1': #terreno
            index = int(code[1:])
            return self.tiles[0][index], 0
        elif code[0] == '2': #elevacion
            index = int(code[1:])
            return self.tiles[1][index], 1