import pygame
from . import Utils
from .Utils import *

pygame.mixer.init()

def updateScreen(screen):
    x, y = screen.get_size()
    if x < MIN_SCREEN_WIDTH:
        x = MIN_SCREEN_WIDTH
    if y < MIN_SCREEN_HEIGHT:
        y = MIN_SCREEN_HEIGHT
    Utils.ScreenWidth = x
    Utils.ScreenHeight = y
    Utils.ScreenWD = Utils.ScreenWidth - MIN_SCREEN_WIDTH
    Utils.ScreenHD = Utils.ScreenHeight - MIN_SCREEN_HEIGHT
    screen = pygame.display.set_mode((x, y), pygame.RESIZABLE)

def playSound(sound, n = 1):
    if not Utils.haveBGM:
        n = n - 1
        sound.set_volume(Utils.SOUND_VOLUME)
        pygame.mixer.Sound.play(sound, n)
    
def playMusic(music, n = -1, pos = 0):
    if not Utils.haveBGM:
        pygame.mixer.music.load(music)
        
        pygame.mixer.music.set_volume(Utils.BGM_VOLUME)
        pygame.mixer.music.play(n, pos)
        Utils.haveBGM = True

def pauseMusic():
    pygame.mixer.music.pause()

def stopMusic():
    pygame.mixer.music.stop()
    Utils.haveBGM = False
    
def stopAllSound():
    pygame.mixer.stop()
    
def getSprite(path, color, size):
    image = pygame.image.load(path)
    image.set_colorkey(color)
    image = pygame.transform.scale(image, size)
    return image

def divideSpritesheetByRows(spritesheet, rows, scale = 1.5):
    totalRows = spritesheet.get_height()
    maxCol = spritesheet.get_width()
    sprites = []
    for i in range(int(totalRows / rows)):
        aux = pygame.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows))
        aux = pygame.transform.scale(aux, [aux.get_rect().w * scale, aux.get_rect().h * scale])

        sprites.append(aux)
    return sprites