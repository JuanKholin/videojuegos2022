import pygame as pg

from . import Zerg, Entity
from .. import Utils

# Constantes
HP = 40
MINERAL_COST = 20
GENERATION_TIME = 200
SPEED = 2 
FRAMES_TO_REFRESH = 20
SPRITES = "zergling.bmp"
SPRITE_PIXEL_ROWS = 128
FACES = 8
FRAME = 16
TOTAL_FRAMES = 296  # [0:203] MOVICION (13 ciclos de 17 frames con solo 16 utiles)
                    # [204:288] ENTERRACION
                    # [289:295] MORICION
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)), 
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)), 
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)), 
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204))]
STILL_FRAMES = 0
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-frame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
PADDING = 110
ID = 3

class Zergling(Zerg.Zerg):
    # Pre: xIni e yIni marcan posiciones del mapa, (ej: (3, 2) se refiere a la posicion de 
    # la cuarta columna y tercera fila del mapa)
    # Post: Crea un bichito mono que no hace practicamente nada pero tu dale tiempo
    def __init__(self, xIni, yIni):
        Zerg.Zerg.__init__(self, HP, xIni * 40 + 20, yIni * 40 + 20, MINERAL_COST, 
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME, 
                PADDING, ID)
        spritesheet = pg.image.load("./sprites/" + self.spritesName)
        spritesheet.set_colorkey(Utils.BLACK)
        self.sprites = Entity.Entity.divideSpritesheetByRows(spritesheet, 
                SPRITE_PIXEL_ROWS)
        self.mirrorTheChosen()
        self.dir = 0
        self.image = self.sprites[FRAMES[STILL_FRAMES][DIR_OFFSET[self.dir]]]
        self.imageRect = Utils.rect(self.x, self.y, self.image.get_width(), 
                self.image.get_height() - self.rectOffY)


    # Aplica un frame mas a la unidad
    def update(self):
        self.framesToRefresh = (self.framesToRefresh + 1) % FRAMES_TO_REFRESH
        if self.framesToRefresh == 0:
            self.dir = self.dir + 1
            self.dir = self.dir % 16
            if len(self.paths) == 0: # Esta quieto
                self.image = self.sprites[FRAMES[STILL_FRAMES][DIR_OFFSET[self.dir]]]
                #self.resize()
            else: # Esta moviendose
                #DIOS lo que hay que meter aqui
                pass


    # Devuelve la posicion en coordenadas del propio mapa
    def getPosition(self):
        return (self.x, self.y)

    # Devuelve el rectangulo que conforma su imagen, creo, esto lo hizo otro
    def getRect(self):
        rectAux = pg.Rect(self.imageRect.x - self.imageRect.w / 2, 
                self.imageRect.y - self.imageRect.h, self.imageRect.w, self.imageRect.h)
        return rectAux

    # You know what they say: "the bigger, the better"
    #def resize(self):
    #    self.image = pg.transform.scale2x(self.image)
    #    self.imageRect.w = self.image.get_width()
    #    self.imageRect.h = self.image.get_height() - self.rectOffY

    # Genera los sprites que son inversos, es todo un artista
    def mirrorTheChosen(self):
        for i in range(len(FRAMES)):
            for j in range(9, 16):
                self.sprites[FRAMES[i][DIR_OFFSET[j]]] = pg.transform.flip(
                        self.sprites[FRAMES[i][DIR_OFFSET[j]]], True, False)