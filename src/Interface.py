
import pygame as pg
from . import Player, Command, Utils, Raton, Button
from src.Music import *
from src.Lib import *
from src.Utils import *

class Interface():
    buttonX = 0
    buttonY = 0
    
    def __init__(self, player, enemy, mouse):
        self.player = player
        self.enemy = enemy
        self.mouse = mouse
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
    
    def loadAllButton(self):
        allButton = {}
        aux = Button.Button(BUTTON_PATH + "barracks" + ".bmp", Command.CommandId.BUILD_BARRACKS)
        allButton[Options.BUILD_BARRACKS] = aux
        aux = Button.Button(BUTTON_PATH + "worker" + ".bmp", Command.CommandId.GENERATE_WORKER)
        allButton[Options.GENERATE_WORKER] = aux
        aux = Button.Button(BUTTON_PATH + "soldier" + ".bmp", Command.CommandId.GENERATE_SOLDIER)
        allButton[Options.GENERATE_SOLDIER] = aux
        aux = Button.Button(BUTTON_PATH + "soldier" + ".bmp", Command.CommandId.BUILD_HATCHERY)
        allButton[Options.BUILD_HATCHERY] = aux
        aux = Button.Button(BUTTON_PATH + "refinery" + ".bmp", Command.CommandId.BUILD_REFINERY)
        allButton[Options.BUILD_REFINERY] = aux
        aux = Button.Button(BUTTON_PATH + "danyoUpgrade" + ".png", Command.CommandId.UPGRADE_SOLDIER_DAMAGE)
        allButton[Options.DANYO_UPGRADE] = aux
        return allButton
    
    def update(self):
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
                    Utils.state = System_State.MAP1
                    stopMusic()
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
            self.showInfo(screen, self.player.unitsSelected[0], GREEN3, 10, 10, 60, 135)
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
            
    def showInfo(self, screen, unit, color, renderX = 0, renderY = 0, hpX = 0, hpY = 0):
        image = unit.getRender()
        hpState = str(unit.getMaxHP()) + "/" + str(unit.getHP())
            
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
            if e != Options.NULO:
                buttons.append(self.allButton[e])
        return buttons
    
        
                
            