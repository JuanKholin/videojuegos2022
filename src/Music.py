import pygame

pygame.mixer.init()

#--------Musica de fondo
mainMenuBGM = "Sonido/BGM/mainMenuBGM.mp3"
map1BGM = "Sonido/BGM/map1BGM.mp3"

#--------Efecto de sonido
botonSound = pygame.mixer.Sound("Sonido/Misc/BUTTON.WAV")
botonSound2 = pygame.mixer.Sound("Sonido/Misc/boton.mp3")

terranStructureDead = pygame.mixer.Sound("Sonido/Misc/EXPLOLRG.WAV")
