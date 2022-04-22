
import pygame
from . import Player, Command, Utils, Raton
from src.Music import *
from src.Lib import *
from src.Utils import *



class Interface():
    def __init__(self, player, mouse):
        self.player = player
        self.mouse = mouse
        self.mainMenu = pygame.image.load(MAIN_MENU + ".png")
        self.mainMenu = pygame.transform.scale(self.mainMenu, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.single = cargarSprites(SINGLE_PLAYER, SINGLE_PLAYER_N, True, BLACK, SINGLE_SIZE) 
        self.exit = cargarSprites(EXIT, EXIT_N, True, BLACK, EXIT_SIZE) 
        self.singleSelected = cargarSprites(SINGLE_PLAYER_FB, SINGLE_PLAYER_FB_N, True, BLACK, SINGLE_SIZE) 
        self.exitSelected = cargarSprites(EXIT_FB, EXIT_FB_N, True, BLACK, EXIT_SIZE)
        
        self.singleRect = pygame.Rect(SINGLE_PLAYER_POS[0], SINGLE_PLAYER_POS[1], self.single[0].get_width(), self.single[0].get_height())
        self.exitRect = pygame.Rect(EXIT_POS[0], EXIT_POS[1], self.exit[0].get_width(), self.exit[0].get_height())
        self.singlePress = False
        self.exitPress = False
        
        self.idExit = 0 
        self.idSingle = 0 
        self.idSingleSelected = 0 
        self.idExitSelected = 0 
        
        self.soundPlayed = False
    
    def update(self):
        if Utils.STATE == System_State.MAINMENU:
            
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
                    Utils.STATE = System_State.MAP1
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
                    Utils.STATE = System_State.EXIT
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
        
    def draw(self, screen):
        if Utils.STATE == System_State.MAINMENU:
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
                    
            
            
        if Utils.STATE == System_State.ONGAME:
            muestra_texto(screen, times, str(self.player.resources), BLACK, 30, (SCREEN_WIDTH - 40, 20))