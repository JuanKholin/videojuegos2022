import pygame, math

#FUNCIONES DEL RATON
class raton(pygame.sprite.Sprite):
    #Constructor
    sprite = []
    sprite2 = []
    index = 0
    index2 = 0
    frame = 0
    clicked = False
    collide = False
    def __init__(self, ruta):
        super().__init__()
        self.index = 0
        for i in range(5):
            self.sprite.append(pygame.image.load(ruta+"tile00"+str(i)+".png").convert_alpha())
        for i in range(14):
            j = i+34
            self.sprite2.append(pygame.image.load(ruta+"tile0"+str(j)+".png").convert_alpha())
        self.clickSprite = pygame.image.load(ruta+"click.png").convert_alpha()
        self.image = self.sprite[0]
        self.rect = self.image.get_rect() #Para posicionar el sprite
        pygame.mouse.set_visible(False)
        self.point = point(ruta)
        
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - self.rect.width/2
        self.rect.y = pos[1] - self.rect.height/2
        type = pygame.mouse.get_pressed()
        if type[0]:
            self.image = self.clickSprite
        elif self.collide:
            self.frame += 1
            if self.frame > 5:
                self.index2 = (self.index2+1)%14
                self.index = (self.index+1)%5
                self.image = self.sprite2[self.index2]
                self.frame = 0
        else:
            self.frame += 1
            if self.frame > 5:
                self.index = (self.index+1)%5
                self.index2 = (self.index2+1)%14
                self.image = self.sprite[self.index]
                self.frame = 0
    
    def click(self):
        self.clicked = not self.clicked

    def setCollide(self, detected):
        self.collide = detected
    def draw(self, screen):
        self.point.draw(screen)
        screen.blit(self.image, (self.rect.x, self.rect.y))

class point(pygame.sprite.Sprite):
    #Constructor
    sprite = []
    index = 0
    frame = 0
    clicked = False
    realX = 0
    realY = 0
    def __init__(self, ruta):
        super().__init__()
        self.index = 0
        for i in range(5):
            self.sprite.append(pygame.image.load(ruta+"point"+str(i)+".png").convert_alpha())
        self.image = self.sprite[0]
        self.rect = self.image.get_rect() #Para posicionar el sprite
        
    def update(self):
        if self.clicked:
            self.frame += 1
            if self.frame > 5:
                self.index = self.index+1
                self.image = self.sprite[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = self.realX-self.rect.width/2
                self.rect.y = self.realY-self.rect.height/2
                self.frame = 0
            if self.index == 4:
                self.clicked = False
                
    def click(self, x, y):
        self.clicked = True
        self.index = 0
        self.realX = x
        self.realY = y
        self.rect.x = x-self.rect.width/2
        self.rect.y = y-self.rect.height/2

    def getClicked(self):
        return self.clicked

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))