import pygame

from .TerranSoldier import *
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *
from .Entity import *

HP = 200
GENERATION_TIME = 5
CAPACITY = 0

class Extractor(Structure):
    TILES_WIDTH = 4
    TILES_HEIGHT = 3
    CENTER_TILE = [1, 1]
    sprites = []
    training = []
    generationTime = 0
    generationCount = 0
    nBuildSprites = 3
    deafault_index = 3
    generationStartTime = 0
    HEIGHT_PAD = 80
    rectOffY = -10
    clicked = False
    frame = 8
    nSprites = 4

    def __init__(self, xini, yini, player, map, building, gas = None):
        Structure.__init__(self, HP, EXTRACTOR_MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        self.sprites = cargarSprites(EXTRACTOR_PATH, self.nSprites, False, BLUE2, 1,0)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        deadSprites = Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.sprites += deadSprites

        self.image = self.sprites[self.index]
        self.operativeIndex = [0, 1, 2, 3]
        self.spawningIndex = [0, 1, 2, 3]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]

        self.render = pygame.transform.scale(pygame.image.load(EXTRACTOR_RENDER), RENDER_SIZE)

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE
        self.resource = gas
        if self.resource != None:
            self.resource.disable()

        self.count = 0
        self.training = []
        self.paths = []

        self.type = ZERG_GEYSER_STRUCTURE

    def command(self, command):
        return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[0]
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
        if len(tiles_set) == (self.TILES_HEIGHT -1)*self.TILES_WIDTH:
            for tile in tiles_set:
                print(tile.tileid)
                if tile.type != GEYSER:
                    ok = False
                    break
        else:
            ok = False
        print(ok)
        return ok

    def buildProcess(self):
        gas = (self.mapa.getTile(self.x, self.y)).ocupante
        if gas != None:
            self.resource = gas
            gas.disable()
    def getOrder(self):
        if self.state != BuildingState.BUILDING and self.state != BuildingState.COLLAPSING and self.state!= BuildingState.DESTROYED:
            return CommandId.EXTRACT_GAS
        else:
            return CommandId.NULL

    def toDictionary(self, map):
        #print("barracke x e y Ini ", self.xIni, self.yIni)
        #x, y = map.getTileIndex(self.originX, self.originY)
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "extractor",
            "building": self.building,
            "nombre": "Extractor de Zerg",
            "funcion": "extrae recursos"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
