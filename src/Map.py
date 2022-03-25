import pygame
import math

# Definir colores

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

class Tile():
    def __init__(self, x, y, h, w, type):
        self.centerx = int(x + w/2)
        self.centery = int(y + h/2)
        self.h = h
        self.w = w
        self.type = type 
    
    def getRect(self):
        return (int(self.centerx - self.w/2) ,int(self.centery - self.h/2), self.w, self.h)

class Map():
    def __init__(self, h, w):
        self.tw = 40
        self.th = 40
        self.map = []
        for i in range(h):
            self.map.insert(i,[])#Es una matriz que representa el mapa(0 es suelo, 1 es obstaculo, 2 vecino)
            for j in range(w):
                tile = Tile(self.tw * j, self.th * i, self.tw, self.th, 0)
                self.map[i].insert(j,tile)
    #Dibuja el mapa
    def drawMap(self, screen):
        for i in range(len(self.map)): #i es el valor de la fila
            for j in range(len(self.map[i])): #j es el valor de la columna
                tile = self.map[i][j]
                if tile.type == 1:
                    pygame.draw.rect(screen, RED, pygame.Rect(tile.getRect()), 1)
                elif tile.type == 0:
                    pygame.draw.rect(screen, GREEN, pygame.Rect(tile.getRect()),1)
                else:
                    pygame.draw.rect(screen, BLUE, pygame.Rect(tile.getRect()),1)
    
    #Pone a true las Tiles del rectangulo que forman x,y,w,h
    def addObstacle(self, x,y,w,h):
        for i in range(h): #Recorro el mapa  por las filas
            for j  in range(w): #En la fila i recorro las columnas
                self.map[i+int(y/self.th)][j+int(x/self.tw)].type = 1
    
    #Devuelve la Tile que se encuentra en las coordenadas x,y
    def getTile(self, x, y):
        xaux = x
        yaux = y
        print(x, y)
        if x >= SCREEN_WIDTH:
            xaux = SCREEN_WIDTH-1
        if y >= SCREEN_HEIGHT:   
            yaux = SCREEN_HEIGHT-1
            
        return self.map[int(yaux/self.th)][int(xaux/self.tw)]


    #Devuelve la funcion heuristica de una tile(Distancia al objetivo)
    def heur(self,tini, tfin):
        return int(math.hypot(tfin.centerx - tini.centerx, tfin.centery - tini.centery))

    #Pone la tile como vecina
    def setVecina(self, tile):
        self.map[int(tile.centery/self.th)][int(tile.centerx/self.tw)].type = 2

    #Devuelve una lista de tiles vecinas a la dada
    def getTileVecinas(self, tile):
        tilesVecinas = []
        aux = self.getTile(tile.centerx + self.tw,tile.centery)#tile derecha
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx + self.tw,tile.centery + self.th) #tile esquina superior derecha
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx + self.tw,tile.centery - self.th) #tile esquina inferior derecha
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx,tile.centery - self.th) #tile inferior 
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx,tile.centery + self.th) #tile superior 
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery) #tile izquierda 
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery + self.th) #tile esquina superior izquierda
        if aux.type != 1:
            tilesVecinas.append(aux)
        aux = self.getTile(tile.centerx - self.tw,tile.centery - self.th) #tile esquina inferior izquierda
        if aux.type != 1:
            tilesVecinas.append(aux)

        return tilesVecinas

    def calcDest(self, xini, yini, xfin, yfin):
        destino = self.getTile(xfin, yfin)
        xaux = xfin
        yaux = yfin
        while destino.type == 1:
            xaux = xaux-((xfin-xini)/10)
            yaux = yaux-((yfin-yini)/10)
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
            while self.heur(tileCandidata, tfin) != 0:
                tilePosibles = self.getTileVecinas(tileSIG)
                tileCandidata = tilePosibles[0]
                for tile in tilePosibles:
                    if tile not in visitados:
                        #print(tile.centerx, tile.centery, tileAnt.centerx, tileAnt.centery)
                        if  tile != tileAnt:
                            #print(self.heur(tile,tfin), self.heur(tileCandidata,tfin))
                            if self.heur(tile,tfin) < self.heur(tileCandidata,tfin):
                                tileCandidata = tile
                path.append(tileCandidata)
                visitados.append(tileCandidata)
                tileAnt = tileSIG
                tileSIG = tileCandidata
                #print("Candidata elegida", tileCandidata.centerx, tileCandidata.centery)
        return path