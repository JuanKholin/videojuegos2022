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
luuserSound = pygame.mixer.Sound("Sonido/Misc/YouLose.wav")
winSound = pygame.mixer.Sound("Sonido/Misc/YouWin.wav")

construirSound = pygame.mixer.Sound("Sonido/Misc/PBldgPlc.wav")
structureSelectedSound = pygame.mixer.Sound("Sonido/Misc/OutOfGas.wav")
zergStructureSelectedSound = pygame.mixer.Sound("Sonido/Misc/IntoNydus.wav")
terranSelectedSound = pygame.mixer.Sound("Sonido/Misc/TBldgPlc.wav")
zergSelectedSound = pygame.mixer.Sound("Sonido/Misc/Critters/LCrDth00.wav")

terranStructureDead = pygame.mixer.Sound("Sonido/Misc/EXPLOLRG.WAV")
zergStructureDead = pygame.mixer.Sound("Sonido/Misc/explo3.wav")

soldierDeadSound = pygame.mixer.Sound("Sonido/Misc/ZBldgPlc.wav")
workerDeadSound = pygame.mixer.Sound("Sonido/Misc/EXPLOLRG.WAV")
zerglingDeadSound = pygame.mixer.Sound("Sonido/Misc/ZPwrDown.wav")

workerAttackSound = pygame.mixer.Sound("Sonido/Misc/PPwrDown.wav")
soldierAttackSound = pygame.mixer.Sound("Sonido/Bullet/blastgn2.wav")
firebatAttackSound = pygame.mixer.Sound("Sonido/Bullet/PSIBLADE.WAV")
goliathAttackSound = pygame.mixer.Sound("Sonido/Misc/burrowup.wav")

zerglingAttackSound = pygame.mixer.Sound("Sonido/Misc/Critters/JCrDth00.wav")

workerGenerateSound = pygame.mixer.Sound("Sonido/Misc/TPwrDown.wav")
soldierGenerateSound = pygame.mixer.Sound("Sonido/Misc/tdrTra01.wav")
zerglingGenerateSound = pygame.mixer.Sound("Sonido/Bullet/ZDrHit00.WAV")

'''botonSound = None
botonSound2 = None
loserSound = None
luuserSound = None
winSound = None

construirSound = None
structureSelectedSound = None
zergStructureSelectedSound = None
terranSelectedSound = None
zergSelectedSound = None

terranStructureDead = None
zergStructureDead = None

soldierDeadSound = None
workerDeadSound = None
zerglingDeadSound = None

workerAttackSound = None
soldierAttackSound = None
firebatAttackSound = None
goliathAttackSound = None

zerglingAttackSound = None

workerGenerateSound = None
soldierGenerateSound = None
zerglingGenerateSound = None'''
