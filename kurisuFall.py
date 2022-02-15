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
    x = SCREEN_WIDTH / 2
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
    frame = 1
    frames = []
    angle = 0
    frameRate = 0
    #Constructor
    def __init__(self):
        super().__init__()
        for i in range(5,20):
            ruta = animation_dir + str(i) + ".png" 
            self.frames.append(pygame.image.load(ruta).convert())
        self.image = self.frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #Para posicionar el sprite
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.frame += 1
        lastFrame = 15
        if self.frame < self.frameRate*15:
            lastFrame = int(self.frame/self.frameRate)
            if self.frame%self.frameRate == 0:
                self.image = self.frames[int(self.frame/self.frameRate)]
                self.image.set_colorkey(BLACK)
                self.image = pygame.transform.rotate(self.image,self.angle)
        print(lastFrame)
        self.image = self.frames[lastFrame - 1]
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.rotate(self.image,self.angle)
        self.angle += 2
        self.angle = self.angle%360
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH  or self.rect.y < 0 - self.image.get_height()  or self.rect.y > SCREEN_HEIGHT:
            self.rect.x = SCREEN_WIDTH/2
            self.rect.y = SCREEN_HEIGHT/2
            self.frame = 1
            self.image = self.frames[int(self.frame/self.frameRate)]
            self.angle = 0
            self.speed_x = random.randrange(-10,10,1) 
            while self.speed_x == 0:
                self.speed_x = random.randrange(-10,10,1)
            if self.speed_x < 0:
                self.speed_x -= 2
            else:
                self.speed_x += 2
            self.speed_y = random.randrange(-10,10,1)  
            while self.speed_y == 0:
                self.speed_y = random.randrange(-10,10,1)
            if self.speed_y < 0:
                self.speed_y -= 2
            else:
                self.speed_y += 2
            self.frameRate = int(framesToOut(self.speed_x, self.speed_y, self.image)/15)



screen =  pygame.display.set_mode(size, pygame.RESIZABLE)
#Controlar frames por segundo
clock = pygame.time.Clock()



all_sprites = pygame.sprite.Group()

for i in range(1):
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
    input()
    print("INPUT")
    all_sprites.draw(screen)

    ###--- ZONA DE DIBUJO

    #ACtualizar pantalla
    pygame.display.flip()
    clock.tick(60)