import pygame, math
from . import Player, Command

class Escena():
    def __init__(self, p1, p2, ia, mapa, camera, raton):
        self.p1 = p1
        self.p2 = p2
        self.ia = ia
        self.mapa = mapa 
        self.camera = camera
        self.raton = raton



    def procesarEvent(self, event):
        #command = pi.procesarEvent(event)
        #if map.check(command) and p1.check(command):
            #map.procesarCommand(command)
            #p1.procesarCommand(command)
        command = self.raton.processEvent(event)
        self.raton.processEvent(event)
        mouse_pos = pygame.mouse.get_pos()
        pathsForPlayer = []
        if command.id == Command.CommandId.MOVER: # 1 es moverse
            for param in command.params:
                pathA = self.mapa.calcPath(param[0],param[1],mouse_pos[0],mouse_pos[1])
                tileIni = self.mapa.getTile(param[0],param[1])
                posIni = (tileIni.centerx, tileIni.centery)
                path = []
                for tile in pathA:
                    posFin = (tile.centerx, tile.centery)
                    path1 = Player.path(math.atan2(posFin[1] - posIni[1], posFin[0] - posIni[0]), int(math.hypot(posFin[0] - posIni[0], posFin[1] - posIni[1])))
                    path.append(path1)
                    posIni = posFin
                pathsForPlayer.append(path)
            print(pathsForPlayer.__len__())
            self.p1.execute(Command.CommandId.MOVER, pathsForPlayer)
                     
        pass

    def update(self):
        self.p1.update()
        self.raton.update()
    
    def draw(self, screen):
        self.mapa.drawMap(screen)
        self.p1.draw(screen)
        self.raton.draw(screen)
