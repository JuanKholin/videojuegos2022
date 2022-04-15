
import pygame
from . import Player, Command, Utils, Raton


class Interface():
    def __init__(self, player, mouse):
        self.player = player
        self.mouse = mouse
        self.mainMenu = pygame.image.load(Utils.MAIN_MENU + ".png")
        self.mainMenu = pygame.transform.scale(self.mainMenu, (Utils.SCREEN_WIDTH, Utils.SCREEN_HEIGHT))
        self.single = Utils.cargarSprites(Utils.SINGLE_PLAYER, Utils.SINGLE_PLAYER_N, True, Utils.BLACK, Utils.SINGLE_SIZE) 
        self.exit = Utils.cargarSprites(Utils.EXIT, Utils.EXIT_N, True, Utils.BLACK, Utils.EXIT_SIZE) 
        self.singleSelected = Utils.cargarSprites(Utils.SINGLE_PLAYER_FB, Utils.SINGLE_PLAYER_FB_N, True, Utils.BLACK, Utils.SINGLE_SIZE) 
        self.exitSelected = Utils.cargarSprites(Utils.EXIT_FB, Utils.EXIT_FB_N, True, Utils.BLACK, Utils.EXIT_SIZE)
        
        self.singleRect = pygame.Rect(Utils.SINGLE_PLAYER_POS[0], Utils.SINGLE_PLAYER_POS[1], self.single[0].get_width(), self.single[0].get_height())
        self.exitRect = pygame.Rect(Utils.EXIT_POS[0], Utils.EXIT_POS[1], self.exit[0].get_width(), self.exit[0].get_height())
        self.singlePress = False
        self.exitPress = False
        
        self.idExit = 0 
        self.idSingle = 0 
        self.idSingleSelected = 0 
        self.idExitSelected = 0 
    
    def update(self):
        if Utils.STATE == Utils.System_State.MAINMENU:
            
            press, iniPos = self.mouse.getPressed()
            #Boton single player
            if self.mouse.isCollide(self.singleRect):
                endPos = self.mouse.getPosition()
                if not self.singlePress and press and Raton.collides(iniPos[0], iniPos[1], self.singleRect):
                    self.singlePress = True
                elif self.mouse.getClick() and self.singlePress and Raton.collides(endPos[0], endPos[1], self.singleRect):
                    print("Seleccionado single player")
                    Utils.STATE = Utils.System_State.MAP1
                    self.singlePress = False
                
            if self.mouse.isCollide(self.exitRect):
                endPos = self.mouse.getPosition()
                if not self.exitPress and press and Raton.collides(iniPos[0], iniPos[1], self.exitRect):
                    self.exitPress = True
                elif self.mouse.getClick() and self.exitPress and Raton.collides(endPos[0], endPos[1], self.exitRect):
                    print("Seleccionado exit")
                    Utils.STATE = Utils.System_State.EXIT
                    self.exitPress = False
                    
            if self.mouse.getClick():
                self.exitPress = False
                self.singlePress = False
                
            self.idSingle = (self.idSingle + Utils.frame(5)) % Utils.SINGLE_PLAYER_N
            self.idExit = (self.idExit + Utils.frame(5)) % Utils.EXIT_N
            self.idSingleSelected = (self.idSingleSelected + Utils.frame(5)) % Utils.SINGLE_PLAYER_FB_N
            self.idExitSelected = (self.idExitSelected + Utils.frame(5)) % Utils.EXIT_FB_N
        
    def draw(self, screen):
        if Utils.STATE == Utils.System_State.MAINMENU:
            screen.blit(self.mainMenu, [0, 0])
            
            #Boton single player
            if self.mouse.isCollide(self.singleRect):
                screen.blit(self.singleSelected[self.idSingleSelected], Utils.SINGLE_PLAYER_FB_POS)
                screen.blit(self.single[self.idSingle], Utils.SINGLE_PLAYER_POS)
                Utils.muestra_texto(screen, 'monotypecorsiva', "single player", Utils.GREEN2, Utils.MAIN_MENU_TEXT_SIZE, Utils.SINGLE_TEXT_POS)
            else: 
                screen.blit(self.single[self.idSingle], Utils.SINGLE_PLAYER_POS)
                Utils.muestra_texto(screen, 'monotypecorsiva', "single player", Utils.GREEN3, Utils.MAIN_MENU_TEXT_SIZE, Utils.SINGLE_TEXT_POS)
            #screen.blit(self.single[self.idSingle], Utils.SINGLE_PLAYER_POS)
            
            #Boton Exit
            screen.blit(self.exit[self.idExit], Utils.EXIT_POS)
            if self.mouse.isCollide(self.exitRect):
                screen.blit(self.exitSelected[self.idExitSelected], Utils.EXIT_FB_POS)
                Utils.muestra_texto(screen, str('monotypecorsiva'), "exit", Utils.GREEN2, Utils.MAIN_MENU_TEXT_SIZE, Utils.EXIT_TEXT_POS)
            else:
                Utils.muestra_texto(screen, str('monotypecorsiva'), "exit", Utils.GREEN3, Utils.MAIN_MENU_TEXT_SIZE, Utils.EXIT_TEXT_POS)
                    
            
            
        if Utils.STATE == Utils.System_State.ONGAME:
            Utils.muestra_texto(screen, Utils.times, str(self.player.resources), Utils.BLACK, 30, (Utils.SCREEN_WIDTH - 40, 20))