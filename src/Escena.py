import pygame, math
from . import Player, Command, Utils
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
    
    def setBasePlayer1(self, base1):
        self.basePlayer1 = base1
    
    def setBasePlayer2(self, base2):
        self.basePlayer2 = base2

    def procesarEvent(self, event):
        #command = pi.procesarEvent(event)
        #if map.check(command) and p1.check(command):
            #map.procesarCommand(command)
            #p1.procesarCommand(command)
        command = self.raton.processEvent(event, self.camera.x, self.camera.y)
        self.p1.processEvent(event)
        #for structure in p1.structures:
        #   structure.processEvent(event)
        relative_mouse_pos = pygame.mouse.get_pos()
        real_mouse_pos = (relative_mouse_pos[0] + self.camera.x, relative_mouse_pos[1] + self.camera.y)
        pathsForPlayer = []
        orderForPlayer = []
        if command.id == Command.CommandId.MOVER: # 1 es moverse
            for param in command.params:
                tileObj = self.mapa.getTile(real_mouse_pos[0], real_mouse_pos[1])
                posFinal = (tileObj.centerx, tileObj.centery)
                #print(tileObj.centery, tileObj.tileid)
                #print("pos final tile centro x e y: ", tileObj.centerx, tileObj.centery)
                tileIni = self.mapa.getTile(param[0], param[1])
                #print("pos ini tile centro x e y: ", tileIni.centerx, tileIni.centery)
                if tileObj.type != 0: #Esta ocupada
                    tileObj = self.mapa.getTileCercana(tileIni, tileObj)
                    #print(tileObj.centery, tileObj.tileid)
                now = datetime.now()
                pathA = self.mapa.Astar(tileIni,tileObj)
                #print((datetime.now() - now))
                posIni = (tileIni.centerx, tileIni.centery)
                #print(posIni)
                path = []
                #print(pathA.__len__())
                #Movernos al centro de la tile
                posFin = (tileIni.centerx, tileIni.centery)
                path.append(Utils.path(math.atan2(posFin[1] - param[1], posFin[0] - param[0]), int(math.hypot(posFin[0] - param[0], posFin[1] - param[1])), posFin))
                posAux = ()
                for tile in pathA:
                    posFin = (tile.centerx, tile.centery)
                    #print("desde: ",posIni,"hacia", posFin)
                    path1 = Utils.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)
                    #print("angulo del camino:", path1.angle)
                    path.append(path1)
                    posAux = posIni
                    posIni = posFin
                #print("Queria ir a", posFin, "y me han calculado", posIni)
                if posFinal == posIni:
                    #print("Entro a raton")
                    posIni = posAux
                    #print(path.__len__())
                    path.remove(path[path.__len__() - 1])
                    #print(path.__len__())
                    if path.__len__() > 0:

                        path.append(Utils.path(math.atan2(real_mouse_pos[1] - posIni[1], real_mouse_pos[0] - posIni[0]), int(math.hypot(real_mouse_pos[0] - posIni[0], real_mouse_pos[1] - posIni[1])),real_mouse_pos))
                
                #COMPROBAR QUE LA TILE CLICKADA CORRESPONDE A DISTINTAS ENTIDADES
                # COMPROBAR SI HA CLICKADO UN ORE
                tileCLikced = self.mapa.getTile(posFinal[0], posFinal[1])
                order = {'order': Command.CommandId.MOVER, 'angle': 0}
                if tileCLikced.type == 3:
                    Cristal = tileCLikced.ocupante
                    #calcular el camino a casa 
                    #print("Me quedo en:",posIni)
                    poStay = posIni 
                    tileIni = self.mapa.getTile(posIni[0], posIni[1])
                    baseRect = self.basePlayer1.getRect()
                    tileObj = self.mapa.getTile(baseRect.x + baseRect.w/2, baseRect.y + baseRect.h / 2)
                    #print("Centro de la base: ", tileObj.centerx, tileObj.centery)
                    tileObj = self.mapa.getTileCercana(tileIni, tileObj)
                    #print("La base esta en: ",tileObj.centerx, tileObj.centery)
                    self.mapa.setLibre(tileObj)
                    pathA = self.mapa.Astar(tileIni,tileObj)
                    posIni = (tileIni.centerx, tileIni.centery)
                    #print(posIni)
                    pathB = []
                    #print(pathA.__len__())
                    #Movernos al centro de la tile
                    posFin = (tileIni.centerx, tileIni.centery)
                    pathB.append(Utils.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])), posFin))
                    posAux = ()
                    for tile in pathA:
                        posFin = (tile.centerx, tile.centery)
                        #print("desde: ",posIni,"hacia", posFin)
                        path1 = Utils.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)
                        #print("angulo del camino:", path1.angle)
                        pathB.append(path1)
                        posAux = posIni
                        posIni = posFin

                    angle = math.atan2(posFinal[1] - poStay[1], posFinal[0] - poStay[0])
                    #Y de casa a la mina tileObj casa y poStay la de minar
                    tileFin = self.mapa.getTile(poStay[0],poStay[1])
                    pathA = self.mapa.Astar(tileObj,tileFin)
                    posIni = (tileObj.centerx, tileObj.centery)
                    #print(posIni)
                    pathC = []
                    #print(pathA.__len__())
                    #Movernos al centro de la tile
                    posFin = poStay
                    posAux = ()
                    for tile in pathA:
                        posFin = (tile.centerx, tile.centery)
                        #print("desde: ",posIni,"hacia", posFin)
                        path1 = Utils.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)
                        #print("angulo del camino:", path1.angle)
                        pathC.append(path1)
                        posAux = posIni
                        posIni = posFin

                    order = {'order': Command.CommandId.MINAR, 'angle': angle,'basePath': pathB, 'cristal': Cristal,'cristalPath': pathC }
                    orderForPlayer.append(order)


                else:
                    orderForPlayer.append(order)
                pathsForPlayer.append(path)
            self.p1.execute(Command.CommandId.MOVER, pathsForPlayer)
            self.p1.execute(Command.CommandId.ORDENAR, orderForPlayer)
                
        pass
    def checkPressedButtons(self):
        key = pygame.key.get_pressed()
        if key[self.p1.commandMap[Command.CommandId.MOVER_CAMARA_ARRIBA]]:
            self.camera.moverArriba()
        if key[self.p1.commandMap[Command.CommandId.MOVER_CAMARA_ABAJO]]:
            self.camera.moverAbajo(self.mapa.h)
        if key[self.p1.commandMap[Command.CommandId.MOVER_CAMARA_IZQUIERDA]]:
            self.camera.moverIzquierda()
        if key[self.p1.commandMap[Command.CommandId.MOVER_CAMARA_DERECHA]]:
            self.camera.moverDerecha(self.mapa.w)

    def checkUnHoldButton(self, key):
        if self.p1.commandMap[Command.CommandId.ROTAR] == key:
            for unit in self.p1.unitsSelected:
                #print(unit.getRect().x - unit.getRect().w,unit.getRect().y - unit.getRect().h)
                unit.dir = (unit.dir + 1)%16

    def update(self):
        units = self.p1.units + self.p2.units
        for unit in units:
            unitPos = unit.getPosition()
            tileActual = self.mapa.getTile(unitPos[0], unitPos[1])
            if unit.paths.__len__() > 0:
                path = unit.paths[0]
                pathObj = unit.paths[unit.paths.__len__() - 1]
                tilePath = self.mapa.getTile(path.posFin[0],path.posFin[1])
                tileObj = self.mapa.getTile(pathObj.posFin[0],pathObj.posFin[1])
                if tilePath.type != 2 or ((tilePath.id == unit.id) and (tilePath.type == 2)):
                    dirX = math.cos(path.angle)
                    dirY = math.sin(path.angle)
                    tileSiguiente = self.mapa.getTile(int(unitPos[0] + dirX*unit.speed + 0.5), int(unitPos[1] + dirY*unit.speed + 0.5))
                    #print(unitPos)
                    #input()
                    #print("tileActual: ", tileActual.centerx, tileActual.centery, "tileSiguiente",int(unitPos[0] + dirX*unit.speed + 0.5),tileSiguiente.centerx,int(unitPos[1] + dirY*unit.speed + 0.5), tileSiguiente.centery)
                    #input()
                    if tileActual != tileSiguiente :
                        #print("es de este tipo, ", tileActual.type)
                        if tileActual.type != 1 and tileActual.type != 3:
                            self.mapa.setLibre(tileActual)
                            if tileSiguiente.type != 1 and tileSiguiente.type != 3:
                                self.mapa.setVecina(tileSiguiente, unit.id)
                                tileSiguiente.setOcupante(unit)
                    else:
                        if tileActual.type != 1 and tileActual.type != 3:
                            self.mapa.setVecina(tileActual, unit.id)
                            tileActual.setOcupante(unit)
                    tiles = self.mapa.getAllTileVecinas(tileActual)
                    for tile in tiles:
                            self.mapa.setLibre(tile)
                else:

                    #print("Que me la han ocupao",tilePath.tileid ,"y yo estando en",tileActual.tileid,unit.id )
                    #input()
                    #if tilePath == tileObj:
                     #   #print("Y ademas mi objetivo, me miro otro que no sea", tileObj.centerx, tileObj.centery)
                      #  tileObj = self.mapa.calcDest(tileActual.centerx,tileActual.centery,tileObj.centerx,tileObj.centery) #Obtengo una cercana al objetivo
                       # #print("Mi nuevo objetivo es", tileObj.centerx, tileObj.centery)
                    if tilePath.tileid != tileObj.tileid: #No es mi objetivo pero esta ocupado
                        for unitBlock in units:
                            if unitBlock.id == tilePath.id: #Estamos con la unidad bloqueante
                                if unitBlock.paths.__len__() == 0: # ME bloquea y ademas no se mueve
                                    #print("Me bloque y no se mueve el tio")
                                    pathA = self.mapa.Astar(tileActual,tileObj)
                                    param = unitBlock.getPosition()
                                    posFinalT = unit.paths[unit.paths.__len__() - 1].posFin
                                    path = []
                                    posFin = (tileActual.centerx, tileActual.centery)
                                    path.append(Utils.path(math.atan2(posFin[1] - param[1], posFin[0] - param[0]), int(math.hypot(posFin[0] - param[0], posFin[1] - param[1])), posFin))
                                    posIni = posFin
                                    for tile in pathA:
                                        posFin = (tile.centerx, tile.centery)
                                        #print("desde: ",posIni,"hacia", posFin)
                                        path1 = Utils.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)
                                        #print("angulo del camino:", path1.angle)
                                        path.append(path1)
                                        posAux = posIni
                                        posIni = posFin
                                    posFin = (tileObj.centerx, tileObj.centery)
                                    #print("Queria ir a", posFin, "y me han calculado", posIni)
                                    if posFin == posIni:
                                        #print("Entro a raton")
                                        posIni = posAux
                                        #print(path.__len__())
                                        path.remove(path[path.__len__() - 1])
                                        #print(path.__len__())
                                        if path.__len__() > 0:
                                            path.append(Utils.path(math.atan2(posFinalT[1] - posIni[1], posFinalT[0] - posIni[0]), int(math.hypot(posFinalT[0] - posIni[0], posFinalT[1] - posIni[1])),posFinalT))
                                    unit.paths = path
                                else: #Es majo y se va a mover
                                    posiblesAlt = self.mapa.getTileVecinas(tileActual)
                                    newTilePath = posiblesAlt[0]
                                    for tile in posiblesAlt:
                                        #print(tilePath.tileid, tileObj.tileid, tile.tileid)
                                        if tilePath.tileid == tileObj.tileid and tile.tileid != tileObj.tileid:
                                            newTilePath = tile
                                            break
                                        if (newTilePath.heur(tileActual) > tile.heur(tileActual) and tile.tileid != tileActual.tileid) or (newTilePath.heur(tileActual) <= tile.heur(tileActual) and tile.tileid != tileActual.tileid):
                                            newTilePath = tile
                                    #print("Salgo", newTilePath.tileid, tileActual.tileid)
                                    #for path in unit.paths:
                                        #print(path.posFin)
                                    #print("aaaaaaaaaaaaaaaaaaaaaaa")
                                    unit.paths.pop(0)

                                    # Nos colocamos en la central
                                    posIni = unitPos
                                    posFin = (tileActual.centerx,tileActual.centery)
                                    path1 = Utils.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)
                                    unit.paths.insert(0,path1)
                                    #for path in unit.paths:
                                        #print(path.posFin)
                                    #print("aaaaaaaaaaaaaaaaaaaaaaa")

                                    #Irnos a la nueva
                                    posIni = posFin
                                    posFin = (newTilePath.centerx, newTilePath.centery)
                                    path1 = Utils.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)
                                    unit.paths.insert(1,path1)
                                    #for path in unit.paths:
                                        #print(path.posFin)
                                    #print("aaaaaaaaaaaaaaaaaaaaaaa")
                                    #Conectarla con la ocupada
                                    if unit.paths.__len__() > 2:
                                        #print("ENTRO ACA")
                                        #unit.paths.pop(2)
                                        posIni = posFin
                                        posFin = (tilePath.centerx, tilePath.centery)
                                        path1 = Utils.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)
                                        unit.paths.insert(2,path1)
                                        #for path in unit.paths:
                                            #print(path.posFin)
                                    #print("aaaaaaaaaaaaaaaaaaaaaaa")
                    else: #La siguiente es mi objetivo
                        #print("La siguiente es mi objetivo")
                        unit.paths = []
            else:
                if tileActual.type != 1:
                    self.mapa.setVecina(tileActual, unit.id)
        for unit in self.p1.structures + self.p2.structures:
            unitPos = unit.getPosition()
            tileActual = self.mapa.getTile(unitPos[0], unitPos[1])
            if unit.paths.__len__() > 0:
                path = unit.paths[0]
                pathObj = unit.paths[unit.paths.__len__() - 1]
                tilePath = self.mapa.getTile(path.posFin[0],path.posFin[1])
                ##print("Tilepath es: ", tilePath.centerx, tilePath.centery)
                tileObj = self.mapa.getTile(pathObj.posFin[0],pathObj.posFin[1])
                if tilePath.type != 2 or (tilePath.id == unit.id and tilePath.type == 2):
                    dirX = math.cos(path.angle)
                    dirY = math.sin(path.angle)
                    tileSiguiente = self.mapa.getTile(unitPos[0] + dirX*unit.speed, unitPos[1] + dirY*unit.speed)
                    if tileActual != tileSiguiente :
                        if tileActual.type != 1:
                            self.mapa.setLibre(tileActual)
                            if tileSiguiente.type != 1:
                                self.mapa.setVecina(tileSiguiente, unit.id)
                    else:
                        if tileActual.type != 1:
                            self.mapa.setVecina(tileActual, unit.id)
            else:
                if tileActual.type != 1:
                    rect = unit.getRect()
                    x = self.mapa.getTile(rect.x, rect.y).centerx
                    y = self.mapa.getTile(rect.x, rect.y).centery
                    finx = self.mapa.getTile(x + rect.w, y + rect.h).centerx
                    finy = self.mapa.getTile(x + rect.w, y + rect.h).centery
                    
                    while x <= finx:
                        while y <= finy:
                            #print(int(x/40), int(y/40))
                            tile = self.mapa.getTile(x,y)
                            self.mapa.setVecina(self.mapa.getTile(x,y), unit.id)
                            self.mapa.getTile(x,y).setOcupante(unit)
                            y = y + 20
                        y = self.mapa.getTile(rect.x, rect.y).centery
                        x = x + 20
        for res in self.resources:
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


        self.p1.update()
        self.p2.update()
        self.raton.update(self.camera)
        self.aI.make_commands()

    def draw(self, screen):
        self.mapa.drawMap2(screen, self.camera)
        self.p1.draw(screen, self.camera)
        self.p2.draw(screen, self.camera)
        self.raton.draw(screen, self.camera)
        self.interfaz.draw(screen)
        for res in self.resources:
            r = res.getRect()
            pygame.draw.rect(screen, Utils.BLACK, pygame.Rect(r.x - self.camera.x, r.y  - self.camera.y, r.w, r.h),1)
            if (r.x + r.w >= self.camera.x and r.x <= self.camera.x + self.camera.w and
            r.y + r.h >= self.camera.y and r.y <= self.camera.y + self.camera.h):
                drawPos = res.getDrawPosition()
                if res.clicked:
                    pygame.draw.ellipse(screen, Utils.GREEN, [r.x - self.camera.x, r.y + (0.7*r.h)- self.camera.y,r.w , 0.3*r.h], 2)
                #screen.blit(unit.image, [r.x - self.camera.x, r.y - self.camera.y])
                screen.blit(res.image, [drawPos[0] - self.camera.x, drawPos[1] - self.camera.y])
