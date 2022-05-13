import pygame
from . import Utils

pygame.mixer.init()

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