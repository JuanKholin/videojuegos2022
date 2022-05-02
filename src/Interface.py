
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
        
        self.gui = pg.image.load(BARRA_COMANDO + ".bmp")
        self.gui = pg.transform.scale(self.gui, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.gui.set_colorkey(BLACK)
        
        self.allButton = self.loadAllButton()
        
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
    
    def loadAllButton(self):
        allButton = []
        aux = Button.Button(BUTTON_PATH + "barracks" + ".bmp", Command.CommandId.BUILD_BARRACKS)
        allButton.append(aux)
        aux = Button.Button(BUTTON_PATH + "worker" + ".bmp", Command.CommandId.GENERATE_WORKER)
        allButton.append(aux)
        aux = Button.Button(BUTTON_PATH + "soldier" + ".bmp", Command.CommandId.GENERATE_SOLDIER)
        allButton.append(aux)
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
                self.buttonX = Utils.BUTTON_X
                self.buttonY = Utils.BUTTON_Y
                
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
            muestra_texto(screen, str('monotypecorsiva'), str(round(Utils.SYSTEM_CLOCK / CLOCK_PER_SEC)), BLACK, 30, (20, 20))
            muestra_texto(screen, times, str(self.player.resources), BLACK, 30, (SCREEN_WIDTH - 40, 20))
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
                self.buttonX += Utils.BUTTONPADX
                if opcion % 3 == 0:
                    self.buttonY += Utils.BUTTONPADY
                    self.buttonX = Utils.BUTTON_X
                if opcion == 9:
                    break
    
    def drawEntityInfo(self, screen, camera):
        if len(self.player.unitsSelected) == 1:
            image = self.player.unitsSelected[0].getRender()
            screen.blit(image, (GUI_INFO_X + 10, GUI_INFO_Y + 20))
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
                    y = 100
                    x = 0
                if n == 8:
                    break
        elif self.player.structureSelected != None:
            image = self.player.structureSelected.getRender()
            screen.blit(image, (GUI_INFO_X, GUI_INFO_Y))
        elif self.player.resourceSelected != None:
            image = self.player.resourceSelected.getRender()
            screen.blit(image, (GUI_INFO_X, GUI_INFO_Y))
                
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
    
        
                
            