
from token import OP
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
    index = 0
    
    heropadx = 0
    heropady = 0

    def __init__(self, player, enemy, mouse):
        self.player = player
        self.enemy = enemy
        self.mouse = mouse
        # GAME SELECT
        self.partidas = []
        self.selectedPartida = None

        self.gameSelect = pg.image.load(GAME_SELECT + "gameSelect.png")
        self.gameSelect = pg.transform.scale(self.gameSelect, (ScreenWidth, ScreenHeight))

        self.aceptarRect = pg.Rect(ACEPTAR_POS[0], ACEPTAR_POS[1], ACEPTAR_RECT[0], ACEPTAR_RECT[1])
        self.aceptarNoPulsabeSurf = pygame.Surface(ACEPTAR_RECT, pygame.SRCALPHA)
        self.aceptarNoPulsabeSurf.fill((0,0,0,128))
        self.cancelarRect = pg.Rect(CANCELAR_POS[0], CANCELAR_POS[1], 250, 40)
        self.nuevaPartidaRect = pg.Rect(NUEVA_PARTIDA_POS[0], NUEVA_PARTIDA_POS[1], 250, 40)

        self.aceptarPress = False
        self.cancelarPress = False
        self.nuevaPartidaPress = False

        #PAUSE
        self.pauseRect = pg.Rect(0, 0, 50, 50)
        self.continueRect = pg.Rect(710,90,50,50)
        self.helpPauseRect = pg.Rect(265,90,50,50)
        self.exitPauseRect = pg.Rect(700,90,50,50)

        # NEW GAME
        self.newGame = pg.image.load(NEW_GAME + "newGame.png")
        self.newGame = pg.transform.scale(self.newGame, (ScreenWidth, ScreenHeight))

        #ya estan en game select
        #self.aceptarRect = pg.Rect(ACEPTAR_POS[0], ACEPTAR_POS[1], 260, 40)
        #self.cancelarRect = pg.Rect(CANCELAR_POS[0], CANCELAR_POS[1], 260, 40)
        self.botonRazaTerran = {"nombre": "Terran", "tipo": "raza", "rect": pg.Rect(TERRAN_POS[0], TERRAN_POS[1], 185, 35), "press": False, "raza": Race.TERRAN}
        self.botonesNewGame = [
            {"nombre": "1", "tipo": "mapa", "rect": pg.Rect(MAPA1_POS[0], MAPA1_POS[1], 90, 35), "press": False},
            {"nombre": "2", "tipo": "mapa", "rect": pg.Rect(MAPA2_POS[0], MAPA2_POS[1], 90, 35), "press": False},
            {"nombre": "3", "tipo": "mapa", "rect": pg.Rect(MAPA3_POS[0], MAPA3_POS[1], 90, 35), "press": False},
            {"nombre": "4", "tipo": "mapa", "rect": pg.Rect(MAPA4_POS[0], MAPA4_POS[1], 90, 35), "press": False},
            {"nombre": "Facil", "tipo": "dificultad", "rect": pg.Rect(FACIL_POS[0], FACIL_POS[1], 125, 35), "press": False, "dif": EASY},
            {"nombre": "Normal", "tipo": "dificultad", "rect": pg.Rect(NORMAL_POS[0], NORMAL_POS[1], 125, 35), "press": False, "dif": MEDIUM},
            {"nombre": "Dificil", "tipo": "dificultad", "rect": pg.Rect(DIFICIL_POS[0], DIFICIL_POS[1], 125, 35), "press": False, "dif": HARD},
            self.botonRazaTerran,
            {"nombre": "Zerg","tipo": "raza", "rect": pg.Rect(ZERG_POS[0], ZERG_POS[1], 185, 35), "press": False, "raza": Race.ZERG},
        ]

        self.selectedMap = "1"
        self.selectedDif = {"nombre":"Facil", "dif": EASY}
        self.selectedRaza = {"nombre":"Terran", "raza": Race.TERRAN}



        #MAIN MENU
        self.mainMenu = pg.image.load(MAIN_MENU + ".png")
        self.mainMenu = pg.transform.scale(self.mainMenu, (ScreenWidth, ScreenHeight))
        self.single = cargarSprites(SINGLE_PLAYER, SINGLE_PLAYER_N, True, BLACK, SINGLE_SIZE)
        self.exit = cargarSprites(EXIT, EXIT_N, True, BLACK, EXIT_SIZE)
        self.singleSelected = cargarSprites(SINGLE_PLAYER_FB, SINGLE_PLAYER_FB_N, True, BLACK, SINGLE_SIZE)
        self.exitSelected = cargarSprites(EXIT_FB, EXIT_FB_N, True, BLACK, EXIT_SIZE)

        self.loadGameGUI()

        self.singleRect = pg.Rect(Utils.ScreenWidth/2 - SINGLE_PLAYER_POS[0], Utils.ScreenHeight/2 - SINGLE_PLAYER_POS[1], self.single[0].get_width(), self.single[0].get_height())
        self.exitRect = pg.Rect(Utils.ScreenWidth/2 - EXIT_POS[0], Utils.ScreenHeight/2 - EXIT_POS[1], self.exit[0].get_width(), self.exit[0].get_height())
        self.ajustesSonidoRect = pg.Rect(Utils.ScreenWidth/2 - AJUSTES_SONIDO_POS[0], Utils.ScreenHeight/2 - AJUSTES_SONIDO_POS[1], 220, 40)
        self.ajustesAtajosRect = pg.Rect(Utils.ScreenWidth/2 - AJUSTES_ATAJOS_POS[0], Utils.ScreenHeight/2 - AJUSTES_ATAJOS_POS[1], 220, 40)
        self.singlePress = False
        self.exitPress = False
        self.ajustesAtajosPress = False
        self.ajustesSonidoPress = False

        self.heroeSprites = cargarSprites(HEROE_PATH, HEROE_N, False, None, 1.3)
        self.heroeIndex = 0
        self.herow = self.heroeSprites[0].get_width()
        self.heroh = self.heroeSprites[0].get_height()
        self.count2 = 0

        self.idExit = 0
        self.idSingle = 0
        self.idSingleSelected = 0
        self.idExitSelected = 0

        self.soundPlayed = False

        self.entityOptions = []
        self.button = []

        
        #ANIMACION
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        deadSprites = Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200, (ScreenWidth, ScreenHeight))
        for sprite in deadSprites:
            sprite = pg.transform.scale(sprite, (ScreenWidth, ScreenHeight))
        self.loseSprite = deadSprites + cargarSprites("./SPRITE/animacion/gameOver/tile0", 20, True, size = [ScreenWidth, ScreenHeight])
    
        self.winSprite = deadSprites + cargarSprites("./SPRITE/animacion/win/tile0", 20, True, size = [ScreenWidth, ScreenHeight])
        
        #HELP
        self.helpPage = 0
        self.helpButtons = []
        self.helpPageSprites = cargarSprites("./SPRITE/EXTRA/help", 6, False, size = (526, 660))


    def loadGameGUI(self):
        self.gui = pg.image.load(BARRA_COMANDO + ".bmp")
        self.gui = pg.transform.scale(self.gui, (ScreenWidth, ScreenHeight))
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
        #print("LOADEADOS")

    def loadAllButton(self):
        allButton = {}
        #Terran unidades
        aux = Button.Button(BUTTON_PATH + "worker" + ".bmp", CommandId.GENERATE_WORKER, BUTTON_PATH + "construirConMineral.png", "Construir VCE", 45, TERRAN_WORKER_MINERAL_COST)
        allButton[Options.GENERATE_WORKER_TERRAN] = aux
        aux = Button.Button(BUTTON_PATH + "soldier" + ".bmp", CommandId.GENERATE_T1, BUTTON_PATH + "construirConMineral.png", "Construir Soldado", 55, TERRAN_T1_MINERAL_COST)
        allButton[Options.GENERATE_T1_TERRAN] = aux
        
        #Terran estructuras
        aux = Button.Button(BUTTON_PATH + "barracks" + ".bmp", CommandId.BUILD_BARRACKS,BUTTON_PATH + "construirConMineral.png", "Construir Barracas", 55, TERRAN_BARRACKS_MINERAL_COST)
        allButton[Options.BUILD_BARRACKS_TERRAN] = aux
        aux = Button.Button(BUTTON_PATH + "depot" + ".bmp", CommandId.BUILD_DEPOT, BUTTON_PATH + "construirConMineral.png", "Construir Deposito", 55, TERRAN_DEPOT_MINERAL_COST, 45)
        allButton[Options.BUILD_DEPOT_TERRAN] = aux
        aux = Button.Button(BUTTON_PATH + "refinery" + ".bmp", CommandId.BUILD_REFINERY, BUTTON_PATH + "construirConMineral.png", "Construir Refineria", 50, TERRAN_REFINERY_MINERAL_COST, 45)
        allButton[Options.BUILD_REFINERY_TERRAN] = aux
        
        #Zerg unidades
        aux = Button.Button(BUTTON_PATH + "drone" + ".png", CommandId.GENERATE_WORKER,BUTTON_PATH + "construirConMineral.png", "Engendrar Drone", 55, ZERG_WORKER_MINERAL_COST)
        allButton[Options.GENERATE_WORKER_ZERG] = aux
        aux = Button.Button(BUTTON_PATH + "zergling" + ".png", CommandId.GENERATE_T1,BUTTON_PATH + "construirConMineral.png", "Engendrar Zergling", 55, ZERG_T1_MINERAL_COST)
        allButton[Options.GENERATE_T1_ZERG] = aux
        aux = Button.Button(BUTTON_PATH + "broodling" + ".png", CommandId.GENERATE_T2,BUTTON_PATH + "construirConMineral.png", "Engendrar Broodling", 55, ZERG_T2_MINERAL_COST)
        allButton[Options.GENERATE_T2_ZERG] = aux
        aux = Button.Button(BUTTON_PATH + "hydralisk" + ".png", CommandId.GENERATE_T3,BUTTON_PATH + "construirConMineral.png", "Engendrar Hydralisk", 55, ZERG_T3_MINERAL_COST)
        allButton[Options.GENERATE_T3_ZERG] = aux
        
        #Zerg estructuras
        aux = Button.Button(BUTTON_PATH + "zergBarracks" + ".png", CommandId.BUILD_BARRACKS,BUTTON_PATH + "construirConMineral.png", "Construir Colmena", 55, ZERG_BARRACKS_MINERAL_COST)
        allButton[Options.BUILD_BARRACKS_ZERG] = aux
        aux = Button.Button(BUTTON_PATH + "zergSupply" + ".png", CommandId.BUILD_DEPOT, BUTTON_PATH + "construirConMineral.png", "Construir Guarida", 55, SUPPLY_ZERG_MINERAL_COST, 45)
        allButton[Options.BUILD_DEPOT_ZERG] = aux
        aux = Button.Button(BUTTON_PATH + "zergRefinery" + ".png", CommandId.BUILD_REFINERY, BUTTON_PATH + "construirConMineral.png", "Construir Extractor", 50, EXTRACTOR_MINERAL_COST, 45)
        allButton[Options.BUILD_REFINERY_ZERG] = aux
        #aux = Button.Button(BUTTON_PATH + "soldier" + ".bmp", CommandId.BUILD_HATCHERY)
        #allButton[Options.BUILD_HATCHERY] = aux
        
        #botones
        aux = Button.Button(BUTTON_PATH + "close" + ".png", CommandId.RETURN_GAME)
        aux.image.set_colorkey(BLACK)
        allButton[Options.CLOSE] = aux
        aux = Button.Button(BUTTON_PATH + "next" + ".png", CommandId.NEXT_PAGE)
        aux.image.set_colorkey(BLACK)
        allButton[Options.NEXT_PAGE] = aux
        aux = Button.Button(BUTTON_PATH + "previous" + ".png", CommandId.PREVIOUS_PAGE)
        aux.image.set_colorkey(BLACK)
        allButton[Options.PREVIOUS_PAGE] = aux
        
        #mejoras
        aux = UpgradeButton.UpgradeButton(BUTTON_PATH + "danyoUpgrade" + ".png", CommandId.UPGRADE_SOLDIER_DAMAGE,BUTTON_PATH + "cartelUpgrade.bmp", "Mejorar daño;de las unidades", 90, 50)
        allButton[Options.DANYO_UPGRADE] = aux
        aux = UpgradeButton.UpgradeButton(BUTTON_PATH + "mineUpgrade" + ".png", CommandId.UPGRADE_WORKER_MINING,BUTTON_PATH + "cartelUpgrade.bmp", "Reducir tiempo de minado;de los VCE", 90, 50)
        allButton[Options.MINE_UPGRADE] = aux
        aux = UpgradeButton.UpgradeButton(BUTTON_PATH + "armorUpgrade" + ".png", CommandId.UPGRADE_SOLDIER_ARMOR,BUTTON_PATH + "cartelUpgrade.bmp", "Mejorar blindaje;de las unidades", 90, 120)
        allButton[Options.ARMOR_UPGRADE] = aux

        self.pauseButton = Button.Button(BUTTON_PATH + "pause" + ".png", CommandId.PAUSE_GAME)
        #self.continueButton = Button.Button(BUTTON_PATH + "continue" + ".png", CommandId.PAUSE_GAME)
        self.helpPauseButton = Button.Button(BUTTON_PATH + "ayuda" + ".png", CommandId.HELP)
        self.exitPauseButton = Button.Button(BUTTON_PATH + "close" + ".png", CommandId.RETURN_GAME)
        self.saveButton = Button.Button(BUTTON_PATH + "save" + ".png", CommandId.SAVE_GAME)
        self.saveAndExitButton = Button.Button(BUTTON_PATH + "guardarYSalir" + ".png", CommandId.SAVE_EXIT_GAME)
        self.exitButton = Button.Button(BUTTON_PATH + "salir" + ".png", CommandId.EXIT_GAME)
        self.helpPauseButton.x = self.helpPauseRect.x
        self.helpPauseButton.y = self.helpPauseRect.y
        self.exitPauseButton.x = self.exitPauseRect.x
        self.exitPauseButton.y = self.exitPauseRect.y
        self.pauseButtons = [self.exitPauseButton, self.helpPauseButton, self.saveButton, self.saveAndExitButton, self.exitButton]
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
        self.partidas = []
        for file in onlyfiles:
            self.partidas.append({'nombre': str(file).split('.')[0],
                'rect': pg.Rect(Utils.ScreenWidth/2 - PARTIDA_POS[0], Utils.ScreenHeight/2 - PARTIDA_POS[1] + YPARTIDA_PAD*pad, 455, YPARTIDA_PAD-1),
                'pressed': False})
            pad += 1
    
    def getNumPartidas(self):
        onlyfiles = [f for f in listdir("./games") if isfile(join("./games", f))]
        pad = 0
        for file in onlyfiles:
            pad += 1
        return pad


    def update(self, escena, raton, camera):
        if Utils.state == System_State.MAINMENU:
            
            self.updateMainMenu()

        elif Utils.state == System_State.GAMESELECT:
            
            self.updateGameMenu(escena, raton, camera)

        elif Utils.state == System_State.NEWGAME:

            self.updateNewGame(escena, raton, camera)

        elif Utils.state == System_State.ONGAME:
            
            self.updateOnGame()
    
    def updateMainMenuPos(self):
        self.mainMenu = pg.transform.scale(self.mainMenu, (Utils.ScreenHeight*SCREEN_SCALE, Utils.ScreenHeight));
        self.singleRect = pg.Rect(Utils.ScreenWidth/2 - SINGLE_PLAYER_POS[0], Utils.ScreenHeight/2 - SINGLE_PLAYER_POS[1], self.single[0].get_width(), self.single[0].get_height())
        self.exitRect = pg.Rect(Utils.ScreenWidth/2 - EXIT_POS[0], Utils.ScreenHeight/2 - EXIT_POS[1], self.exit[0].get_width(), self.exit[0].get_height())
        self.ajustesSonidoRect = pg.Rect(Utils.ScreenWidth/2 - AJUSTES_SONIDO_POS[0], Utils.ScreenHeight/2 - AJUSTES_SONIDO_POS[1], 220, 40)
        self.ajustesAtajosRect = pg.Rect(Utils.ScreenWidth/2 - AJUSTES_ATAJOS_POS[0], Utils.ScreenHeight/2 - AJUSTES_ATAJOS_POS[1], 220, 40)
            
    def updateMainMenu(self):
        self.updateMainMenuPos()
        press, iniPos = self.mouse.getPressed()
        #Boton single player
        if self.mouse.isCollide(self.singleRect):
            if not self.soundPlayed:
                playSound(botonSound)
                self.soundPlayed = True
            endPos = self.mouse.getPosition()
            if not self.singlePress and press and Raton.collides(iniPos[0], iniPos[1], self.singleRect):
                self.singlePress = True
            elif self.mouse.getClick() and self.singlePress and Raton.collides(endPos[0], endPos[1], self.singleRect):
                #print("Seleccionado single player")
                Utils.state = System_State.MAP1
                self.loadPartidas()
                Utils.state = System_State.GAMESELECT
                #stopMusic()
                self.singlePress = False

        elif self.mouse.isCollide(self.exitRect):
            if not self.soundPlayed:
                playSound(botonSound)
                self.soundPlayed = True
            endPos = self.mouse.getPosition()
            if not self.exitPress and press and Raton.collides(iniPos[0], iniPos[1], self.exitRect):
                self.exitPress = True
            elif self.mouse.getClick() and self.exitPress and Raton.collides(endPos[0], endPos[1], self.exitRect):
                #print("Seleccionado exit")
                Utils.state = System_State.EXIT
                stopMusic()
                self.exitPress = False

        elif self.mouse.isCollide(self.ajustesSonidoRect):
            if not self.soundPlayed:
                playSound(botonSound)
                self.soundPlayed = True
            endPos = self.mouse.getPosition()
            if not self.ajustesSonidoPress and press and Raton.collides(iniPos[0], iniPos[1], self.ajustesSonidoRect):
                self.ajustesSonidoPress = True
            elif self.mouse.getClick() and self.ajustesSonidoPress and Raton.collides(endPos[0], endPos[1], self.ajustesSonidoRect):
                #print("Seleccionado exit")
                Utils.state = System_State.SETTINGS
                stopMusic()
                self.ajustesSonidoPress = False

        elif self.mouse.isCollide(self.ajustesAtajosRect):
            if not self.soundPlayed:
                playSound(botonSound)
                self.soundPlayed = True
            endPos = self.mouse.getPosition()
            if not self.ajustesAtajosPress and press and Raton.collides(iniPos[0], iniPos[1], self.ajustesAtajosRect):
                self.ajustesAtajosPress = True
            elif self.mouse.getClick() and self.ajustesAtajosPress and Raton.collides(endPos[0], endPos[1], self.ajustesAtajosRect):
                #print("Seleccionado exit")
                Utils.state = System_State.SETTINGS
                stopMusic()
                self.ajustesAtajosPress = False

        else:
            self.soundPlayed = False

        if self.mouse.getClick():
            self.exitPress = False
            self.singlePress = False

        self.idSingle = (self.idSingle + frame(5)) % SINGLE_PLAYER_N
        self.idExit = (self.idExit + frame(5)) % EXIT_N
        self.idSingleSelected = (self.idSingleSelected + frame(5)) % SINGLE_PLAYER_FB_N
        self.idExitSelected = (self.idExitSelected + frame(5)) % EXIT_FB_N
        
    def updateGameMenuPos(self):
        #self.gameSelect = pg.transform.scale(self.gameSelect, (Utils.ScreenHeight*SCREEN_SCALE, Utils.ScreenHeight))
        self.aceptarRect = pg.Rect(Utils.ScreenWidth/2 - ACEPTAR_POS[0], Utils.ScreenHeight/2 - ACEPTAR_POS[1], ACEPTAR_RECT[0], ACEPTAR_RECT[1])
        self.aceptarNoPulsabeSurf = pygame.Surface((self.aceptarRect.w, self.aceptarRect.h), pygame.SRCALPHA)
        self.aceptarNoPulsabeSurf.fill((0,0,0,128))
        self.cancelarRect = pg.Rect(Utils.ScreenWidth/2 - CANCELAR_POS[0], Utils.ScreenHeight/2 - CANCELAR_POS[1], 250, 40)
        self.nuevaPartidaRect = pg.Rect(Utils.ScreenWidth/2 - NUEVA_PARTIDA_POS[0], Utils.ScreenHeight/2 - NUEVA_PARTIDA_POS[1], 250, 40)
        
        aux = []
        pad = 0
        for partidas in self.partidas:
            auxpartida = {
                'nombre': partidas['nombre'],
                'rect': pg.Rect(Utils.ScreenWidth/2 - PARTIDA_POS[0], Utils.ScreenHeight/2 - PARTIDA_POS[1] + YPARTIDA_PAD*pad, 455, YPARTIDA_PAD-1),
                'pressed': partidas['pressed']
                }
            aux.append(auxpartida)
            pad += 1
        self.partidas = aux
        
    def updateGameMenu(self, escena, raton, camera):
        self.updateGameMenuPos()
        press, iniPos = self.mouse.getPressed()
        #Boton aceptar
        #print(self.mouse.isCollide(self.nuevaPartidaRect), self.mouse.real_pos, self.aceptarRect.x, self.aceptarRect.y, self.aceptarRect.w, self.aceptarRect.h )
        if self.mouse.isCollide(self.aceptarRect) and self.selectedPartida != None:
            #print("acepar")
            if not self.soundPlayed:
                playSound(botonSound)
                self.soundPlayed = True
            endPos = self.mouse.getPosition()
            if not self.aceptarPress and press and Raton.collides(iniPos[0], iniPos[1], self.aceptarRect):
                self.aceptarPress = True
            elif self.mouse.getClick() and self.aceptarPress and Raton.collides(endPos[0], endPos[1], self.aceptarRect):
                #print("Aceptar")
                #Hay que hacer uno generico, o que carge el mapa y pase a ONGAME aqui
                _escena, _raton, _camera = loadFromSave(self.selectedPartida['nombre'])
                escena.setSelf(_escena)
                options = self.selectedPartida['nombre'].split("_")
                raza = None
                dif = None
                if options[0] == "4":
                    raza = Race.ZERG
                else:
                    if options[1] == "Zerg":
                        #print("Contra terran")
                        raza = Race.TERRAN
                    else:
                        #print("Contra zerg")
                        raza = Race.ZERG
                if options[2] == "Dificil":
                    #print("DIFICIL")
                    dif = HARD
                elif options[2] == "Normal":
                    #print("NORMAL")
                    dif = MEDIUM
                else:
                    #print("EASY")
                    dif = EASY
                if Utils.DEBBUG == False:
                    aI = AI(escena.p2, raza, dif)
                else:
                    aI = AI(escena.p2, raza, NULL)
                escena.aI = aI
                raton.setSelf(_raton)
                self.player = escena.p1
                self.enemy = escena.p2
                escena.raton = raton
                escena.p1.base.raton = escena.raton
                self.raton = escena.raton
                raton.addInterface(self)
                escena.interfaz = self
                camera.setSelf(_camera)
                escena.camera = camera
                Utils.state = System_State.ONGAME
                setGameState2(System_State.LOAD)
                escena.nombre = self.selectedPartida['nombre']
                self.selectedPartida = None
                self.escena = escena
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
                #print("Cancelar")
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
                #print("Nueva partida")
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
                    #print(partida['nombre'])
                    #Pasar a menu de nueva partida
                    self.selectedPartida = partida
                    playSound(botonSound2)
                    partida['pressed'] = False
        if self.mouse.getClick():
            self.aceptarPress = False
            self.cancelarPress = False
            self.nuevaPartidaPress = False
    
    def updateNewGamePos(self):
        #self.gameSelect = pg.transform.scale(self.gameSelect, (Utils.ScreenHeight*SCREEN_SCALE, Utils.ScreenHeight))
        self.aceptarRect = pg.Rect(Utils.ScreenWidth/2 - ACEPTAR_POS[0], Utils.ScreenHeight/2 - ACEPTAR_POS[1], ACEPTAR_RECT[0], ACEPTAR_RECT[1])
        self.aceptarNoPulsabeSurf = pygame.Surface((self.aceptarRect.w, self.aceptarRect.h), pygame.SRCALPHA)
        self.aceptarNoPulsabeSurf.fill((0,0,0,128))
        self.cancelarRect = pg.Rect(Utils.ScreenWidth/2 - CANCELAR_POS[0], Utils.ScreenHeight/2 - CANCELAR_POS[1], 250, 40)

        aux = [
            {"nombre": "1", "tipo": "mapa", "rect": pg.Rect(Utils.ScreenWidth/2 - MAPA1_POS[0], Utils.ScreenHeight/2 - MAPA1_POS[1], 90, 35), "press": self.botonesNewGame[0]['press']},
            {"nombre": "2", "tipo": "mapa", "rect": pg.Rect(Utils.ScreenWidth/2 - MAPA2_POS[0], Utils.ScreenHeight/2 - MAPA2_POS[1], 90, 35), "press": self.botonesNewGame[1]['press']},
            {"nombre": "3", "tipo": "mapa", "rect": pg.Rect(Utils.ScreenWidth/2 - MAPA3_POS[0], Utils.ScreenHeight/2 - MAPA3_POS[1], 90, 35), "press": self.botonesNewGame[2]['press']},
            {"nombre": "4", "tipo": "mapa", "rect": pg.Rect(Utils.ScreenWidth/2 - MAPA4_POS[0], Utils.ScreenHeight/2 - MAPA4_POS[1], 90, 35), "press": self.botonesNewGame[3]['press']},
            {"nombre": "Facil", "tipo": "dificultad", "rect": pg.Rect(Utils.ScreenWidth/2 - FACIL_POS[0], Utils.ScreenHeight/2 - FACIL_POS[1], 125, 35), "press": self.botonesNewGame[4]['press'], "dif": EASY},
            {"nombre": "Normal", "tipo": "dificultad", "rect": pg.Rect(Utils.ScreenWidth/2 - NORMAL_POS[0], Utils.ScreenHeight/2 - NORMAL_POS[1], 125, 35), "press": self.botonesNewGame[5]['press'], "dif": MEDIUM},
            {"nombre": "Dificil", "tipo": "dificultad", "rect": pg.Rect(Utils.ScreenWidth/2 - DIFICIL_POS[0], Utils.ScreenHeight/2 - DIFICIL_POS[1], 125, 35), "press": self.botonesNewGame[6]['press'], "dif": HARD},
            {"nombre": "Terran", "tipo": "raza", "rect": pg.Rect(Utils.ScreenWidth/2 - TERRAN_POS[0], Utils.ScreenHeight/2 - TERRAN_POS[1], 185, 35), "press": self.botonesNewGame[7]['press'], "raza": Race.TERRAN},
            {"nombre": "Zerg","tipo": "raza", "rect": pg.Rect(Utils.ScreenWidth/2 - ZERG_POS[0], Utils.ScreenHeight/2 - ZERG_POS[1], 185, 35), "press": self.botonesNewGame[8]['press'], "raza": Race.ZERG},
        ]
        
        self.botonesNewGame = aux
        
    def updateNewGame(self, escena, raton, camera):
        self.updateNewGamePos()
        press, iniPos = self.mouse.getPressed()
        #Boton aceptar
        if self.mouse.isCollide(self.aceptarRect):
            if not self.soundPlayed:
                playSound(botonSound)
                self.soundPlayed = True
            endPos = self.mouse.getPosition()
            if not self.aceptarPress and press and Raton.collides(iniPos[0], iniPos[1], self.aceptarRect):
                self.aceptarPress = True
            elif self.mouse.getClick() and self.aceptarPress and Raton.collides(endPos[0], endPos[1], self.aceptarRect):
                #Con self.selectedMap selectedDif selectedRaza se crea la partida
                _escena, _raton, _camera = loadHardcodedMap(self.selectedMap + "_" + self.selectedRaza["nombre"])
                escena.setSelf(_escena)
                raza = None
                if self.selectedMap == "4":
                    raza = Race.ZERG
                else:
                    if self.selectedRaza['raza'] == Race.TERRAN:
                        raza = Race.ZERG
                    else:
                        raza = Race.TERRAN
                if Utils.DEBBUG == False:
                    aI = AI(escena.p2, raza, self.selectedDif['dif'])
                else:
                    aI = AI(escena.p2, raza, NULL)
                escena.aI = aI
                raton.setSelf(_raton)
                self.player = escena.p1
                #print(self.player.limitUnits)
                self.enemy = escena.p2
                escena.raton = raton
                escena.p1.base.raton = escena.raton
                self.raton = escena.raton
                raton.addInterface(self)
                escena.interfaz = self
                camera.setSelf(_camera)
                escena.camera = camera
                id = self.getNumPartidas()
                escena.nombre = self.selectedMap + "_" + self.selectedRaza["nombre"] + "_" + self.selectedDif['nombre'] + "_" + str(id)
                Utils.state = System_State.ONGAME
                setGameState2(System_State.LOAD)
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
                #print("Cancelar")
                Utils.state = System_State.GAMESELECT
                self.cancelarPress = False
        else:
            self.soundPlayed = False

        
        if self.botonRazaTerran in self.botonesNewGame and self.selectedMap == "4":
            self.botonesNewGame.remove(self.botonRazaTerran)
            self.selectedRaza = {"nombre":"Zerg", "raza": Race.ZERG}
        elif self.botonRazaTerran not in self.botonesNewGame and self.selectedMap != "4":
            self.botonesNewGame.append(self.botonRazaTerran)
        for b in self.botonesNewGame:
            if self.mouse.isCollide(b['rect']):
                endPos = self.mouse.getPosition()
                if not b['press'] and press and Raton.collides(iniPos[0], iniPos[1], b['rect']):
                    b['press'] = True
                elif self.mouse.getClick() and b['press'] and Raton.collides(endPos[0], endPos[1], b['rect']):
                    #print(b['nombre'])
                    playSound(botonSound2)
                    b['press'] = False
                    if b['tipo'] == "mapa":
                        self.selectedMap = b['nombre']
                    elif b['tipo'] == "dificultad":
                        self.selectedDif['nombre'] = b['nombre']
                        self.selectedDif['dif'] = b['dif']
                    elif b['tipo'] == "raza":
                        self.selectedRaza['nombre'] = b['nombre']
                        self.selectedRaza['raza'] = b['raza']



        if self.mouse.getClick():
            self.aceptarPress = False
            self.cancelarPress = False
            
    def updateOnGame(self):
        #si esta en GUI desactivar funciones de raton
        self.escena.update()
        if getGameState2() == System_State.PLAYING or getGameState2() == System_State.LOAD:
            
            self.updatePLAY()
        
        elif getGameState2() == System_State.HELP:
            
            self.updateHELP()
            
        elif getGameState2() == System_State.PAUSED:
        
            self.updatePAUSED()
            
        if frame(10):
            self.heroeIndex = (self.heroeIndex+1)%HEROE_N
    
    def updateHELP(self):
        self.mouse.setEnable(False)
        self.helpButtons =  self.getHelpButton()
    
    def updatePAUSED(self):
        pass
            
    def updatePLAY(self):
        
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
                
    def updateHELP(self):
        self.mouse.setEnable(False)
        self.helpButtons = [None, None, None]
        self.helpButtons[2] = self.allButton[Options.CLOSE]
        if self.helpPage > 0:
            self.helpButtons[0] = self.allButton[Options.PREVIOUS_PAGE]
        if self.helpPage < len(self.helpPageSprites)-1:
            self.helpButtons[1] = self.allButton[Options.NEXT_PAGE]
                
    def draw(self, screen, camera):
        if Utils.state == System_State.MAINMENU:
            screen.blit(self.mainMenu, [Utils.ScreenWidth/2 - self.mainMenu.get_width()/2, 0])

            #Boton single player
            if self.mouse.isCollide(self.singleRect):
                screen.blit(self.singleSelected[self.idSingleSelected], [Utils.ScreenWidth/2 - SINGLE_PLAYER_FB_POS[0], Utils.ScreenHeight/2 - SINGLE_PLAYER_FB_POS[1]])
                screen.blit(self.single[self.idSingle], [Utils.ScreenWidth/2 - SINGLE_PLAYER_POS[0], Utils.ScreenHeight/2 - SINGLE_PLAYER_POS[1]])
                muestra_texto(screen, 'monotypecorsiva', "Un jugador", GREEN2, MAIN_MENU_TEXT_SIZE, [Utils.ScreenWidth/2 - SINGLE_TEXT_POS[0], Utils.ScreenHeight/2 - SINGLE_TEXT_POS[1]])
            else:
                screen.blit(self.single[self.idSingle], [Utils.ScreenWidth/2 - SINGLE_PLAYER_POS[0], Utils.ScreenHeight/2 - SINGLE_PLAYER_POS[1]])
                muestra_texto(screen, 'monotypecorsiva', "Un jugador", GREEN3, MAIN_MENU_TEXT_SIZE, [Utils.ScreenWidth/2 - SINGLE_TEXT_POS[0], Utils.ScreenHeight/2 - SINGLE_TEXT_POS[1]])
            #screen.blit(self.single[self.idSingle], SINGLE_PLAYER_POS)

            #Boton Exit
            screen.blit(self.exit[self.idExit], [Utils.ScreenWidth/2 - EXIT_POS[0], Utils.ScreenHeight/2 - EXIT_POS[1]])
            if self.mouse.isCollide(self.exitRect):
                screen.blit(self.exitSelected[self.idExitSelected], [Utils.ScreenWidth/2 - EXIT_FB_POS[0], Utils.ScreenHeight/2 - EXIT_FB_POS[1]])
                muestra_texto(screen, str('monotypecorsiva'), "Salir", GREEN2, MAIN_MENU_TEXT_SIZE, [Utils.ScreenWidth/2 - EXIT_TEXT_POS[0], Utils.ScreenHeight/2 - EXIT_TEXT_POS[1]])
            else:
                muestra_texto(screen, str('monotypecorsiva'), "Salir", GREEN3, MAIN_MENU_TEXT_SIZE, [Utils.ScreenWidth/2 - EXIT_TEXT_POS[0], Utils.ScreenHeight/2 - EXIT_TEXT_POS[1]])

            #Boton ajustes
            if self.mouse.isCollide(self.ajustesSonidoRect):
                pg.draw.rect(screen, BLUE, (Utils.ScreenWidth/2 - AJUSTES_SONIDO_TEXT_POS[0], Utils.ScreenHeight/2 - AJUSTES_SONIDO_TEXT_POS[1], 220, 40), 3)
                muestra_texto(screen, str('monotypecorsiva'), "Ajustes de sonido", GREEN2, MAIN_MENU_TEXT_SIZE + 5, [Utils.ScreenWidth/2 - AJUSTES_SONIDO_TEXT_POS[0], Utils.ScreenHeight/2 - AJUSTES_SONIDO_TEXT_POS[1]])
            else:
                muestra_texto(screen, str('monotypecorsiva'), "Ajustes de sonido", GREEN3, MAIN_MENU_TEXT_SIZE + 5, [Utils.ScreenWidth/2 - AJUSTES_SONIDO_TEXT_POS[0], Utils.ScreenHeight/2 - AJUSTES_SONIDO_TEXT_POS[1]])

            if self.mouse.isCollide(self.ajustesAtajosRect):
                pg.draw.rect(screen, BLUE, (Utils.ScreenWidth/2 - AJUSTES_ATAJOS_TEXT_POS[0], Utils.ScreenHeight/2 - AJUSTES_ATAJOS_TEXT_POS[1], 220, 40), 3)
                muestra_texto(screen, str('monotypecorsiva'), "Atajos de teclado", GREEN2, MAIN_MENU_TEXT_SIZE + 5, [Utils.ScreenWidth/2 - AJUSTES_ATAJOS_TEXT_POS[0], Utils.ScreenHeight/2 - AJUSTES_ATAJOS_TEXT_POS[1]])
            else:
                muestra_texto(screen, str('monotypecorsiva'), "Atajos de teclado", GREEN3, MAIN_MENU_TEXT_SIZE + 5, [Utils.ScreenWidth/2 - AJUSTES_ATAJOS_TEXT_POS[0], Utils.ScreenHeight/2 - AJUSTES_ATAJOS_TEXT_POS[1]])


        elif Utils.state == System_State.GAMESELECT:
            screen.blit(self.gameSelect, [Utils.ScreenWidth/2 - self.gameSelect.get_width()/2, Utils.ScreenHeight/2 - self.gameSelect.get_height()/2])

            if self.mouse.isCollide(self.aceptarRect) and self.selectedPartida != None:
                pygame.draw.rect(screen, GREEN3, self.aceptarRect, 2)
            elif self.selectedPartida == None:
                screen.blit(self.aceptarNoPulsabeSurf, [self.aceptarRect.x, self.aceptarRect.y])
            if self.mouse.isCollide(self.cancelarRect):
                pygame.draw.rect(screen, GREEN3, self.cancelarRect, 2)
            if self.mouse.isCollide(self.nuevaPartidaRect):
                pygame.draw.rect(screen, GREEN3, self.nuevaPartidaRect, 2)

            for partida in self.partidas:
                if self.mouse.isCollide(partida['rect']):
                    pygame.draw.rect(screen, GREEN2, partida['rect'], 1)
                if partida == self.selectedPartida:
                    pygame.draw.rect(screen, GREEN, partida['rect'], 2)
                muestra_texto(screen, str('monotypecorsiva'), partida['nombre'], WHITE, 28, (partida['rect'].x + 100, partida['rect'].y))
            if self.selectedPartida != None:
                info = self.selectedPartida['nombre'].split("_")
                muestra_texto(screen, str('monotypecorsiva'), info[0], WHITE, 40, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2-740), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2-170)))
                muestra_texto(screen, str('monotypecorsiva'), info[2], WHITE, 40, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2-810), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2-275)))
                muestra_texto(screen, str('monotypecorsiva'), info[1], WHITE, 40, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2-745), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2-390)))

        elif Utils.state == System_State.NEWGAME:
            screen.blit(self.newGame, [Utils.ScreenWidth/2 - self.newGame.get_width()/2, Utils.ScreenHeight/2 - self.newGame.get_height()/2])

            if (self.mouse.isCollide(self.aceptarRect) and
            (self.selectedMap != None or self.selectedDif != None or self.selectedRaza != None)):
                pygame.draw.rect(screen, GREEN3, self.aceptarRect, 2)
            elif self.selectedMap == None or self.selectedDif == None or self.selectedRaza == None:
                screen.blit(self.aceptarNoPulsabeSurf, ACEPTAR_POS)
            if self.mouse.isCollide(self.cancelarRect):
                pygame.draw.rect(screen, GREEN3, self.cancelarRect, 2)

            for b in self.botonesNewGame:
                if self.mouse.isCollide(b['rect']):
                    pygame.draw.rect(screen, GREEN2, b['rect'], 2)
                
                if (b['nombre'] == self.selectedMap or b['nombre'] == self.selectedDif['nombre'] 
                    or b['nombre'] == self.selectedRaza['nombre']):
                    pygame.draw.rect(screen, GREEN, b['rect'], 3)


            muestra_texto(screen, str('monotypecorsiva'), str(self.selectedMap), WHITE, 40, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2-740), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2-170)))
            muestra_texto(screen, str('monotypecorsiva'), self.selectedDif['nombre'], WHITE, 40, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2-810), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2-275)))
            muestra_texto(screen, str('monotypecorsiva'), self.selectedRaza['nombre'], WHITE, 40, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2-745), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2-390)))

        elif Utils.state == System_State.ONGAME:
            screen.blit(self.pauseButton.image, (0, 0))
            pygame.draw.rect(screen, BLUE, self.pauseRect, 1)
            if DEBBUG == True:
                muestra_texto(screen, str('monotypecorsiva'), str(round(Utils.SYSTEM_CLOCK / CLOCK_PER_SEC)), BLACK, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  20), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 20)))
                muestra_texto(screen, times, str(self.player.resources), BLUE, 30, (ScreenWidth - 40, 60))
                muestra_texto(screen, times, str(self.enemy.resources), RED, 30, (ScreenWidth - 40, 100))

            screen.blit(self.resources[0], (Utils.ScreenWidth - RESOURCES_COUNT_X, 3))
            muestra_texto(screen, times, str(self.player.resources), GREEN4, 30, (Utils.ScreenWidth - RESOURCES_COUNT_X + 40, 10))
            screen.blit(self.resources[1], (Utils.ScreenWidth - RESOURCES_COUNT_X + 100, 3))
            muestra_texto(screen, times, str(self.player.gas), GREEN4, 30, (Utils.ScreenWidth - RESOURCES_COUNT_X + 140, 10))
            screen.blit(self.resources[2], (Utils.ScreenWidth - RESOURCES_COUNT_X + 200, 3))
            muestra_texto(screen, times, str(self.player.units.__len__()) + "/" + str(self.player.limitUnits), GREEN4, 28, (Utils.ScreenWidth - RESOURCES_COUNT_X + 240, 10))

            screen.blit(self.gui, (Utils.ScreenWidth/2 - self.gui.get_width()/2, Utils.ScreenHeight - self.gui.get_height()))

            #draw minimapa
            pygame.draw.rect(screen, BLUE, pygame.Rect(Utils.ScreenWidth/2 - MINIMAP_X, Utils.ScreenHeight - MINIMAP_Y, MINIMAP_W, MINIMAP_H), 1)
            #self.player.mapa.drawMinimap(screen)
            self.player.drawEntity(screen, True)
            self.enemy.drawEntity(screen, False)

            pygame.draw.rect(screen, WHITE, pygame.Rect(Utils.ScreenWidth/2 - MINIMAP_X + (camera.x/self.player.mapa.w * MINIMAP_W), Utils.ScreenHeight - MINIMAP_Y + (camera.y/self.player.mapa.h * MINIMAP_H), camera.w/self.player.mapa.w * MINIMAP_W, camera.h/self.player.mapa.h * MINIMAP_H), 2)

            #informacion de entidades seleccionadas
            self.drawEntityInfo(screen, camera)

            #draw cara del heroe
            screen.blit(self.heroeSprites[self.heroeIndex], (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 - 672), Utils.ScreenHeight - (MIN_SCREEN_HEIGHT - 667)))

            #draw comandos de la entidad seleccionada
            opcion = 0
            for b in self.button:
                opcion += 1
                b.draw(screen, Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 - self.buttonX), Utils.ScreenHeight - (MIN_SCREEN_HEIGHT - self.buttonY))
                self.buttonX += BUTTONPADX
                if opcion % 3 == 0:
                    self.buttonY += BUTTONPADY
                    self.buttonX = BUTTON_X
                if opcion == 9:
                    break
                
            if getGameState2() == System_State.HELP:
                
                self.drawHELP(screen)
            elif getGameState2() == System_State.PAUSED:
                
                self.drawPause(screen)
                
            elif getGameState2() == System_State.GAMEOVER:
                if self.count2 < 10:
                    image = pg.transform.scale(self.heroeSprites[self.heroeIndex], [self.herow, self.heroh])
                    screen.blit(image, (672 - self.heropadx, 667- self.heropady))
                    self.heroeIndex = (self.heroeIndex+frame(8))%HEROE_N 
                    self.count2 += frame(30)
                    if self.heropadx < 670:
                        self.heropadx += 5
                    if self.heropady < 667:
                        self.heropady += 5
                    if self.herow < ScreenWidth:
                        self.herow += 7
                    if self.heroh < ScreenHeight:
                        self.heroh += 5
                        if self.heroh >= ScreenHeight:
                            playSound(loserSound)
                    else:
                        muestra_texto(screen, str('monotypecorsiva'), "???", YELLOW, 80, [800, 200])
                else:
                    screen.blit(self.loseSprite[self.index], (0, 0))
                    self.index += frame(5)
                    if self.index == 30:
                        if self.index == 30:
                            self.index = 10
            elif Utils.state2 == System_State.WIN:
                
                screen.blit(self.winSprite[self.index], (0, 0))
                self.index += frame(5)
                if self.index == 30:
                    self.index = 10
                    #setGameState(System_State.MAINMENU)
                    #setGameState2(System_State.PLAYING)
                if self.index >= 10:
                    muestra_texto(screen, str('monotypecorsiva'), "Victoria! tu tu tuu~ tu tu", YELLOW, 40, (ScreenWidth/2, ScreenHeight - 200))

    def drawHELP(self, screen):
        screen.blit(self.helpPageSprites[self.helpPage], (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  240), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 80)))
         
        self.helpButtons[2].draw(screen, Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 - 703), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 84))
        if self.helpPage > 0:
            self.helpButtons[0].draw(screen, Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 - 304), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 95))
        if self.helpPage < len(self.helpPageSprites)-1:
            self.helpButtons[1].draw(screen, Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 - 604), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 95))   
        '''
        if self.helpPage == 1:
            muestra_texto(screen, str('monotypecorsiva'), "INSTRUCCIONES", WHITE, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  370), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 110)))
            
            screen.blit(getSprite(MOUSE_PATH + "tile002.png", WHITE, (70, 70)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  310), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 200)))
            muestra_texto(screen, str('monotypecorsiva'), "Click Izquierdo", GREEN, 26, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 200)))
            muestra_texto(screen, str('monotypecorsiva'), "Para seleccionar unidades o realizar acciones", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 220)))
            muestra_texto(screen, str('monotypecorsiva'), "Click Derecho ", GREEN, 26, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 245)))
            muestra_texto(screen, str('monotypecorsiva'), "Para desplazar tropas", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 265)))
            
            screen.blit(getSprite(KEY_PATH , WHITE, (150, 100)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  260), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 320)))
            muestra_texto(screen, str('monotypecorsiva'), "Movimiento de camara", GREEN, 26, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 330)))
            muestra_texto(screen, str('monotypecorsiva'), "Utiliza las teclas para controlar la camara", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 360)))
            muestra_texto(screen, str('monotypecorsiva'), "o desde el minimapa usando el ratón", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 375)))
            
        elif self.helpPage == 4:
            muestra_texto(screen, str('monotypecorsiva'), "TERRAN", WHITE, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  425), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 90)))
            muestra_texto(screen, str('monotypecorsiva'), "ESTRUCUTURAS", WHITE, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  375), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 120)))
            
            screen.blit(getSprite(TERRAN_BUILDER_PATH + "4.png", WHITE, (100, 100)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  300), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 200)))
            muestra_texto(screen, str('monotypecorsiva'), "Centro de comandos", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 210)))
            muestra_texto(screen, str('monotypecorsiva'), "Es el edificio mas importante de los Terran,", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 240)))
            muestra_texto(screen, str('monotypecorsiva'), "puede contruir otras estructuras y entrenar", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 255)))
            muestra_texto(screen, str('monotypecorsiva'), "tropas obreras", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 270)))
            
            screen.blit(getSprite(TERRAN_BARRACKS_PATH + "4.png", WHITE, (100, 100)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  300), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 330)))
            muestra_texto(screen, str('monotypecorsiva'), "Cuartel Terran", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 340)))
            muestra_texto(screen, str('monotypecorsiva'), "En el cuartel se puede entrenar las unidades", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 370)))
            muestra_texto(screen, str('monotypecorsiva'), "ofensivas, construye mas cuarteles para", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 385)))
            muestra_texto(screen, str('monotypecorsiva'), "entrenar varias tropas a la vez!", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 400)))
            
            screen.blit(getSprite(TERRAN_DEPOT_PATH + "4.png", WHITE, (100, 100)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  300), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 460)))
            muestra_texto(screen, str('monotypecorsiva'), "Deposito de suministros", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 470)))
            muestra_texto(screen, str('monotypecorsiva'), "Donde se guarda los recursos, necesario", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 500)))
            muestra_texto(screen, str('monotypecorsiva'), "para mantener el ejercito, contruye para", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 515)))
            muestra_texto(screen, str('monotypecorsiva'), "aumentar el tamaño del ejercito", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 530)))
            
            screen.blit(getSprite(TERRAN_REFINERY_PATH + "4.png", BLACK, (150, 150)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  280), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 570)))
            muestra_texto(screen, str('monotypecorsiva'), "Refineria", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 600)))
            muestra_texto(screen, str('monotypecorsiva'), "Solo se puede contruir sobre un geyser,", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 630)))
            muestra_texto(screen, str('monotypecorsiva'), "sirve para la extraccion del geyser", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 645)))
            
        elif self.helpPage == 3:
            muestra_texto(screen, str('monotypecorsiva'), "TERRAN", WHITE, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  425), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 90)))
            muestra_texto(screen, str('monotypecorsiva'), "UNIDADES", WHITE, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 120)))
            
            spritesheet = pg.image.load("./sprites/scvJusto.bmp").convert()
            spritesheet.set_colorkey(BLACK)
            sprites = Entity.divideSpritesheetByRows(spritesheet, 72, 1.5)
            screen.blit(sprites[13], (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  280), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 200)))
            muestra_texto(screen, str('monotypecorsiva'), "SVC", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 210)))
            muestra_texto(screen, str('monotypecorsiva'), "Unidad obrera de los terran, se encargan", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 240)))
            muestra_texto(screen, str('monotypecorsiva'), "de la extracción de recursos, son débiles", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 255)))
            muestra_texto(screen, str('monotypecorsiva'), "poca vida y poco daño", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 270)))
            
            spritesheet = pg.image.load("./sprites/terran_soldier_sheet.bmp").convert()
            spritesheet.set_colorkey(WHITE)
            sprites = Entity.divideSpritesheetByRows(spritesheet, 64, 1.5)
            screen.blit(sprites[13], (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  290), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 330)))
            muestra_texto(screen, str('monotypecorsiva'), "Terran Marine", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 340)))
            muestra_texto(screen, str('monotypecorsiva'), "Unidad ofensiva basica de los terran, ", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 370)))
            muestra_texto(screen, str('monotypecorsiva'), "tienen bastante daño y atacan a distancia", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 385)))
            
            spritesheet = pg.image.load("./sprites/firebat.bmp").convert()
            spritesheet.set_colorkey(BLACK)
            sprites = Entity.divideSpritesheetByRows(spritesheet, 32, 1.5)
            screen.blit(sprites[13], (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  315), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 480)))
            muestra_texto(screen, str('monotypecorsiva'), "FireBat", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 470)))
            muestra_texto(screen, str('monotypecorsiva'), "Unidad ofensiva avanzada de los terran,", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 500)))
            muestra_texto(screen, str('monotypecorsiva'), "se caracteriza por el daño en area", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 515)))
            
            spritesheet = pg.image.load("./sprites/goliath.bmp").convert()
            spritesheet.set_colorkey(WHITE)
            sprites = Entity.divideSpritesheetByRows(spritesheet, 76, 1.4)
            screen.blit(sprites[13], (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  290), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 590)))
            muestra_texto(screen, str('monotypecorsiva'), "Goliat", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 600)))
            muestra_texto(screen, str('monotypecorsiva'), "Unidad ofensiva avanzada de los terran,", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 630)))
            muestra_texto(screen, str('monotypecorsiva'), "tienen una gran resistencia, pero es muy", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 645)))
            muestra_texto(screen, str('monotypecorsiva'), "lento, y ataca a melee", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 660)))
            
        elif self.helpPage == 2:
            muestra_texto(screen, str('monotypecorsiva'), "RECURSOS", WHITE, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 110)))
            
            spritesheet = pg.image.load("./SPRITE/Cristal/min01.bmp").convert()
            spritesheet.set_colorkey((BLACK))
            sprites = divideSpritesheetByRows(spritesheet, 96, 1.3)
            #self.image = self.sprites[4 - int(float(capacidad)/float(self.interval) + 0.5)]
            image = sprites[0]
            screen.blit(pg.transform.scale(image, (100, 150)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  300), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 190)))
            muestra_texto(screen, str('monotypecorsiva'), "Mineral cristal", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 210)))
            muestra_texto(screen, str('monotypecorsiva'), "Recurso esencial para todo tipo de tareas,", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 240)))
            muestra_texto(screen, str('monotypecorsiva'), "necesario para contruccion, entrenamiento", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 255)))
            muestra_texto(screen, str('monotypecorsiva'), "y mejoras", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 270)))
            
            spritesheet = pg.image.load("./sprites/geyser.bmp").convert()
            spritesheet.set_colorkey((BLACK))
            sprites = divideSpritesheetByRows(spritesheet, 64, 1.3)
            #self.image = self.sprites[4 - int(float(capacidad)/float(self.interval) + 0.5)]
            image = sprites[0]
            screen.blit(pg.transform.scale(image, (120, 80)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  300), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 340)))
            muestra_texto(screen, str('monotypecorsiva'), "Geyser", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 340)))
            muestra_texto(screen, str('monotypecorsiva'), "Gas con energia misteriosa, necesario para", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 370)))
            muestra_texto(screen, str('monotypecorsiva'), "entreno y mejoras avanzadas. Necesita una", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 385)))
            muestra_texto(screen, str('monotypecorsiva'), "estructura especial para poder extraerlo", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 400)))

        elif self.helpPage == 5:
            muestra_texto(screen, str('monotypecorsiva'), "ZERG", WHITE, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  430), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 90)))
            muestra_texto(screen, str('monotypecorsiva'), "ESTRUCUTURAS", WHITE, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  375), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 120)))
            
            screen.blit(getSprite(HATCHERY_PATH + "3.png", BLUE2, (150, 150)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  260), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 160)))
            muestra_texto(screen, str('monotypecorsiva'), "Criadero", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 210)))
            muestra_texto(screen, str('monotypecorsiva'), "Es la estructura mas importante de los Zerg,", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 240)))
            muestra_texto(screen, str('monotypecorsiva'), "puede contruir otras estructuras y entrenar", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 255)))
            muestra_texto(screen, str('monotypecorsiva'), "tropas obreras", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 270)))
            
            screen.blit(getSprite(ZERG_BARRACKS_PATH + "2.png", BLUE2, (90, 90)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  305), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 340)))
            muestra_texto(screen, str('monotypecorsiva'), "Colmena", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 340)))
            muestra_texto(screen, str('monotypecorsiva'), "En la Colmena se puede entrenar las unidades", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 370)))
            muestra_texto(screen, str('monotypecorsiva'), "ofensivas, construye mas Colmenas para", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 385)))
            muestra_texto(screen, str('monotypecorsiva'), "entrenar varias unidades a la vez!", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 400)))
            
            screen.blit(getSprite(SUPPLY_ZERG_PATH + "2.png", BLUE2, (100, 100)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  310), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 460)))
            muestra_texto(screen, str('monotypecorsiva'), "Guarida", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 470)))
            muestra_texto(screen, str('monotypecorsiva'), "Vital para mantener a las crias de Zerg", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 500)))
            muestra_texto(screen, str('monotypecorsiva'), "necesario para aumentar la poblacion", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 515)))
            
            screen.blit(getSprite(EXTRACTOR_PATH + "2.png", BLUE2, (90, 90)), (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  300), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 590)))
            muestra_texto(screen, str('monotypecorsiva'), "Extractor", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 600)))
            muestra_texto(screen, str('monotypecorsiva'), "Solo se puede contruir sobre un geyser,", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 630)))
            muestra_texto(screen, str('monotypecorsiva'), "y realiza la extracción del geyser", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 645)))
        
        elif self.helpPage == 6:
            muestra_texto(screen, str('monotypecorsiva'), "ZERG", WHITE, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  430), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 90)))
            muestra_texto(screen, str('monotypecorsiva'), "UNIDADES", WHITE, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 120)))
            
            spritesheet = pg.image.load("./sprites/drone.bmp").convert()
            spritesheet.set_colorkey(BLACK)
            sprites = Entity.divideSpritesheetByRows(spritesheet, 128, 1.5)
            screen.blit(sprites[13], (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  240), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 160)))
            muestra_texto(screen, str('monotypecorsiva'), "Drone", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 210)))
            muestra_texto(screen, str('monotypecorsiva'), "Unidad obrera de los zerg, se encargan", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 240)))
            muestra_texto(screen, str('monotypecorsiva'), "de la extracción de recursos, son débiles", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 255)))
            muestra_texto(screen, str('monotypecorsiva'), "poca vida y poco daño", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 270)))
            
            spritesheet = pg.image.load("./sprites/zergling.bmp").convert()
            spritesheet.set_colorkey(BLACK)
            sprites = Entity.divideSpritesheetByRows(spritesheet, 128, 1.5)
            screen.blit(sprites[13], (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  245), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 280)))
            muestra_texto(screen, str('monotypecorsiva'), "Zergling", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 340)))
            muestra_texto(screen, str('monotypecorsiva'), "Unidad ofensiva basica de los Zerg, son", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 370)))
            muestra_texto(screen, str('monotypecorsiva'), "muy rapidas", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 385)))
            
            spritesheet = pg.image.load("./sprites/broodling.bmp").convert()
            spritesheet.set_colorkey(BLACK)
            sprites = Entity.divideSpritesheetByRows(spritesheet, 48, 1.8)
            screen.blit(sprites[13], (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  300), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 470)))
            muestra_texto(screen, str('monotypecorsiva'), "Broodling", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 470)))
            muestra_texto(screen, str('monotypecorsiva'), "Unidad ofensiva avanzada de los Zerg,", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 500)))
            muestra_texto(screen, str('monotypecorsiva'), "es rapida y tiene mucho daño", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 515)))
            
            spritesheet = pg.image.load("./sprites/hydralisk.bmp").convert()
            spritesheet.set_colorkey(BLACK)
            sprites = Entity.divideSpritesheetByRows(spritesheet, 128, 1.8)
            screen.blit(sprites[13], (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  235), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 540)))
            muestra_texto(screen, str('monotypecorsiva'), "Hydralisk", GREEN, 30, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  410), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 600)))
            muestra_texto(screen, str('monotypecorsiva'), "Unidad ofensiva avanzada de los Zerg,", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 630)))
            muestra_texto(screen, str('monotypecorsiva'), "tienen alta resistencia, es lento y", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 645)))
            muestra_texto(screen, str('monotypecorsiva'), "ataca a distancia", ORANGE, 20, (Utils.ScreenWidth/2 - (MIN_SCREEN_WIDTH/2 -  420), Utils.ScreenHeight/2 - (MIN_SCREEN_HEIGHT/2 - 660)))
        '''    
    def drawPause(self, screen):
        pygame.draw.rect(screen, BLACK, pygame.Rect(Utils.ScreenWidth/4, Utils.ScreenHeight/9, Utils.ScreenWidth/2, Utils.ScreenHeight/1.9))
        pygame.draw.rect(screen, BLUE2, pygame.Rect(Utils.ScreenWidth/4, Utils.ScreenHeight/9, Utils.ScreenWidth/2, Utils.ScreenHeight/1.9), 4)
        pygame.draw.rect(screen, BLUE2, self.helpPauseRect, 1)
        screen.blit(self.exitPauseButton.image, (self.exitPauseRect.x, self.exitPauseRect.y))
        screen.blit(self.helpPauseButton.image, (self.helpPauseRect.x, self.helpPauseRect.y))
        self.saveButton.draw(screen, 400,200)
        self.saveAndExitButton.draw(screen, 400, 290)
        self.exitButton.draw(screen, 400, 380)
        muestra_texto(screen, str('monotypecorsiva'), "MENU DE PAUSA", WHITE, 30, (490, 120))
        muestra_texto(screen, str('monotypecorsiva'), "Guardar", GREEN, 26, (480, 210))
        muestra_texto(screen, str('monotypecorsiva'), "Guardar y Salir", GREEN, 26, (480, 300))
        muestra_texto(screen, str('monotypecorsiva'), "Salir sin guardar", GREEN, 26, (480, 390))
    
    def drawEntityInfo(self, screen, camera):
        if len(self.player.unitsSelected) == 1:
            upgrades = self.getUpgrades(self.player.unitsSelected[0].getUpgrades())
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
                screen.blit(image, (Utils.ScreenWidth/2 - GUI_INFO_X + x, Utils.ScreenHeight - GUI_INFO_Y + 5 + y))
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
                screen.blit(image, (Utils.ScreenWidth/2 - GUI_INFO_X + x, Utils.ScreenHeight - GUI_INFO_Y + 5 + y))
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

            screen.blit(image, (Utils.ScreenWidth/2 - GUI_INFO_X, Utils.ScreenHeight - GUI_INFO_Y))
            muestra_texto(screen, 'monotypecorsiva', capacity, YELLOW, 20, [Utils.ScreenWidth/2 - GUI_INFO_X + 60, Utils.ScreenHeight - GUI_INFO_Y + 135])
            self.player.resourceSelected.drawInfo(screen, YELLOW)

    def showInfo(self, screen, unit, color, renderX = 0, renderY = 0, hpX = 0, hpY = 0, upgrades = None):
        image = unit.getRender()
        hpState = str(unit.getHP()) + "/" + str(unit.getMaxHP())
        x = self.upgradeX
        if upgrades != None: #Dibujar las upgrades
            for upgrade in upgrades:
                upgrade.draw(screen, x, self.upgradeY)
                x += UPGRADEPADX
        screen.blit(image, (Utils.ScreenWidth/2 - GUI_INFO_X + renderX, Utils.ScreenHeight - GUI_INFO_Y + renderY))
        muestra_texto(screen, 'monotypecorsiva', hpState, color, 20, [Utils.ScreenWidth/2 - GUI_INFO_X + hpX, Utils.ScreenHeight -  GUI_INFO_Y + hpY])
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
                self.allButton[e].costeMineral = self.player.structureSelected.damageMineralUpCost
                self.allButton[e].costeGas = self.player.structureSelected.damageGasUpCost
                self.allButton[e].nextLevel = int(self.player.structureSelected.damageMineralUpCost / 25 - 1)
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
