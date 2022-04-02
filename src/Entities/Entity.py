import pygame as pg

BLACK   = (0,0,0)
WHITE   = (255,255,255)
GREEN   = (0,255,0)
RED     = (255,0,0)
BLUE    = (0,0,255)

class Entity():
    def __init__(self, hp, mineralCost, generationTime, id):
        self.hp = hp
        self.mineralCost = mineralCost
        self.generationTime = generationTime
        self.id = id

    def update():
        pass


    # Pre: Altura del spritesheet % rows == 0
    # Post: Devuelve el spritesheet dividido en una lista de sprites
    @staticmethod
    def divideSpritesheetByRows(spritesheet, rows):
        totalRows = spritesheet.get_height()
        maxCol = spritesheet.get_width()
        sprites = []
        for i in range(int(totalRows / rows)):
            sprites.append(pg.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows)))
        return sprites