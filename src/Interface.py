
import pygame
from . import Player, Command, Utils

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
    def __init__(self, player):
        self.player = player
    
    def draw(self, screen):
        muestra_texto(screen, times, str(self.player.resources), Utils.BLACK, 30, Utils.SCREEN_WIDTH - 40, 20)