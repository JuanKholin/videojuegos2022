from cmath import cos
import pygame as pg
from . import Player, Command, Utils, Raton
from .Music import *
from .Lib import *
from .Utils import *
from .Command import *

class Button():
    def __init__(self, image, command, cartel = None, msgCartel = "a", xpad = 0, coste = 0, costeGas = 0, cartelpad = 0):
        self.image = pg.image.load(image)
        self.image = pg.transform.scale(self.image, (Utils.BUTTON_W, Utils.BUTTON_H))
        if cartel != None:
            self.cartel = pg.image.load(cartel)
            self.cartel = pg.transform.scale(self.cartel, (self.cartel.get_width() * 1.5, self.cartel.get_height() * 1.5))
        else:
            self.cartel = None
        self.msgCartel = msgCartel
        self.command = command
        self.click = False
        self.collide = False
        self.x = 0
        self.y = 0
        self.xpad = xpad
        self.coste = coste
        self.cartelPad = cartelpad
        self.costeGas = costeGas
        
    def update(self):
        pass
        
    def draw(self, screen, x, y):
        self.x = x
        self.y = y
        screen.blit(self.image, (x, y))
        if self.collide:
            if self.cartel != None:
                screen.blit(self.cartel, (x - self.cartelPad, y- 40))
                #muestra_texto(screen, 'monotypecorsiva', str(self.msgCartel), GREEN2, 15, (self.x - self.cartelPad + self.xpad, self.y - 32))
                #muestra_texto(screen, 'monotypecorsiva', str(self.coste), GREEN2, 20, (self.x + 33 - self.cartelPad , self.y - 12))
                #muestra_texto(screen, 'monotypecorsiva', "1", GREEN2, 20, (self.x + 73 - self.cartelPad , self.y - 12))
                muestra_texto(screen, 'monotypecorsiva', str(self.msgCartel), GREEN2, 15, (self.x - self.cartelPad + self.xpad, self.y - 40))
                muestra_texto(screen, 'monotypecorsiva', str(self.coste), GREEN2, 20, (self.x + 24 - self.cartelPad , self.y - 22))
                if self.costeGas == 0:
                    muestra_texto(screen, 'monotypecorsiva', "0", GREEN2, 20, (self.x + 70 - self.cartelPad , self.y - 23))
                else:
                    muestra_texto(screen, 'monotypecorsiva', "0", GREEN2, 20, (self.x + 140 - self.cartelPad , self.y - 23))
                    muestra_texto(screen, 'monotypecorsiva', str(self.costeGas), GREEN2, 20, (self.x + 85 - self.cartelPad , self.y - 22))
            else:
                pass
                #pg.draw.rect(screen, BLUE, pg.Rect(self.x, self.y-15, 50, 20))
            #text = Utils.text[self.option] 
            #muestra_texto(screen, times, text, BLACK, 30, (self.x, self.y-20))
        if Utils.DEBBUG:
            pg.draw.rect(screen, PINK, pg.Rect(self.x, self.y, Utils.BUTTON_W, Utils.BUTTON_H), 1)
            
    def getRect(self):
        return pg.Rect(self.x, self.y, Utils.BUTTON_W, Utils.BUTTON_H)
        
    def setClicked(self):
        self.click = True 
        
    def setCollide(self, collide):
        self.collide = collide 
        
    def getCommand(self):
        return Command(self.command)
    
    
           
        