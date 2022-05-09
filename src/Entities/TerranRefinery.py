import pygame

from .Structure import *
from .. import Player, Map
from ..Command import *
from .Entity import *
from ..Utils import *

HP = 200
GENERATION_TIME = 5

class TerranRefinery(Structure):
    TILES_WIDTH = 4
    TILES_HEIGHT = 2
    CENTER_TILE = [1, 1]
    sprites = []
    training = []
    generationTime = 0
    generationCount = 0
    nBuildSprites = 4
    deafault_index = 5
    generationStartTime = 0
    heightPad = 5
    rectOffY = 57
    tileW = 4
    tileH = 2
    clicked = False
    frame = 8

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, TERRAN_REFINERY_MINERAL_COST, GENERATION_TIME, xini, yini, map, player)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        self.sprites = cargarSprites(TERRAN_REFINERY_PATH, 5, False, BLACK)
        #+ Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.image = self.sprites[self.index]
        self.operativeIndex = [4]
        self.spawningIndex = [4]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]

        self.render = pygame.transform.scale(pygame.image.load(REFINERY_RENDER), RENDER_SIZE)

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE

        self.resource = None
        self.training = []
        self.paths = []

    def getBuildSprite(self):
        return self.sprites[4]

    def getOrder(self):
        return CommandId.EXTRACT_GAS

    def drawBuildTiles(self, screen, camera, tiles):
        for tile in tiles:
            r = tile.getRect()
            if tile.type == GEYSER:
                pygame.draw.rect(screen, GREEN, pygame.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)
            else:
                pygame.draw.rect(screen, RED, pygame.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)

    def draw(self, screen, camera):
        Structure.draw(self, screen, camera)
        if self.resource != None:
            muestra_texto(screen, str('monotypecorsiva'), str(self.resource.capacity), BLUE, 20, [60, 10])

    def checkTiles(self):
        r = self.getRect()
        tiles = self.mapa.getRectTiles(r)
        ok = True
        tiles_set = set(tiles)
        if len(tiles_set) == self.tileH*self.tileW:
            for tile in tiles_set:
                if tile.type != GEYSER:
                    ok = False
                    break
        else:
            ok = False
        return ok

    def buildProcess(self):
        gas = (self.mapa.getTile(self.x, self.y)).ocupante
        if gas != None:
            self.resource = gas
            gas.disable()

    def toDictionary(self, map):
        #print("barracke x e y Ini ", self.xIni, self.yIni)
        #x, y = map.getTileIndex(self.originX, self.originY)
        return {
            "clase": "terranRefinery",
            "x": self.xIni,
            "y": self.yIni,
            "building": self.building,
            "nombre": "Refineria",
            "funcion": "extrae gas geyser"
        }
