import pygame, math
from . import Player, Command, Utils, Raton
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
        #Conseguir el comando
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            command = self.raton.processEvent(event, self.camera.x, self.camera.y)
        else:
            command = self.p1.processEvent(event)

        #ejecutar el comando
        if command.id == Command.CommandId.GENERAR_UNIDAD:
            self.p1.execute(command.id, [])
        elif command.id == Command.CommandId.MOVER: # 1 es moverse
            relative_mouse_pos = pygame.mouse.get_pos()
            real_mouse_pos = (relative_mouse_pos[0] + self.camera.x, relative_mouse_pos[1] + self.camera.y)
            pathsForPlayer = []
            orderForPlayer = []
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
                order = {'order': Command.CommandId.MOVER, 'angle': 0, 'path': path}
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

                    order = {'order': Command.CommandId.MINAR, 'angle': angle,'basePath': pathB, 'cristal': Cristal,'cristalPath': pathC, 'path': path }


                else:
                    rectClicked = Raton.createRect(tileCLikced.centerx,tileCLikced.centery,tileCLikced.centerx + 1, tileCLikced.centery + 1)
                    for struct in self.p1.structures:
                        if Raton.collideRect(struct.getRect(), rectClicked):
                            order = struct.getOrder()
                            order = {'order': order,'path': path}
                pathsForPlayer.append(path)
                orderForPlayer.append(order)
            #self.p1.execute(Command.CommandId.MOVER, pathsForPlayer)
            for pat in path:
                print(self.mapa.getTile(pat.posFin[0],pat.posFin[1]).tileid)
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
        #Recorremos las unidades de los jugadores para detectar colisiones
        for unit in units:
            self.updateUnit(unit, units)
        for structure in self.p1.structures + self.p2.structures:
            self.updateStructure(structure)
        for res in self.resources:
            self.updateResource(res)

        self.p1.update()
        self.p2.update()
        self.raton.update(self.camera)
        self.aI.make_commands()

    def updateUnit(self, unit, units):
        #OBTENEMOS LA TILE EN LA QUE SE ENCUENTRAN
        unitPos = unit.getPosition()
        tileActual = self.mapa.getTile(unitPos[0], unitPos[1])

        #SI ESTA MOVIENDOSE HAY QUE CALCULAR COLISIONES Y CAMBIAR LAS TILES QUE OCUPAN
        if unit.paths.__len__() > 0:

            #CON POSFIN DEL PATH ACTUAL Y EL PATH FINAL(OBJETIVO) CALCULO LAS TILES DE LA SIGUIENTE Y OBJETIVO
            path = unit.paths[0]
            pathObj = unit.paths[unit.paths.__len__() - 1]
            tilePath = self.mapa.getTile(path.posFin[0],path.posFin[1])
            tileObj = self.mapa.getTile(pathObj.posFin[0],pathObj.posFin[1])

            #SI LA SIGUIENTE NO ESTA OCUPADA HAY QUE ACTUALIZAR LAS TILES
            if tilePath.type != 2 or ((tilePath.id == unit.id) and (tilePath.type == 2)):
                dirX = math.cos(path.angle)
                dirY = math.sin(path.angle)
                tileSiguiente = self.mapa.getTile(int(unitPos[0] + dirX*unit.speed + 0.5), int(unitPos[1] + dirY*unit.speed + 0.5))
                #print(unitPos)
                ###input()
                #print("tileActual: ", tileActual.centerx, tileActual.centery, "tileSiguiente",int(unitPos[0] + dirX*unit.speed + 0.5),tileSiguiente.centerx,int(unitPos[1] + dirY*unit.speed + 0.5), tileSiguiente.centery)
                ###input()
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
                    if tile.type != 1:
                        self.mapa.setLibre(tile)
            else:
                    
                ###input()
                #if tilePath == tileObj:
                    #   #print("Y ademas mi objetivo, me miro otro que no sea", tileObj.centerx, tileObj.centery)
                    #  tileObj = self.mapa.calcDest(tileActual.centerx,tileActual.centery,tileObj.centerx,tileObj.centery) #Obtengo una cercana al objetivo
                    # #print("Mi nuevo objetivo es", tileObj.centerx, tileObj.centery)

                #LA TILE SIGUIENTE ESTA OCUPADA
                print("Que me la han ocupao",tilePath.tileid ,"y yo estando en",tileActual.tileid, "Quiero ir a:", tileObj.tileid )
                #No es mi objetivo pero esta ocupado
                if tilePath.tileid != tileObj.tileid: 
                    for unitBlock in units:
                        if unitBlock.id == tilePath.id: #Estamos con la unidad bloqueante
                            if unitBlock.paths.__len__() == 0: # ME bloquea y ademas no se mueve
                                print("Me bloque y no se mueve el tio")
                                pathA = self.mapa.Astar(tileActual,tileObj)
                                param = unitBlock.getPosition()
                                posFinalT = unit.paths[unit.paths.__len__() - 1].posFin
                                path = []
                                posIni = (tileActual.centerx, tileActual.centery)
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
                                for path in unit.paths:
                                    print("CAMINO: ", self.mapa.getTile(path.posFin[0],path.posFin[1]).tileid)
                            else: #Es majo y se va a mover
                                print("Es majo y se va a mover")
                                #CALCULAR LA TILE MAS ADECUADA
                                bestTile = self.mapa.getTileVecinaCercana(tileObj,tileActual)
                                print("MEJOR TILE: ", bestTile.tileid)
                                #NO TIENE A DONDE IR
                                if bestTile.tileid == -1:
                                    unit.paths = []
                                else:
                                    if bestTile.heur(tileObj) > tileActual.heur(tileObj):
                                        print("Me tengo que replegar por lo que mejor recalculo")
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
                                    else: #HACEMOS EL CAMBIO A LOS PATHS
                                        for path in unit.paths:
                                            print(self.mapa.getTile(path.posFin[0],path.posFin[1]).tileid)
                                        unit.paths.pop(0) #quitamos el path a la ocupada
##input()
                                        for path in unit.paths:
                                            print(self.mapa.getTile(path.posFin[0],path.posFin[1]).tileid)
                                        #CAMINO A LA MEJOR TILE
                                        posFin = (bestTile.centerx, bestTile.centery)
                                        posIni = unit.getPosition()
                                        path1 = Utils.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)

                                        unit.paths.insert(0, path1)
##input()
                                        for path in unit.paths:
                                            print(self.mapa.getTile(path.posFin[0],path.posFin[1]).tileid)

                                        #CAMINO A LA TILE DESOCUPADA
                                        posIni = posFin
                                        posFin = (tilePath.centerx, tilePath.centery)
                                        path1 = Utils.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])),posFin)

                                        unit.paths.insert(1, path1)
##input()
                                        for path in unit.paths:
                                            print(self.mapa.getTile(path.posFin[0],path.posFin[1]).tileid, path.angle)
##input()
                else: #La siguiente es mi objetivo
                    unit.paths = []
        else:
            if tileActual.type != 1:
                self.mapa.setVecina(tileActual, unit.id)

    def updateStructure(self, structure):
        unitPos = structure.getPosition()
        tileActual = self.mapa.getTile(unitPos[0], unitPos[1])
        if structure.paths.__len__() > 0:
            path = structure.paths[0]
            pathObj = structure.paths[structure.paths.__len__() - 1]
            tilePath = self.mapa.getTile(path.posFin[0],path.posFin[1])
            ##print("Tilepath es: ", tilePath.centerx, tilePath.centery)
            tileObj = self.mapa.getTile(pathObj.posFin[0],pathObj.posFin[1])
            if tilePath.type != 2 or (tilePath.id == structure.id and tilePath.type == 2):
                dirX = math.cos(path.angle)
                dirY = math.sin(path.angle)
                tileSiguiente = self.mapa.getTile(unitPos[0] + dirX*structure.speed, unitPos[1] + dirY*structure.speed)
                if tileActual != tileSiguiente :
                    if tileActual.type != 1:
                        self.mapa.setLibre(tileActual)
                        if tileSiguiente.type != 1:
                            self.mapa.setVecina(tileSiguiente, structure.id)
                else:
                    if tileActual.type != 1:
                        self.mapa.setVecina(tileActual, structure.id)
        else:
            if tileActual.type != 1:
                rect = structure.getRect()
                x, y = self.mapa.getTileIndex(rect.x, rect.y)
                while y*self.mapa.th <= rect.y+rect.h:
                    x, _ = self.mapa.getTileIndex(rect.x, rect.y)
                    while x*self.mapa.tw <= rect.x+rect.w:
                        tile = self.mapa.map[y][x]
                        self.mapa.setVecina(tile, structure.id)
                        tile.setOcupante(structure)
                        x += 1
                    y += 1

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
        self.mapa.drawMap(screen, self.camera)
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
