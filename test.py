import pygame, sys

pygame.init()

# Definir colores

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

size =(SCREEN_WIDTH,SCREEN_HEIGHT)

animation_dir = "assets/kurisuAnimation/kurisu"
frame = 1
kurisuFrames = []

class Kurisu(pygame.sprite.Sprite):
    #Constructor
    def __init__(self, id):
        super().__init__()
        ruta = animation_dir + str(id) + ".png"
        print(ruta)
        self.image = pygame.image.load(ruta).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #Para posicionar el sprite
    
    def update(self):
        self.rect.w += 1
        self.rect.y += 1




screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
for i in range(5,20):
    kurisu = Kurisu(i)
    kurisuFrames.append(kurisu.image)
#Controlar frames por segundo
clock = pygame.time.Clock()
frame_list = pygame.sprite.Group()
kurisu = Kurisu(20)
frame_list.add(kurisu)
dim = (kurisu.image.get_width(), kurisu.image.get_height())
angle = 0
while True:
    for event in pygame.event.get(): #Identificar lo sucedido en la ventana
        #print(event)
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            keys=pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                print("resize")
                frame_list.update()
                
            if keys[pygame.K_0]:
                print("resize")
                
    
    screen.fill(WHITE)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()