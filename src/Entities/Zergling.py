import pygame as pg

from . import Zerg, Entity
from .. import Utils

# Constantes
HP = 40
MINERAL_COST = 20
GENERATION_TIME = 200
SPEED = 2 
FRAMES_TO_REFRESH = 5
SPRITES = "zergling.bmp"
FACES = 8
FRAMES = 8
ID = 3

class Zergling(Zerg.Zerg):
    # Pre: xIni e yIni marcan posiciones del mapa, (ej: (3, 2) se refiere a la posicion de la
    # cuarta columna y tercera fila del mapa)
    # Post: Crea un bichito mono que no hace practicamente nada pero tu dale tiempo
    def __init__(self, xIni, yIni):
        Zerg.Zerg.__init__(self, HP, xIni * 40 + 20, yIni * 40 + 20, MINERAL_COST, 
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAMES, ID)
        spritesheet = pg.image.load("./sprites/" + self.spritesName)
        spritesheet.set_colorkey(Utils.BLACK)
        self.sprites = Entity.Entity.divideSpritesheetByRows(spritesheet, 128)
        self.image = self.sprites[0]
        self.imageRect = Utils.rect(self.x, self.y, self.image.get_width(), 
                self.image.get_height() - self.rectOffY)

    def update(self):
        self.image = self.sprites[self.frame]
        pass

    # Devuelve la posicion en coordenadas del propio mapa
    def getPosition(self):
        return (self.x, self.y)

    # Devuelve el rectangulo que conforma su imagen, creo, esto lo hizo otro
    def getRect(self):
        rectAux = pg.Rect(self.imageRect.x - self.imageRect.w / 2, 
                self.imageRect.y - self.imageRect.h, self.imageRect.w, self.imageRect.h)
        return rectAux