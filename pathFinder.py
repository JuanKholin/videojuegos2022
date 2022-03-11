import pygame, sys, random, time
import math

pygame.init()

# Definir colores

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

size =(SCREEN_WIDTH,SCREEN_HEIGHT)

def collides(rect1, rect2):
    print("RECTANGULO 1", rect1.x, rect1.y, rect1.w, rect1.h)
    print("RECTANGULO 2", rect2.x, rect2.y, rect2.w, rect2.h)
    if (rect1.x + rect1.w) >= rect2.x and  (rect1.x + rect1.w) <= (rect2.x + rect2.w) and (rect1.y + rect1.h) >= rect2.y and  (rect1.y + rect1.h) <= (rect2.y + rect2.h):
        return True
    if (rect1.x + rect1.w) >= rect2.x and  (rect1.x + rect1.w) <= (rect2.x + rect2.w) and (rect1.y + rect1.h) >= rect2.y and  rect1.y <= (rect2.y + rect2.h):
        return True
    if rect1.x >= rect2.x and  rect1.x <= (rect2.x + rect2.w) and rect1.y >= rect2.y and  rect1.y <= (rect2.y + rect2.h):
        return True
    if rect1.x >= rect2.x and  rect1.x <= (rect2.x + rect2.w) and (rect1.y + rect1.h) >= rect2.y and  (rect1.y + rect1.h) <= (rect2.y + rect2.h):
        return True
    return False
class rect():
    def __init__(self):
        pass
    def setDim(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class path():
    def __init__(self, angle, dist):
        self.angle = angle
        self.dist = dist
    

class Terran():
    def __init__(self, speed, xini, yini, sprites, id):
        super().__init__()
        #ATRIBUTOS
        self.paths = []
        self.id = id
        self.rectOffY = 8
        self.clicked = False
        self.angle = 0
        self.speed = speed
        self.face = 8
        self.frame = 6
        self.framesToRefresh = 5
        self.count = 0
        self.sprites = []
        self.dirX = 0
        self.dirY = 0
        self.distanceToPoint = 0


        #INICIALIZACION DE LOS MISMOS
        for i in range(16):
            self.sprites.insert(i,[])
        for i in range(72):
            if i < 10:
                nPath = "0" + str(i)
            else:
                nPath = i
            if i%9 != 0 and i%9 != 8:
                self.sprites[16-(i%9)].insert(int(i/9),pygame.transform.flip(pygame.image.load(sprites + "/tile0" + str(nPath) + ".png"),True,False))
            self.sprites[i%9].insert(int(i/9),pygame.image.load(sprites + "/tile0" + str(nPath) + ".png"))
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(WHITE)
        self.rectn = rect()
        self.rectn.w = self.image.get_width()
        self.rectn.h = self.image.get_height() - self.rectOffY
        self.rectn.x = xini
        self.rectn.y = yini

        self.prevX = self.rectn.x
        self.prevY = self.rectn.y

    def isClicked(self):
        return self.clicked
    def setClicked(self, click):
        self.clicked = click
    def update(self):
        self.image = self.sprites[self.face][self.frame]
        self.image.set_colorkey(WHITE)
        self.resize()
        if self.paths.__len__() > 0:
            actualPath = self.paths[0]
            if actualPath.dist > 0:
                if actualPath.angle < 0:
                        self.angle = -actualPath.angle
                else:
                    self.angle = 2*math.pi - actualPath.angle
                self.dirX = math.cos(actualPath.angle)
                self.dirY = math.sin(actualPath.angle)
                distrec = math.hypot((self.rectn.x + self.dirX*self.speed) - self.rectn.x, (self.rectn.y + self.dirY*self.speed) - self.rectn.y)
                actualPath.dist -= distrec
                
                
                self.rectn.x += self.dirX*self.speed
                self.rectn.y += self.dirY*self.speed
                #print(self.rectn.x, self.rectn.y)

                self.face = int(4 - (self.angle*8/math.pi))%16
                self.count += 1
                if self.count >= self.framesToRefresh:
                    self.frame = (self.frame + 1)%8
                    self.count = 0
            else:
                print("SE ACABO EL CAMINO", self.angle, actualPath.angle)
                #print(self.rectn.x, self.rectn.y)
                self.paths.remove(actualPath)
                if self.paths.__len__() == 0:
                    self.frame = 6
                    self.face = 8
            
                
                
    def resize(self):
        self.rectn.x -= self.rectn.w
        self.rectn.y -= self.rectn.h
        self.image = pygame.transform.scale2x(self.image)
        self.rectn.w = self.image.get_width()
        self.rectn.h = self.image.get_height() - self.rectOffY
        self.rectn.x += self.rectn.w
        self.rectn.y += self.rectn.h
    
    def getRect(self):
        rectAux = rect()
        rectAux.x = self.rectn.x - self.rectn.w/2
        rectAux.y = self.rectn.y - self.rectn.h
        rectAux.w = self.rectn.w
        rectAux.h = self.rectn.h
        return rectAux
    
    def cancel(self):
        self.distanceToPoint = 0
    
    def addPath(self,path):
        self.paths.append(path)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
 

screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()




units = []
unitsClicked = []


class Tile():
    def __init__(self, x, y, h, w, type):
        self.centerx = int(x + w/2)
        self.centery = int(y + h/2)
        self.h = h
        self.w = w
        self.type = type 
    
    def getRect(self):
        return (int(self.centerx - self.w/2) ,int(self.centery - self.h/2), self.w, self.h)


#Inicializo el mapa

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
    def drawMap(self):
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
        return self.map[int(y/self.th)][int(x/self.tw)]


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


    def calcPath(self, xini, yini, xfin, yfin):
        path = []
        tactual = self.getTile(xini, yini)
        tfin = self.getTile(xfin, yfin)
        print("Distancia a la tile final",tactual.centerx, tactual.centery, tfin.centerx, tfin.centery)
        if self.heur(tactual, tfin) != 0:
            tilePosibles = self.getTileVecinas(tactual)
            tileCandidata = tilePosibles[0]
            tileSIG = tactual
            tileAnt = tactual
            while self.heur(tileCandidata, tfin) != 0:
                tilePosibles = self.getTileVecinas(tileSIG)
                tileCandidata = tilePosibles[0]
                for tile in tilePosibles:
                    print(tile.centerx, tile.centery, tileAnt.centerx, tileAnt.centery)
                    if  tile != tileAnt:
                        #print(self.heur(tile,tfin), self.heur(tileCandidata,tfin))
                        if self.heur(tile,tfin) < self.heur(tileCandidata,tfin):
                            tileCandidata = tile
                path.append(tileCandidata)
                tileAnt = tileSIG
                tileSIG = tileCandidata
                print("Candidata elegida", tileCandidata.centerx, tileCandidata.centery)
        return path





units.append(Terran(2, 200,200,"terranSprites",1))
#units.append(Terran(2, 100,50,"terranSprites",2))
#units.append(Terran(2, 300,50,"terranSprites",3))
#units.append(Terran(2, 50,100,"terranSprites",4))
#units.append(Terran(2, 100,200,"terranSprites",5))
#units.append(Terran(2, 300,300,"terranSprites",6))

map = Map(10,20)
map.addObstacle(240,40,3,3)
map.addObstacle(240,240,3,3)
map.addObstacle(400,160,3,3)
map.addObstacle(100,160,3,3)


def calcPointsRound(mouse_pos):
    pointsRound = []
    pointsRound.append(mouse_pos)
    pos = (mouse_pos[0] - 40, mouse_pos[1])
    pointsRound.append(pos)
    pos = (mouse_pos[0] + 40, mouse_pos[1])
    pointsRound.append(pos)
    pos = (mouse_pos[0] - 20, mouse_pos[1] - 20)
    pointsRound.append(pos)
    pos = (mouse_pos[0] - 20, mouse_pos[1] + 20)
    pointsRound.append(pos)
    pos = (mouse_pos[0] + 20, mouse_pos[1] + 20)
    pointsRound.append(pos)
    pos = (mouse_pos[0] + 20, mouse_pos[1] - 20)
    pointsRound.append(pos)
    return pointsRound
    
while True:
    rectM = rect()

    for event in pygame.event.get(): #Identificar lo sucedido en la ventana
        #print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_type = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            rectM.x = mouse_pos[0]
            print(rectM.x)
            rectM.y = mouse_pos[1]
            print(rectM.y)
            rectM.h = 1
            rectM.w = 1
            if click_type[0]:
                unitClicked = False
                for terran in units:
                    if collides(rectM, terran.getRect()):
                        unitClicked = True
                        if not terran.isClicked():
                            terran.setClicked(True)
                            unitsClicked.append(terran)
                            print("CLICKADO" + str(terran.id))
                        else:
                            terran.setClicked(False)
                            unitsClicked.remove(terran)
                            print("DESCLICKADO" + str(terran.id))
                        
                if unitClicked:
                    for terran in unitsClicked:
                        terran.setClicked(True)
                        print("Mantenemos a " + str(terran.id))
                else:
                    for terran in units:
                        terran.setClicked(False)
                        if terran in unitsClicked:
                            unitsClicked.remove(terran)
                        print("DESCLICKADO" + str(terran.id))
            if click_type[2]:
                print("CALCULANDO PUNTOS")
                points = calcPointsRound(mouse_pos)
                for terran in unitsClicked:
                    pathA = map.calcPath(terran.rectn.x,terran.rectn.y,mouse_pos[0],mouse_pos[1])
                    tileIni = map.getTile(terran.rectn.x,terran.rectn.y)
                    posIni = (tileIni.centerx, tileIni.centery)
                    for tile in pathA:
                        posFin = (tile.centerx, tile.centery)
                        path1 = path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])))
                        terran.paths.append(path1)
                        posIni = posFin
                
        if event.type == pygame.KEYDOWN:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_c]:
                for terran in unitsClicked:
                    print("CANCELADO" + str(terran.id))
                    terran.cancel()
                
            

    
    ###---LOGICA
    #Actualizar objetos



    
    
    #Poner color de fondo
    screen.fill(WHITE)
    for terran in units:
        ###---LOGICA
        terran.update()


        r = terran.getRect()
        map.drawMap()
        pygame.draw.rect(screen, BLACK, pygame.Rect(r.x, r.y, r.w, r.h),1)
        screen.blit(terran.image, [r.x, r.y])

    
    ###--- ZONA DE DIBUJO


    ###--- ZONA DE DIBUJO

    #ACtualizar pantalla
    pygame.display.flip()
    clock.tick(60)

