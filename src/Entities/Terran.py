import pygame
import math
from . import Unit
BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400


    

class Terran(Unit.Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, faces, frames):
        Unit.Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, faces, frames)
    def atacar():
        pass
    def construir():
        pass

    def draw(self, screen):
        rect = self.getRect()
        #print(image.x,image.y)
        pygame.draw.rect(screen, BLACK, pygame.Rect(rect.x, rect.y, rect.w, rect.h),1)
        screen.blit(self.image, [rect.x, rect.y])