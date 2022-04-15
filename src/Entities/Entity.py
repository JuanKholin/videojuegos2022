import pygame as pg

class Entity():
    def __init__(self, hp, xIni, yIni, mineralCost, generationTime, id):
        self.maxHp = hp
        self.mineralCost = mineralCost
        self.generationTime = generationTime
        self.id = id
        self.x = xIni
        self.y = yIni
        self.hp = 200

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
            aux = pg.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows))
            aux = pg.transform.scale2x(aux)
            
            sprites.append(aux)
        return sprites
    
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        
    def setTilePosition(self, tile):
        self.x = tile.centerx
        self.y = tile.centery