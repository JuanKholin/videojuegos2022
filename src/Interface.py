
import pygame as pg
from os import listdir
from os.path import isfile, join

from . import Player, Command, Utils, Raton, Button, Upgrade, UpgradeButton
from src.Music import *
from src.Lib import *
from src.Utils import *
from src.Loader import *
from src.AI import *

class Interface():
    buttonX = 0
    buttonY = 0
    upgradeX = 400
    upgradeY = 705

    def __init__(self, player, enemy, mouse):
        self.player = player
        self.enemy = enemy
        self.mouse = mouse
        # GAME SELECT
        self.partidas = []
        self.selectedPartida = None

        self.gameSelect = pg.image.load(GAME_SELECT + "gameSelect.png")
        self.gameSelect = pg.transform.scale(self.gameSelect, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.aceptarRect = pg.Rect(ACEPTAR_POS[0], ACEPTAR_POS[1], ACEPTAR_RECT[0], ACEPTAR_RECT[1])
        self.aceptarNoPulsabeSurf = pygame.Surface(ACEPTAR_RECT, pygame.SRCALPHA)
        self.aceptarNoPulsabeSurf.fill((0,0,0,128))
        self.cancelarRect = pg.Rect(CANCELAR_POS[0], CANCELAR_POS[1], 250, 40)
        self.nuevaPartidaRect = pg.Rect(NUEVA_PARTIDA_POS[0], NUEVA_PARTIDA_POS[1], 250, 40)

        self.aceptarPress = False
        self.cancelarPress = False
        self.nuevaPartidaPress = False

        # NEW GAME
        self.newGame = pg.image.load(NEW_GAME + "newGame.png")
        self.newGame = pg.transform.scale(self.newGame, (SCREEN_WIDTH, SCREEN_HEIGHT))

        #ya estan en game select
        #self.aceptarRect = pg.Rect(ACEPTAR_POS[0], ACEPTAR_POS[1], 260, 40)
        #self.cancelarRect = pg.Rect(CANCELAR_POS[0], CANCELAR_POS[1], 260, 40)
        self.botonesNewGame = [
            {"nombre": "1", "tipo": "mapa", "rect": pg.Rect(MAPA1_POS[0], MAPA1_POS[1], 90, 35), "press": False},
            {"nombre": "2", "tipo": "mapa", "rect": pg.Rect(MAPA2_POS[0], MAPA2_POS[1], 90, 35), "press": False},
            {"nombre": "3", "tipo": "mapa", "rect": pg.Rect(MAPA3_POS[0], MAPA3_POS[1], 90, 35), "press": False},
            {"nombre": "4", "tipo": "mapa", "rect": pg.Rect(MAPA4_POS[0], MAPA4_POS[1], 90, 35), "press": False},
            {"nombre": "Facil", "tipo": "dificultad", "rect": pg.Rect(FACIL_POS[0], FACIL_POS[1], 125, 35), "press": False},
            {"nombre": "Normal", "tipo": "dificultad", "rect": pg.Rect(NORMAL_POS[0], NORMAL_POS[1], 125, 35), "press": False},
            {"nombre": "Dificil", "tipo": "dificultad", "rect": pg.Rect(DIFICIL_POS[0], DIFICIL_POS[1], 125, 35), "press": False},
            {"nombre": "Terran", "tipo": "raza", "rect": pg.Rect(TERRAN_POS[0], TERRAN_POS[1], 185, 35), "press": False},
            {"nombre": "Zerg","tipo": "raza", "rect": pg.Rect(ZERG_POS[0], ZERG_POS[1], 185, 35), "press": False},
        ]

        self.selectedMap = "1"
        self.selectedDif = "Facil"
        self.selectedRaza = "Terran"



        #MAIN MENU
        self.mainMenu = pg.image.load(MAIN_MENU + ".png")
        self.mainMenu = pg.transform.scale(self.mainMenu, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.single = cargarSprites(SINGLE_PLAYER, SINGLE_PLAYER_N, True, BLACK, SINGLE_SIZE)
        self.exit = cargarSprites(EXIT, EXIT_N, True, BLACK, EXIT_SIZE)
        self.singleSelected = cargarSprites(SINGLE_PLAYER_FB, SINGLE_PLAYER_FB_N, True, BLACK, SINGLE_SIZE)
        self.exitSelected = cargarSprites(EXIT_FB, EXIT_FB_N, True, BLACK, EXIT_SIZE)

        self.loadGameGUI()

        self.singleRect = pg.Rect(SINGLE_PLAYER_POS[0], SINGLE_PLAYER_POS[1], self.single[0].get_width(), self.single[0].get_height())
        self.exitRect = pg.Rect(EXIT_POS[0], EXIT_POS[1], self.exit[0].get_width(), self.exit[0].get_height())
        self.singlePress = False
        self.exitPress = False

        self.heroeSprites = cargarSprites(HEROE_PATH, HEROE_N, False, None, 1.3)
        self.heroeIndex = 0

        self.idExit = 0
        self.idSingle = 0
        self.idSingleSelected = 0
        self.idExitSelected = 0

        self.soundPlayed = False

        self.entityOptions = []
        self.button = []

    def loadGameGUI(self):
        self.gui = pg.image.load(BARRA_COMANDO + ".bmp")
        self.gui = pg.transform.scale(self.gui, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.gui.set_colorkey(BLACK)

        self.resources = []
        self.resources.append(pg.transform.scale(pg.image.load("SPRITE/EXTRA/crystal.png"), (25, 25)))
        self.resources[0].set_colorkey(BLACK)

        self.resources.append(pg.transform.scale(pg.image.load("SPRITE/EXTRA/gastank.png"), (25, 25)))
        self.resources[1].set_colorkey(BLACK)

        self.resources.append(pg.transform.scale(pg.image.load("SPRITE/EXTRA/unit.png"), (25, 25)))
        self.resources[2].set_colorkey(BLACK)

        self.allButton = self.loadAllButton()
        self.allUpgrades = self.loadAllUpgrades()
        print("LOADEADOS")

    def loadAllButton(self):
        allButton = {}
        aux = Button.Button(BUTTON_PATH + "barracks" + ".bmp", CommandId.BUILD_BARRACKS,BUTTON_PATH + "construirConMineral.png", "Construir Barracas", 55, 50)
        allButton[Options.BUILD_BARRACKS] = aux
        aux = Button.Button(BUTTON_PATH + "worker" + ".bmp", CommandId.GENERATE_WORKER, BUTTON_PATH + "construirConMineral.png", "Construir VCE", 45, 50)
        allButton[Options.GENERATE_WORKER] = aux
        aux = Button.Button(BUTTON_PATH + "soldier" + ".bmp", CommandId.GENERATE_SOLDIER, BUTTON_PATH + "construirConMineral.png", "Construir Soldado", 55, 50)
        allButton[Options.GENERATE_SOLDIER] = aux
        aux = Button.Button(BUTTON_PATH + "soldier" + ".bmp", CommandId.BUILD_HATCHERY)
        allButton[Options.BUILD_HATCHERY] = aux
        aux = Button.Button(BUTTON_PATH + "refinery" + ".bmp", CommandId.BUILD_REFINERY, BUTTON_PATH + "construirConMineral.png", "Construir Refineria", 50, 50, 45)
        allButton[Options.BUILD_REFINERY] = aux
        aux = UpgradeButton.UpgradeButton(BUTTON_PATH + "danyoUpgrade" + ".png", CommandId.UPGRADE_SOLDIER_DAMAGE,BUTTON_PATH + "cartelUpgrade.bmp", "Mejorar daño;de las unidades", 90, 50)
        allButton[Options.DANYO_UPGRADE] = aux
        aux = UpgradeButton.UpgradeButton(BUTTON_PATH + "mineUpgrade" + ".png", CommandId.UPGRADE_WORKER_MINING,BUTTON_PATH + "cartelUpgrade.bmp", "Reducir tiempo de minado;de los VCE", 90, 50)
        allButton[Options.MINE_UPGRADE] = aux
        aux = UpgradeButton.UpgradeButton(BUTTON_PATH + "armorUpgrade" + ".png", CommandId.UPGRADE_SOLDIER_ARMOR,BUTTON_PATH + "cartelUpgrade.bmp", "Mejorar blindaje;de las unidades", 90, 120)
        allButton[Options.ARMOR_UPGRADE] = aux
        return allButton

    def loadAllUpgrades(self):
        allUpgrades = {}
        aux = Upgrade.Upgrade("./SPRITE/upgrades/armorConUpgrade.png")
        allUpgrades[Upgrades.ARMOR] = aux
        aux = Upgrade.Upgrade("./SPRITE/upgrades/danyoConUpgrade.png")
        allUpgrades[Upgrades.DANYO] = aux
        aux = Upgrade.Upgrade("./SPRITE/upgrades/mineConUpgrade.png")
        allUpgrades[Upgrades.MINE] = aux
        aux = Upgrade.Upgrade("./SPRITE/upgrades/armorSinUpgrade.png")
        allUpgrades[Upgrades.NO_ARMOR] = aux
        aux = Upgrade.Upgrade("./SPRITE/upgrades/danyoSinUpgrade.png")
        allUpgrades[Upgrades.NO_DANYO] = aux
        aux = Upgrade.Upgrade("./SPRITE/upgrades/mineSinUpgrade.png")
        allUpgrades[Upgrades.NO_MINE] = aux
        return allUpgrades

    def loadPartidas(self):
        onlyfiles = [f for f in listdir("./games") if isfile(join("./games", f))]
        pad = 0
        for file in onlyfiles:
            self.partidas.append({'nombre': str(file).split('.')[0],
                'rect': pg.Rect(PARTIDA_POS[0], PARTIDA_POS[1] + YPARTIDA_PAD*pad, 455, YPARTIDA_PAD-1),
                'pressed': False})
            pad += 1

    def update(self, escena, raton, camera):
        if Utils.state == System_State.MAINMENU:

            singleCollide = False

            press, iniPos = self.mouse.getPressed()
            #Boton single player
            if self.mouse.isCollide(self.singleRect):
                singleCollide = True
                if not self.soundPlayed:
                    playSound(botonSound)
                    self.soundPlayed = True
                endPos = self.mouse.getPosition()
                if not self.singlePress and press and Raton.collides(iniPos[0], iniPos[1], self.singleRect):
                    self.singlePress = True
                elif self.mouse.getClick() and self.singlePress and Raton.collides(endPos[0], endPos[1], self.singleRect):
                    print("Seleccionado single player")
                    #Utils.state = System_State.MAP1
                    self.loadPartidas()
                    Utils.state = System_State.GAMESELECT
                    #stopMusic()
                    self.singlePress = False

            if self.mouse.isCollide(self.exitRect):
                if not self.soundPlayed:
                    playSound(botonSound)
                    self.soundPlayed = True
                endPos = self.mouse.getPosition()
                if not self.exitPress and press and Raton.collides(iniPos[0], iniPos[1], self.exitRect):
                    self.exitPress = True
                elif self.mouse.getClick() and self.exitPress and Raton.collides(endPos[0], endPos[1], self.exitRect):
                    print("Seleccionado exit")
                    Utils.state = System_State.EXIT
                    stopMusic()
                    self.exitPress = False
            elif not singleCollide:
                self.soundPlayed = False

            if self.mouse.getClick():
                self.exitPress = False
                self.singlePress = False

            self.idSingle = (self.idSingle + frame(5)) % SINGLE_PLAYER_N
            self.idExit = (self.idExit + frame(5)) % EXIT_N
            self.idSingleSelected = (self.idSingleSelected + frame(5)) % SINGLE_PLAYER_FB_N
            self.idExitSelected = (self.idExitSelected + frame(5)) % EXIT_FB_N
        elif Utils.state == System_State.GAMESELECT:
            aceptarCollide = False

            press, iniPos = self.mouse.getPressed()
            #Boton aceptar
            #print(self.mouse.isCollide(self.nuevaPartidaRect), self.mouse.real_pos, self.aceptarRect.x, self.aceptarRect.y, self.aceptarRect.w, self.aceptarRect.h )
            if self.mouse.isCollide(self.aceptarRect) and self.selectedPartida != None:
                #print("acepar")
                aceptarCollide = True
                if not self.soundPlayed:
                    playSound(botonSound)
                    self.soundPlayed = True
                endPos = self.mouse.getPosition()
                if not self.aceptarPress and press and Raton.collides(iniPos[0], iniPos[1], self.aceptarRect):
                    self.aceptarPress = True
                elif self.mouse.getClick() and self.aceptarPress and Raton.collides(endPos[0], endPos[1], self.aceptarRect):
                    print("Aceptar")
                    #Hay que hacer uno generico, o que carge el mapa y pase a ONGAME aqui
                    _escena, _raton, _camera = loadFromSave(self.selectedPartida['nombre'])
                    escena.setSelf(_escena)
                    aI = AI(escena.p2, Race.ZERG, EASY)
                    escena.aI = aI
                    raton.setSelf(_raton)
                    self.player = escena.p1
                    self.enemy = escena.p2
                    escena.raton = raton
                    self.raton = escena.raton
                    raton.addInterface(self)
                    escena.interfaz = self
                    camera.setSelf(_camera)
                    Utils.state = System_State.ONGAME
                    stopMusic()
                    self.singlePress = False

            elif self.mouse.isCollide(self.cancelarRect):
                #print("cancelar")
                if not self.soundPlayed:
                    playSound(botonSound)
                    self.soundPlayed = True
                endPos = self.mouse.getPosition()
                if not self.cancelarPress and press and Raton.collides(iniPos[0], iniPos[1], self.cancelarRect):
                    self.cancelarPress = True
                elif self.mouse.getClick() and self.cancelarPress and Raton.collides(endPos[0], endPos[1], self.cancelarRect):
                    print("Cancelar")
                    Utils.state = System_State.MAINMENU
                    self.cancelarPress = False
                    self.selectedPartida = None
            elif self.mouse.isCollide(self.nuevaPartidaRect):
                #print("newgame")
                if not self.soundPlayed:
                    playSound(botonSound)
                    self.soundPlayed = True
                endPos = self.mouse.getPosition()
                if not self.nuevaPartidaPress and press and Raton.collides(iniPos[0], iniPos[1], self.nuevaPartidaRect):
                    self.nuevaPartidaPress = True
                elif self.mouse.getClick() and self.nuevaPartidaPress and Raton.collides(endPos[0], endPos[1], self.nuevaPartidaRect):
                    print("Nueva partida")
                    #Pasar a menu de nueva partida
                    Utils.state = System_State.NEWGAME
                    stopMusic()
                    self.nuevaPartidaPress = False
            else:
                self.soundPlayed = False

            for partida in self.partidas:
                if self.mouse.isCollide(partida['rect']):
                    endPos = self.mouse.getPosition()
                    if not partida['pressed'] and press and Raton.collides(iniPos[0], iniPos[1], partida['rect']):
                        partida['pressed'] = True
                    elif self.mouse.getClick() and partida['pressed'] and Raton.collides(endPos[0], endPos[1], partida['rect']):
                        print(partida['nombre'])
                        #Pasar a menu de nueva partida
                        self.selectedPartida = partida
                        playSound(botonSound2)
                        partida['pressed'] = False


            if self.mouse.getClick():
                self.aceptarPress = False
                self.cancelarPress = False
                self.nuevaPartidaPress = False



        elif Utils.state == System_State.NEWGAME:
            aceptarCollide = False

            press, iniPos = self.mouse.getPressed()
            #Boton aceptar
            if self.mouse.isCollide(self.aceptarRect):
                aceptarCollide = True
                if not self.soundPlayed:
                    playSound(botonSound)
                    self.soundPlayed = True
                endPos = self.mouse.getPosition()
                if not self.aceptarPress and press and Raton.collides(iniPos[0], iniPos[1], self.aceptarRect):
                    self.aceptarPress = True
                elif self.mouse.getClick() and self.aceptarPress and Raton.collides(endPos[0], endPos[1], self.aceptarRect):
                    print("Aceptar")
                    #Con self.selectedMap selectedDif selectedRaza se crea la partida
                    Utils.state = System_State.MAP1
                    stopMusic()
                    self.singlePress = False

            elif self.mouse.isCollide(self.cancelarRect):
                if not self.soundPlayed:
                    playSound(botonSound)
                    self.soundPlayed = True
                endPos = self.mouse.getPosition()
                if not self.cancelarPress and press and Raton.collides(iniPos[0], iniPos[1], self.cancelarRect):
                    self.cancelarPress = True
                elif self.mouse.getClick() and self.cancelarPress and Raton.collides(endPos[0], endPos[1], self.cancelarRect):
                    print("Cancelar")
                    Utils.state = System_State.GAMESELECT
                    self.cancelarPress = False
            else:
                self.soundPlayed = False

            for b in self.botonesNewGame:
                if self.mouse.isCollide(b['rect']):
                    endPos = self.mouse.getPosition()
                    if not b['press'] and press and Raton.collides(iniPos[0], iniPos[1], b['rect']):
                        b['press'] = True
                    elif self.mouse.getClick() and b['press'] and Raton.collides(endPos[0], endPos[1], b['rect']):
                        print(b['nombre'])
                        playSound(botonSound2)
                        b['press'] = False
                        if b['tipo'] == "mapa":
                            self.selectedMap = b['nombre']
                        elif b['tipo'] == "dificultad":
                            self.selectedDif = b['nombre']
                        elif b['tipo'] == "raza":
                            self.selectedRaza = b['nombre']



            if self.mouse.getClick():
                self.aceptarPress = False
                self.cancelarPress = False

        elif Utils.state == System_State.ONGAME:
            #si esta en GUI desactivar funciones de raton
            if self.checkInGUIPosition():
                self.mouse.setEnable(False)
            else:
                self.mouse.setEnable(True)

            self.button = []
            #obtener opciones de la unidad seleccionada
            if self.player.structureSelected != None:
                self.entityOptions = self.player.structureSelected.getOptions()
                self.button = self.getButton(self.entityOptions)
                self.buttonX = BUTTON_X
                self.buttonY = BUTTON_Y

            #comprobar colision del raton
            for b in self.button:
                if Raton.collides(self.mouse.rel_pos[0], self.mouse.rel_pos[1], b.getRect()):
                    b.setCollide(True)
                else:
                    b.setCollide(False)

            #Comprobar collisiones con las mejoras
            self.upgrades = []
            if self.player.unitsSelected.__len__() == 1:
                self.upgrades = self.getUpgrades(self.player.unitsSelected[0].getUpgrades())


            #comprobar colision del raton
            for up in self.upgrades:
                if Raton.collides(self.mouse.rel_pos[0], self.mouse.rel_pos[1], up.getRect()):
                    up.setCollide(True)
                else:
                    up.setCollide(False)

            if frame(10):
                self.heroeIndex = (self.heroeIndex+1)%HEROE_N

    def draw(self, screen, camera):
        if Utils.state == System_State.MAINMENU:
            screen.blit(self.mainMenu, [0, 0])


            #Boton single player
            if self.mouse.isCollide(self.singleRect):
                screen.blit(self.singleSelected[self.idSingleSelected], SINGLE_PLAYER_FB_POS)
                screen.blit(self.single[self.idSingle], SINGLE_PLAYER_POS)
                muestra_texto(screen, 'monotypecorsiva', "single player", GREEN2, MAIN_MENU_TEXT_SIZE, SINGLE_TEXT_POS)
            else:
                screen.blit(self.single[self.idSingle], SINGLE_PLAYER_POS)
                muestra_texto(screen, 'monotypecorsiva', "single player", GREEN3, MAIN_MENU_TEXT_SIZE, SINGLE_TEXT_POS)
            #screen.blit(self.single[self.idSingle], SINGLE_PLAYER_POS)

            #Boton Exit
            screen.blit(self.exit[self.idExit], EXIT_POS)
            if self.mouse.isCollide(self.exitRect):
                screen.blit(self.exitSelected[self.idExitSelected], EXIT_FB_POS)
                muestra_texto(screen, str('monotypecorsiva'), "exit", GREEN2, MAIN_MENU_TEXT_SIZE, EXIT_TEXT_POS)
            else:
                muestra_texto(screen, str('monotypecorsiva'), "exit", GREEN3, MAIN_MENU_TEXT_SIZE, EXIT_TEXT_POS)

        elif Utils.state == System_State.GAMESELECT:
            screen.blit(self.gameSelect, [0, 0])

            if self.mouse.isCollide(self.aceptarRect) and self.selectedPartida != None:
                pygame.draw.rect(screen, GREEN3, self.aceptarRect, 1)
            elif self.selectedPartida == None:
                screen.blit(self.aceptarNoPulsabeSurf, ACEPTAR_POS)
            if self.mouse.isCollide(self.cancelarRect):
                pygame.draw.rect(screen, GREEN3, self.cancelarRect, 1)
            if self.mouse.isCollide(self.nuevaPartidaRect):
                pygame.draw.rect(screen, GREEN3, self.nuevaPartidaRect, 1)

            for partida in self.partidas:
                if self.mouse.isCollide(partida['rect']) or partida == self.selectedPartida:
                    pygame.draw.rect(screen, GREEN3, partida['rect'], 1)

                muestra_texto(screen, str('monotypecorsiva'), partida['nombre'], WHITE, 28, (partida['rect'].x + 200, partida['rect'].y + 18))
            '''
            #Boton single player
            if self.mouse.isCollide(self.singleRect):
                screen.blit(self.singleSelected[self.idSingleSelected], SINGLE_PLAYER_FB_POS)
                screen.blit(self.single[self.idSingle], SINGLE_PLAYER_POS)
                muestra_texto(screen, 'monotypecorsiva', "single player", GREEN2, MAIN_MENU_TEXT_SIZE, SINGLE_TEXT_POS)
            else:
                screen.blit(self.single[self.idSingle], SINGLE_PLAYER_POS)
                muestra_texto(screen, 'monotypecorsiva', "single player", GREEN3, MAIN_MENU_TEXT_SIZE, SINGLE_TEXT_POS)
            #screen.blit(self.single[self.idSingle], SINGLE_PLAYER_POS)

            #Boton Exit
            screen.blit(self.exit[self.idExit], EXIT_POS)
            if self.mouse.isCollide(self.exitRect):
                screen.blit(self.exitSelected[self.idExitSelected], EXIT_FB_POS)
                muestra_texto(screen, str('monotypecorsiva'), "exit", GREEN2, MAIN_MENU_TEXT_SIZE, EXIT_TEXT_POS)
            else:
                muestra_texto(screen, str('monotypecorsiva'), "exit", GREEN3, MAIN_MENU_TEXT_SIZE, EXIT_TEXT_POS)            '''

        elif Utils.state == System_State.NEWGAME:
            screen.blit(self.newGame, [0, 0])
            '''
            pygame.draw.rect(screen, BLUE, self.mapa1Rect, 1)
            pygame.draw.rect(screen, BLACK, self.mapa2Rect, 1)
            pygame.draw.rect(screen, GREEN, self.mapa3Rect, 1)
            pygame.draw.rect(screen, PINK, self.mapa4Rect, 1)

            pygame.draw.rect(screen, BLACK, self.facilRect, 1)
            pygame.draw.rect(screen, GREEN, self.normalRect, 1)
            pygame.draw.rect(screen, PINK, self.dificilRect, 1)

            pygame.draw.rect(screen, GREEN, self.terranRect, 1)
            pygame.draw.rect(screen, PINK, self.zergRect, 1)'''

            if (self.mouse.isCollide(self.aceptarRect) and
            (self.selectedMap != None or self.selectedDif != None or self.selectedRaza != None)):
                pygame.draw.rect(screen, GREEN3, self.aceptarRect, 1)
            elif self.selectedMap == None or self.selectedDif == None or self.selectedRaza == None:
                screen.blit(self.aceptarNoPulsabeSurf, ACEPTAR_POS)
            if self.mouse.isCollide(self.cancelarRect):
                pygame.draw.rect(screen, GREEN3, self.cancelarRect, 1)

            for b in self.botonesNewGame:
                if (self.mouse.isCollide(b['rect']) or b['nombre'] == self.selectedMap
                or b['nombre'] == self.selectedDif or b['nombre'] == self.selectedRaza):
                    pygame.draw.rect(screen, GREEN3, b['rect'], 1)


            muestra_texto(screen, str('monotypecorsiva'), str(self.selectedMap), WHITE, 40, (740,193))
            muestra_texto(screen, str('monotypecorsiva'), self.selectedDif, WHITE, 40, (840,299))
            muestra_texto(screen, str('monotypecorsiva'), self.selectedRaza, WHITE, 40, (765,410))

        elif Utils.state == System_State.ONGAME:
            if DEBBUG == True:
                muestra_texto(screen, str('monotypecorsiva'), str(round(Utils.SYSTEM_CLOCK / CLOCK_PER_SEC)), BLACK, 30, (20, 20))
                muestra_texto(screen, times, str(self.player.resources), BLUE, 30, (SCREEN_WIDTH - 40, 60))
                muestra_texto(screen, times, str(self.enemy.resources), RED, 30, (SCREEN_WIDTH - 40, 100))

            screen.blit(self.resources[0], (RESOURCES_COUNT_X, 3))
            muestra_texto(screen, times, str(self.player.resources), GREEN4, 30, (RESOURCES_COUNT_X + 60, 20))
            screen.blit(self.resources[1], (RESOURCES_COUNT_X + 100, 3))
            muestra_texto(screen, times, str(self.player.gas), GREEN4, 30, (RESOURCES_COUNT_X + 160, 20))
            screen.blit(self.resources[2], (RESOURCES_COUNT_X + 200, 3))
            muestra_texto(screen, times, str(self.player.units.__len__() + 10) + "/18", GREEN4, 28, (RESOURCES_COUNT_X + 260, 18))

            screen.blit(self.gui, (0, 0))

            #draw minimapa
            pygame.draw.rect(screen, BLUE, pygame.Rect(MINIMAP_X, MINIMAP_Y, MINIMAP_W, MINIMAP_H), 1)
            #self.player.mapa.drawMinimap(screen)
            self.player.drawEntity(screen, True)
            self.enemy.drawEntity(screen, False)

            pygame.draw.rect(screen, WHITE, pygame.Rect(MINIMAP_X + (camera.x/self.player.mapa.w * MINIMAP_W), MINIMAP_Y + (camera.y/self.player.mapa.h * MINIMAP_H), camera.w/self.player.mapa.w * MINIMAP_W, camera.h/self.player.mapa.h * MINIMAP_H), 2)

            #informacion de entidades seleccionadas
            self.drawEntityInfo(screen, camera)

            #draw cara del heroe
            screen.blit(self.heroeSprites[self.heroeIndex], (672, 667))

            #draw comandos de la entidad seleccionada
            opcion = 0
            for b in self.button:
                opcion += 1
                b.draw(screen, self.buttonX, self.buttonY)
                self.buttonX += BUTTONPADX
                if opcion % 3 == 0:
                    self.buttonY += BUTTONPADY
                    self.buttonX = BUTTON_X
                if opcion == 9:
                    break

    def drawEntityInfo(self, screen, camera):
        if len(self.player.unitsSelected) == 1:
            upgrades = self.getUpgrades( self.player.unitsSelected[0].getUpgrades())
            self.showInfo(screen, self.player.unitsSelected[0], GREEN3, 10, 10, 60, 135, upgrades)
        elif len(self.player.unitsSelected) > 1:
            images = []
            for unit in self.player.unitsSelected:
                image = unit.getRender()
                image = pygame.transform.scale(image, [image.get_rect().w * 0.7, image.get_rect().h * 0.7])
                images.append(image)
            x = 0
            y = 0
            n = 0
            for image in images:
                screen.blit(image, (GUI_INFO_X + x, GUI_INFO_Y + 5 + y))
                x += 85
                n += 1
                if n == 4:
                    y = 75
                    x = 0
                if n == 8:
                    break
        if len(self.player.enemySelected) == 1:
            self.showInfo(screen, self.player.enemySelected[0], RED, 10, 10, 60, 135)
        elif len(self.player.enemySelected) > 1:
            images = []
            for unit in self.player.enemySelected:
                image = unit.getRender()
                image = pygame.transform.scale(image, [image.get_rect().w * 0.7, image.get_rect().h * 0.7])
                images.append(image)
            x = 0
            y = 0
            n = 0
            for image in images:
                screen.blit(image, (GUI_INFO_X + x, GUI_INFO_Y + 5 + y))
                x += 85
                n += 1
                if n == 4:
                    y = 100
                    x = 0
                if n == 8:
                    break
        elif self.player.structureSelected != None:
            self.showInfo(screen, self.player.structureSelected, GREEN3, 0, 5, 60, 135)
        elif self.player.enemyStructureSelected != None:
            self.showInfo(screen, self.player.enemyStructureSelected, RED, 0, 5, 60, 135)
        elif self.player.resourceSelected != None:
            image = self.player.resourceSelected.getRender()
            capacity = str(self.player.resourceSelected.getCapacity())

            screen.blit(image, (GUI_INFO_X, GUI_INFO_Y))
            muestra_texto(screen, 'monotypecorsiva', capacity, YELLOW, 20, [GUI_INFO_X + 60, GUI_INFO_Y + 135])
            self.player.resourceSelected.drawInfo(screen, YELLOW)

    def showInfo(self, screen, unit, color, renderX = 0, renderY = 0, hpX = 0, hpY = 0, upgrades = None):
        image = unit.getRender()
        hpState = str(unit.getHP()) + "/" + str(unit.getMaxHP())
        x = self.upgradeX
        if upgrades != None: #Dibujar las upgrades
            for upgrade in upgrades:
                upgrade.draw(screen, x, self.upgradeY)
                x += UPGRADEPADX
        screen.blit(image, (GUI_INFO_X + renderX, GUI_INFO_Y + renderY))
        muestra_texto(screen, 'monotypecorsiva', hpState, color, 20, [GUI_INFO_X + hpX, GUI_INFO_Y + hpY])
        unit.drawInfo(screen, color)

    def checkInGUIPosition(self):
        x = self.mouse.rel_pos[0]
        y = self.mouse.rel_pos[1]
        yes = False
        if y > 600:
            yes = True
        elif x < 15 and y > 485:
            yes = True
        elif x < 30 and y > 490:
            yes = True
        elif x < 40 and y > 510:
            yes = True
        elif x < 265 and y > 510:
            yes = True
        elif x > 735 and y > 585:
            yes = True
        elif x > 750 and y > 535:
            yes = True
        return yes

    def getButton(self, entityOptions):
        buttons = []
        for e in entityOptions:
            if e == Options.ARMOR_UPGRADE:
                self.allButton[e].costeMineral = self.player.structureSelected.armorMineralUpCost
                self.allButton[e].costeGas = self.player.structureSelected.armorGasUpCost
                self.allButton[e].nextLevel = int(self.player.structureSelected.armorMineralUpCost / 25 - 1)
                buttons.append(self.allButton[e])
            elif e == Options.DANYO_UPGRADE:
                self.allButton[e].costeMineral = self.player.structureSelected.dañoMineralUpCost
                self.allButton[e].costeGas = self.player.structureSelected.dañoGasUpCost
                self.allButton[e].nextLevel = int(self.player.structureSelected.dañoMineralUpCost / 25 - 1)
                buttons.append(self.allButton[e])
            elif e == Options.MINE_UPGRADE:
                self.allButton[e].costeMineral = self.player.structureSelected.mineMineralUpCost
                self.allButton[e].costeGas = self.player.structureSelected.mineGasUpCost
                self.allButton[e].nextLevel = int(self.player.structureSelected.mineMineralUpCost / 25 - 1)
                buttons.append(self.allButton[e])
            elif e != Options.NULO:
                buttons.append(self.allButton[e])


        return buttons

    def getUpgrades(self, upgrades):
        ups = []
        for upgrade in upgrades:
            self.allUpgrades[upgrade['upgrade']].cantidad = upgrade['cantidad']
            ups.append(self.allUpgrades[upgrade['upgrade']])
        return ups
