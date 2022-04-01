
SCREEN_WIDTH = 7*40
SCREEN_HEIGHT = 7*40

def mismoId(list, tileB):
    tileReturn = Tile(-1,0,0,0,0,0)
    for tile in list:
        if tile.id == tileB.id:
            tileReturn = tile
    return tileReturn

class Tile():
    def __init__(self, id, x, y, w, h, type):
        self.type = type
        self.id = id
        self.centerx = int(x + w/2)
        self.centery = int(y + h/2)
        self.g = 0
        self.padre = ()
    
    def heur(self,  tfin):
        return (tfin.centerx - self.centerx)*(tfin.centerx - self.centerx) + (tfin.centery - self.centery)*(tfin.centery - self.centerx)
class Map():
    def __init__(self, h, w):
        self.tw = 40
        self.th = 40
        self.map = []
        if h > w:
            for i in range(h):
                for j in range(w):
                    print("a:", i*w + j)
        else:
            for i in range(h):
                for j in range(w):
                    print("a:", i*w + j)

        for i in range(h):
            self.map.insert(i,[])#Es una matriz que representa el mapa(0 es suelo, 1 es obstaculo, 2 vecino)
            for j in range(w):
                tile = Tile(i*(h-1) + j,self.tw * j, self.th * i, self.tw, self.th, 0)
                self.map[i].insert(j,tile)
                #print(tile.id)
    #Devuelve la Tile que se encuentra en las coordenadas x,y
    def getTile(self, x, y):
        xaux = x
        yaux = y
        #print(x, y)
        if x >= SCREEN_WIDTH:
            xaux = SCREEN_WIDTH-1
        if y >= SCREEN_HEIGHT:   
            yaux = SCREEN_HEIGHT-1
            
        return self.map[int(yaux/self.th)][int(xaux/self.tw)]
    #Pone a true las Tiles del rectangulo que forman x,y,w,h
    def addObstacle(self, x,y,w,h):
        for i in range(h): #Recorro el mapa  por las filas
            for j  in range(w): #En la fila i recorro las columnas
                self.map[i+int(y/self.th)][j+int(x/self.tw)].type = 1

    def setTileG(self, tile, g):
        self.map[int(tile.centery/self.th)][int(tile.centerx/self.tw)].g = g
    def setTilePadre(self, tile, padre):
        self.map[int(tile.centery/self.th)][int(tile.centerx/self.tw)].padre = padre
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

    def Astar(self, tileIni, tileObj):
        nodosAbiertos = []
        nodosCerrados = []
        nodosAbiertos.append(tileIni)
        while tileObj not in nodosCerrados and nodosAbiertos.__len__() != 0:
            currentTile = nodosAbiertos[0]
            currentF = currentTile.g + currentTile.heur(tileObj)

            for tile in nodosAbiertos:           
                tileF = tile.g + tile.heur(tileObj)
                print(currentTile.id + 1,":", currentF,tile.id + 1,":", tileF)
                if currentF > tileF:
                    currentTile = tile
            #Tenemos la tile con menos f
            nodosCerrados.append(currentTile)
            nodosAbiertos.remove(currentTile)
            input()
            print("estamos en", currentTile.id + 1)
            for tile in self.getTileVecinas(currentTile):
                if mismoId(nodosCerrados,tile).id == -1:# No esta
                    tileEnAbiertos = mismoId(nodosAbiertos,tile)
                    if  tileEnAbiertos.id == -1: #No esta
                        tile.g = currentTile.g + 1
                        print(tile.id,":",tile.g)
                        nodosAbiertos.append(tile)
                        self.setTileG(tile, tile.g)
                        self.setTilePadre(tile, currentTile)
                        tile.padre = currentTile
                    else:
                        if tileEnAbiertos.g > tile.g:
                            nodosAbiertos.remove(tileEnAbiertos)
                            nodosAbiertos.append(tile)
                            tile.padre = currentTile
                            tile.g = currentTile.g + 1
                            self.setTileG(tile, tile.g)
                            self.setTilePadre(tile, currentTile)
        if nodosAbiertos.__len__() == 0:
            print("camino no encontrado")
        else:
            currentTile = self.getTile(tileObj.centerx,tileObj.centery)
            while currentTile != tileIni:
                print(currentTile.id + 1)
                currentTile = currentTile.padre
            print(currentTile.id + 1)

mapa = Map(7, 7)
mapa.addObstacle(2*41,1*41,4,1)
mapa.addObstacle(5*41,1*41,1,3)

mapa.Astar(mapa.getTile(1*40,5*40),mapa.getTile(6*40,0))

                    








            