import pygame

pygame.mixer.init()

#--------Musica de fondo
mainMenuBGM = "Sonido/BGM/mainMenuBGM.mp3"
map1BGM = "Sonido/BGM/map1BGM.mp3"

#--------Efecto de sonido
botonSound = pygame.mixer.Sound("Sonido/Misc/BUTTON.WAV")
botonSound2 = pygame.mixer.Sound("Sonido/Misc/boton.mp3")

construirSound = pygame.mixer.Sound("Sonido/Misc/PBldgPlc.wav")
structureSelectedSound = pygame.mixer.Sound("Sonido/Misc/OutOfGas.wav")

terranStructureDead = pygame.mixer.Sound("Sonido/Misc/EXPLOLRG.WAV")
soldierDeadSound = pygame.mixer.Sound("Sonido/Misc/ZBldgPlc.wav")
workerDeadSound = pygame.mixer.Sound("Sonido/Misc/explo1.wav")

workerAttackSound = pygame.mixer.Sound("Sonido/Misc/PPwrDown.wav")
soldierAttackSound = pygame.mixer.Sound("Sonido/Bullet/blastgn2.wav")

workerGenerateSound = pygame.mixer.Sound("Sonido/Misc/TPwrDown.wav")
soldierGenerateSound = pygame.mixer.Sound("Sonido/Misc/tdrTra01.wav")
