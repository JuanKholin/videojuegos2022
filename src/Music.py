import pygame
from . import Utils

pygame.mixer.init()

#--------Musica de fondo
mainMenuBGM = "Sonido/BGM/mainMenuBGM.mp3"
map1BGM = "Sonido/BGM/map1BGM.mp3"

#--------Efecto de sonido
botonSound = pygame.mixer.Sound("Sonido/Misc/BUTTON.WAV")
botonSound2 = pygame.mixer.Sound("Sonido/Misc/boton.mp3")
loserSound = pygame.mixer.Sound("Sonido/Misc/ReallyNigga.mp3")

construirSound = pygame.mixer.Sound("Sonido/Misc/PBldgPlc.wav")
structureSelectedSound = pygame.mixer.Sound("Sonido/Misc/OutOfGas.wav")

terranStructureDead = pygame.mixer.Sound("Sonido/Misc/EXPLOLRG.WAV")
soldierDeadSound = pygame.mixer.Sound("Sonido/Misc/ZBldgPlc.wav")
workerDeadSound = pygame.mixer.Sound("Sonido/Misc/explo1.wav")
zerglingDeadSound = pygame.mixer.Sound("Sonido/Misc/ZPwrDown.wav")

workerAttackSound = pygame.mixer.Sound("Sonido/Misc/PPwrDown.wav")
soldierAttackSound = pygame.mixer.Sound("Sonido/Bullet/blastgn2.wav")
zerglingAttackSound = pygame.mixer.Sound("Sonido/Misc/ZBldgPlc.wav")

workerGenerateSound = pygame.mixer.Sound("Sonido/Misc/TPwrDown.wav")
soldierGenerateSound = pygame.mixer.Sound("Sonido/Misc/tdrTra01.wav")
zerglingGenerateSound = pygame.mixer.Sound("Sonido/Bullet/ZDrHit00.WAV")
#COMENTAME PARA SONIDOS
'''botonSound = None
botonSound2 = None
loserSound = None

construirSound = None
structureSelectedSound = None

terranStructureDead = None
soldierDeadSound = None
workerDeadSound = None
zerglingDeadSound = None

workerAttackSound = None
soldierAttackSound = None
zerglingAttackSound = None

workerGenerateSound = None
soldierGenerateSound = None
zerglingGenerateSound = None'''
