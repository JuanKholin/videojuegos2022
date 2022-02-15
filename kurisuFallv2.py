from email.mime import image
import pygame, sys, random

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

def framesToOut(vx, vy, sprite):
    frames = 0
    x = SCREEN_WIDTH/ 2
    y = SCREEN_HEIGHT/ 2
    collide = False
    while not collide:
        frames += 1
        x += vx
        y += vy
        collide = x > SCREEN_WIDTH or x < 0 or y > SCREEN_HEIGHT or y < 0 - sprite.get_height()
    return frames 



#Clase meteoro(Sub clase de Sprite)
class Kurisu(pygame.sprite.Sprite):
    speed_x = 0
    speed_y = 0
    anch = 0 
    alt = 0
    #Constructor
    def __init__(self):
        super().__init__()
        self.originalImage = pygame.image.load("assets/kurisuAnimation/kurisu20.png")
        self.originalImage = pygame.transform.scale(self.originalImage, (64,64))
        self.image = self.originalImage
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #Para posicionar el sprite
        self.anch = self.image.get_width()
        self.alt = self.image.get_height()
    
    def update(self):
        print(self.rect.x)
        print(self.rect.y)
        print(self.anch)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.image = pygame.transform.scale(self.originalImage, (self.image.get_width() + 3,self.image.get_height() + 3))
        self.rect = self.image.get_rect(center = self.rect.center)
        
        
        #if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH  or self.rect.y < 0 - self.image.get_height()  or self.rect.y > SCREEN_HEIGHT:
            



screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()



all_sprites = pygame.sprite.Group()

for i in range(20):
    kurisu = Kurisu()
    kurisu.rect.x = SCREEN_WIDTH/2
    kurisu.rect.y = SCREEN_HEIGHT/2
    kurisu.speed_x = random.randrange(-10,10,1) 
    while kurisu.speed_x == 0:
        kurisu.speed_x = random.randrange(-10,10,1)
    if kurisu.speed_x < 0:
        kurisu.speed_x -= 2
    else:
         kurisu.speed_x += 2
    kurisu.speed_y = random.randrange(-10,10,1)  
    while kurisu.speed_y == 0:
        kurisu.speed_y = random.randrange(-10,10,1)
    if kurisu.speed_y < 0:
        kurisu.speed_y -= 2
    else:
         kurisu.speed_y += 2
    kurisu.frameRate = int(framesToOut(kurisu.speed_x, kurisu.speed_y, kurisu.image)/15)

    all_sprites.add(kurisu)

while True:
    for event in pygame.event.get(): #Identificar lo sucedido en la ventana
        #print(event)
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            SCREEN_HEIGHT = event.h
            SCREEN_WIDTH = event.w
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    
    ###---LOGICA
    #Actualizar objetos
    all_sprites.update()



    ###---LOGICA

    #Poner color de fondo
    screen.fill(BLACK)
    
    ###--- ZONA DE DIBUJO
    all_sprites.draw(screen)

    ###--- ZONA DE DIBUJO

    #ACtualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()