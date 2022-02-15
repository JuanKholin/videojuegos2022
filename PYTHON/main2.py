#Python v3.10.2  pygame v2.1.2
from email.mime import image
from pygame.locals import *
import pygame, sys, random

# Definir colores

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

size =(SCREEN_WIDTH,SCREEN_HEIGHT)

animation_dir = "kurisu"
ruta = animation_dir + ".png" 

#Clase meteoro(Sub clase de Sprite)
class Kurisu(pygame.sprite.Sprite):
    imageW = 0
    imageH = 0
    speed_x = 0
    speed_y = 0
    frame = 1
    angle = 0
    frameRate = 0
    randAng = 0
    #Constructor
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.originalImage = pygame.image.load(ruta).convert_alpha()
        self.rect = self.originalImage.get_rect() #Para posicionar el sprite
    
    def update(self):
        pygame.time.delay(random.randrange(0,4,1))
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.image = pygame.transform.scale(self.originalImage, (self.imageW, self.imageH))
        self.image = pygame.transform.rotate(self.image,self.angle)
        self.angle += self.randAng
        if self.imageH < 200 and self.imageW < 200:
            self.imageH += 2
            self.imageW += 2
        
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

        if (self.rect.x < 0 - self.image.get_width() or self.rect.x > SCREEN_WIDTH  
        or self.rect.y < 0 - self.image.get_height()  or self.rect.y > SCREEN_HEIGHT):
            self.rect.x = SCREEN_WIDTH/2
            self.rect.y = SCREEN_HEIGHT/2
            self.imageH = 0
            self.imageW = 0
            self.image = pygame.transform.scale(self.originalImage, (self.imageW, self.imageH))
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
            # self.frameRate = int(framesToOut(self.speed_x, self.speed_y, self.image)/15)


def main():
    pygame.init()
    screen =  pygame.display.set_mode(size, pygame.RESIZABLE)

    all_sprites = pygame.sprite.Group()

    for i in range(12):
        random.seed(a=None, version = 2)
        kurisu = Kurisu(screen)
        kurisu.rect.x = 1200 / 2
        kurisu.rect.y = 800 / 2
        kurisu.randAng = random.randrange(1,4,1) 
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
        #kurisu.frameRate = int(framesToOut(kurisu.speed_x, kurisu.speed_y, kurisu.image)/15)

        all_sprites.add(kurisu)

    while True:
        ###---LOGICA
        #Actualizar objetos
        screen.fill((0,0,0))
        all_sprites.update()
            
        ###--- ZONA DE DIBUJO
        #ACtualizar pantalla
        pygame.display.flip()
        pygame.time.delay(10)

        for event in pygame.event.get(): #Identificar lo sucedido en la ventana
            #print(event)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                SCREEN_HEIGHT = event.h
                SCREEN_WIDTH = event.w
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)


if __name__ == "__main__":
    main()
