 Cristal = tileClicked.ocupante
            tileIni = tileObj
            #calcular el camino a casa
            #print("Me quedo en:",tileObj.tileid)
            tileObj = tilesCasa[0]
            if(tilesCasa.__len__() > 1):
                for tile in tilesCasa:
                    if tile.heur(tileIni) < tileObj.heur(tileIni):
                        tileObj = tile
                tilesCasa.remove(tileObj)
            poStay = posIni
            self.mapa.setLibre(tileObj)
            pathA = self.mapa.Astar(tileIni,tileObj)
            posIni = (tileIni.centerx, tileIni.centery)
            #print(posIni)
            pathB = []
            #print(pathA.__len__())
            #Movernos al centro de la tile
            posFin = (tileIni.centerx, tileIni.centery)
            pathB.append(Path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]),
                    int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])), posFin))
            posAux = ()
            for tile in pathA:
                posFin = (tile.centerx, tile.centery)
                #print("desde: ",posIni,"hacia", posFin)
                path1 = Path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]),
                        int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])), posFin)
                #print("angulo del camino:", path1.angle)
                pathB.append(path1)
                posAux = posIni
                posIni = posFin

            angle = math.atan2(posFinal[1] - poStay[1], posFinal[0] - poStay[0])
            #print("angulo de minado", angle)
            #Y de casa a la mina tileObj casa y poStay la de minar
            tileFin = self.mapa.getTile(poStay[0],poStay[1])
            self.mapa.setLibre(tileFin)
            pathA = self.mapa.Astar(tileObj,tileFin)
            posIni = (tileObj.centerx, tileObj.centery)
            #print(posIni)
            pathC = []
            #print(pathA.__len__())
            #Movernos al centro de la tile
            posFin = poStay
            for tile in pathA:
                posFin = (tile.centerx, tile.centery)
                #print("desde: ",posIni,"hacia", posFin)
                path1 = Path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]),
                        int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])), posFin)
                #print("angulo del camino:", path1.angle, self.mapa.getTile(path1.posFin[0], path1.posFin[1]).tileid)
                pathC.append(path1)
                posIni = posFin

print(self.order['order'])
            if self.order != 0:
                if self.order['order'] == CommandId.TRANSPORTAR_ORE:
                    #sumar minerales al jugador
                    if self.cristal.capacidad < 0:
                        self.player.resources += self.cantidadMinada
                        print("cambiamos a still")
                        self.changeToStill()
                        del self.cristal
                    else:
                        self.order = {'order': CommandId.MINAR_BUCLE}
                        self.player.resources += self.cantidadMinada
                        self.paths = []
                        for path in self.cristalPath:
                            self.paths.append(path.copy())
                        self.changeToMove()
                elif self.order['order'] == CommandId.TRANSPORTAR_ORE_STILL:
                    #print("sumar minerales al jugador")
                    if self.cristal.capacidad < 0:
                        self.player.resources += self.minePower + self.cristal.capacidad
                        self.changeToStill()
                        del self.cristal
                    else:
                        self.player.resources += self.minePower
                        self.changeToStill()
                        del self.cristal
                elif self.order['order'] == CommandId.MINAR_BUCLE:
                    #sumar minerales al jugador         
                    self.changeToMining()