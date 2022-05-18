import pygame

from .Structure import *
from .. import Player, Map
from ..Command import *
from .Entity import *
from ..Utils import *

HP = 200
GENERATION_TIME = 5
CAPACITY = 0

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
    HEIGHT_PAD = 5
    rectOffY = 57
    clicked = False
    frame = 8
    nSprites = 5

    def __init__(self, xini, yini, player, map, building, gas = None):
        Structure.__init__(self, HP, TERRAN_REFINERY_MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        self.sprites = cargarSprites(TERRAN_REFINERY_PATH, self.nSprites, False, BLACK)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        deadSprites = Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.sprites += deadSprites
        #+ Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.type = TERRAN_REFINERY

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
        self.resource = gas
        if self.resource != None:
            self.resource.disable()
        self.training = []
        self.paths = []

        self.type = TERRAN_REFINERY
        
    def drawInfoOperative(self, screen, color):
        dic = self.toDictionary(self.mapa)
        muestra_texto(screen, str('monotypecorsiva'), dic['funcion'], color, 20, [Utils.ScreenWidth/2 - GUI_INFO_X2, Utils.ScreenHeight - GUI_INFO_Y2 + 50])
        if self.resource.capacity > 0:
            muestra_texto(screen, str('monotypecorsiva'), str(self.resource.capacity), YELLOW, 20, [Utils.ScreenWidth/2 - GUI_INFO_X2 + 60, Utils.ScreenHeight - GUI_INFO_Y2 + 90], True)
        else:
            muestra_texto(screen, str('monotypecorsiva'), "0", YELLOW, 20, [Utils.ScreenWidth/2 - GUI_INFO_X2 + 60, Utils.ScreenHeight - GUI_INFO_Y2 + 90], True)

    def getBuildSprite(self):
        return self.sprites[4]

    def getOrder(self):
        if self.state != BuildingState.BUILDING and self.state != BuildingState.COLLAPSING and self.state!= BuildingState.DESTROYED:
            return CommandId.EXTRACT_GAS
        else:
            return CommandId.NULL

    def changeToDestroyed(self):
        #print("DESTROYED ", self.x, " ", self.y)
        self.state = BuildingState.DESTROYED
        self.index = 0
        self.mapa.setLibre(self.getTile())
        self.resource.setEnable()
        self.clicked = False
        self.player.structures.remove(self)

    def drawBuildTiles(self, screen, camera, tiles):
        for tile in tiles:
            r = tile.getRect()
            if tile.type == GEYSER and tile.visible:
                pygame.draw.rect(screen, GREEN, pygame.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)
            else:
                pygame.draw.rect(screen, RED, pygame.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)

    def draw(self, screen, camera):
        Structure.draw(self, screen, camera)
        if self.resource != None:
            muestra_texto(screen, str('monotypecorsiva'), str(self.resource.capacity), BLUE, 20, [60, 10])

    def checkTiles(self, visible = True):
        r = self.getRect()
        tiles = self.mapa.getRectTiles(r)
        ok = True
        tiles_set = set(tiles)
        if len(tiles_set) == self.TILES_HEIGHT * self.TILES_WIDTH:
            for tile in tiles_set:
                if tile.type != GEYSER or (not tile.visible and visible):
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
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "terranRefinery",
            "building": self.building,
            "nombre": "Refineria",
            "funcion": "Extrae gas de un geyser"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
