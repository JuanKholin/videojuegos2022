
import pygame
from . import Player, Command, Utils, Raton

consolas = pygame.font.match_font('consolas')
times = pygame.font.match_font('times')
arial = pygame.font.match_font('arial')
courier = pygame.font.match_font('courier')

def muestra_texto(pantalla,fuente,texto,color, dimensiones, x, y):
	tipo_letra = pygame.font.Font(fuente,dimensiones)
	superficie = tipo_letra.render(texto,True, color)
	rectangulo = superficie.get_rect()
	rectangulo.center = (x, y)
	pantalla.blit(superficie,rectangulo)

class Interface():
    def __init__(self, player, mouse):
        self.player = player
        self.mouse = mouse
        self.mainMenu = pygame.image.load(Utils.MAIN_MENU + ".png")
        self.mainMenu = pygame.transform.scale(self.mainMenu, (Utils.SCREEN_WIDTH, Utils.SCREEN_HEIGHT))
        self.single = Utils.cargarSprites(Utils.SINGLE_PLAYER, Utils.SINGLE_PLAYER_N, True, Utils.BLACK) 
        self.exit = Utils.cargarSprites(Utils.EXIT, Utils.EXIT_N, True, Utils.BLACK) 
        self.singleSelected = Utils.cargarSprites(Utils.SINGLE_PLAYER_FB, Utils.SINGLE_PLAYER_FB_N, True, Utils.BLACK) 
        self.exitSelected = Utils.cargarSprites(Utils.EXIT_FB, Utils.EXIT_FB_N, True, Utils.BLACK)
        
        self.singleRect = pygame.Rect(20, 40, self.single[0].get_width(), self.single[0].get_height())
        self.exitRect = pygame.Rect(520, 200, self.exit[0].get_width(), self.exit[0].get_height())
        self.singlePress = False
        self.exitPress = False
        
        self.idExit = 0 
        self.idSingle = 0 
        self.idSingleSelected = 0 
        self.idExitSelected = 0 
    
    def update(self):
        if Utils.STATE == 0:
            pass
        
    def draw(self, screen):
        if Utils.STATE == Utils.System_State.MAINMENU:
            screen.blit(self.mainMenu, [0, 0])
            
            #Boton single player
            press, iniPos = self.mouse.getPressed()
            if self.mouse.isCollide(self.singleRect):
                screen.blit(self.singleSelected[self.idSingleSelected], Utils.SINGLE_PLAYER_FB_POS)
                endPos = self.mouse.getPosition()
                if not self.singlePress and press and Raton.collides(iniPos[0], iniPos[1], self.singleRect):
                    self.singlePress = True
                elif self.mouse.getClick() and self.singlePress and Raton.collides(endPos[0], endPos[1], self.singleRect):
                    print("Seleccionado single player")
                    Utils.STATE = Utils.System_State.MAP1
                    self.singlePress = False
            screen.blit(self.single[self.idSingle], Utils.SINGLE_PLAYER_POS)
            
            #Boton Exit
            screen.blit(self.exit[self.idExit], Utils.EXIT_POS)
            if self.mouse.isCollide(self.exitRect):
                screen.blit(self.exitSelected[self.idExitSelected], Utils.EXIT_FB_POS)
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
            
        if Utils.STATE == Utils.System_State.ONGAME:
            muestra_texto(screen, times, str(self.player.resources), Utils.BLACK, 30, Utils.SCREEN_WIDTH - 40, 20)