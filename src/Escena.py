import pygame

class Escena():
    def __init__(self, p1, p2, ia, mapa, camera):
        self.p1 = p1
        self.p2 = p2
        self.ia = ia
        self.mapa = mapa 
        self.camera = camera

    def __init__(self):
        pass

    def procesarEvent(self, event):
        #command = pi.procesarEvent(event)
        #if map.check(command) and p1.check(command):
            #map.procesarCommand(command)
            #p1.procesarCommand(command)
        command = p1.proccesEvent(event)
        if command.id == MOVER:
            for param in command.params:
                pathA = map.calcPath(param[0],terran.rectn.y,mouse_pos[0],mouse_pos[1])
                tileIni = map.getTile(terran.rectn.x,terran.rectn.y)
                posIni = (tileIni.centerx, tileIni.centery)
                terran.paths = []
                for tile in pathA:
                    posFin = (tile.centerx, tile.centery)
                    path1 = Terran.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])))
                    terran.paths.append(path1)
                    posIni = posFin     
        pass

    def update():
        mapa.update()
        p1.update()
        p2.update()
    
    def draw(screen):
        mapa.drawMap(screen)
        p1.draw(screen)
        p2.draw(screen)
