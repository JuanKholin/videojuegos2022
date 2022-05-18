import pygame as pg

class Entity():
    def __init__(self, hp, xIni, yIni, mineralCost, generationTime, id, player):
        self.maxHp = hp
        self.mineralCost = mineralCost
        self.generationTime = generationTime
        self.id = id
        self.x = xIni
        self.y = yIni
        self.hp = hp
        self.player = player
        if player != None:
            self.mapa = player.getMapa()
            
        self.shadow = []

    def update():
        pass
    
    def getHP(self):
        return self.hp
    
    def getInfo(self):
        return "None"
    
    def getMaxHP(self):
        return self.maxHp
    
    def getTile(self):
        pos = self.getPosition()
        return self.mapa.getTile(pos[0], pos[1])
    
    def getRender(self):
        return self.render

    # Pre: Altura del spritesheet % rows == 0
    # Post: Devuelve el spritesheet dividido en una lista de sprites
    @staticmethod
    def divideSpritesheetByRows(spritesheet, rows, scale):
        totalRows = spritesheet.get_height()
        maxCol = spritesheet.get_width()
        sprites = []
        for i in range(int(totalRows / rows)):
            aux = pg.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows))
            #aux = pg.transform.scale2x(aux)
            aux = pg.transform.scale(aux, [aux.get_rect().w * scale, aux.get_rect().h * scale])

            sprites.append(aux)
        return sprites
    
    # Pre: Altura del spritesheet % rows == 0
    # Post: Devuelve el spritesheet dividido en una lista de sprites sin escalado
    @staticmethod
    def divideSpritesheetByRowsNoScale(spritesheet, rows, size = None):
        totalRows = spritesheet.get_height()
        maxCol = spritesheet.get_width()
        sprites = []
        for i in range(int(totalRows / rows)):
            aux = pg.Surface.subsurface(spritesheet, (0, rows * i, maxCol, rows))
            if size != None:
                aux = pg.transform.scale(aux, [size[0], size[1]])

            sprites.append(aux)
        return sprites

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setTilePosition(self, tile):
        self.x = tile.centerx
        self.y = tile.centery
        
    def drawInfo(self):
        pass
