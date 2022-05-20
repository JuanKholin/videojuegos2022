import pygame as pg

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
    nSprites = EXTRACTOR_TOTAL_FRAMES

    def __init__(self, xini, yini, player, map, building, gas = None):
        self.resource = gas
        if self.resource != None:
            self.resource.disable()
            xini, yini = self.resource.getTile()
        Structure.__init__(self, HP, EXTRACTOR_MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        sprites = Utils.EXTRACTOR_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]
        self.nDeadSprite = len(self.sprites) - len(self.shadows)
        self.image = self.sprites[self.index]
        
        self.operativeIndex = [0, 1, 2, 3]
        self.spawningIndex = [0, 1, 2, 3]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]

        self.render = pg.transform.scale(pg.image.load(EXTRACTOR_RENDER), RENDER_SIZE)

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE
        
        
            

        self.count = 0
        self.training = []
        self.paths = []

        self.type = REFINERY
        
    def drawInfoOperative(self, screen, color):
        dic = self.toDictionary(self.mapa)
        muestra_texto(screen, str('monotypecorsiva'), dic['funcion'], color, 20, [Utils.ScreenWidth/2 - GUI_INFO_X2, Utils.ScreenHeight - GUI_INFO_Y2 + 50])
        if self.resource.capacity > 0:
            muestra_texto(screen, str('monotypecorsiva'), str(self.resource.capacity), YELLOW, 20, [Utils.ScreenWidth/2 - GUI_INFO_X2 + 60, Utils.ScreenHeight - GUI_INFO_Y2 + 90], True)
        else:
            muestra_texto(screen, str('monotypecorsiva'), "0", YELLOW, 20, [Utils.ScreenWidth/2 - GUI_INFO_X2 + 60, Utils.ScreenHeight - GUI_INFO_Y2 + 90], True)

    def command(self, command):
        return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[0]
    
    def drawBuildTiles(self, screen, camera, tiles):
        for tile in tiles:
            r = tile.getRect()
            if tile.type == GEYSER and tile.visible:
                pg.draw.rect(screen, GREEN, pg.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)
            else:
                pg.draw.rect(screen, RED, pg.Rect(r[0] - camera.x, r[1] - camera.y, r[2], r[3]), 2)

    def draw(self, screen, camera):
        Structure.draw(self, screen, camera)
        if self.resource != None:
            muestra_texto(screen, str('monotypecorsiva'), str(self.resource.capacity), BLUE, 20, [60, 10])

    def checkTiles(self, visible = True):
        r = self.getRect()
        tiles = self.mapa.getRectTiles(r)
        ok = True
        tiles_set = set(tiles)
        if len(tiles_set) == (self.TILES_HEIGHT -1)*self.TILES_WIDTH:
            for tile in tiles_set:
                if tile.type != GEYSER or (not tile.visible and visible):
                    ok = False
                    break
        else:
            ok = False
        #print(ok)
        return ok
    
    def changeToDestroyed(self):
        #print("DESTROYED ", self.x, " ", self.y)
        self.state = BuildingState.DESTROYED
        self.index = 0
        self.mapa.setLibre(self.getTile())
        self.resource.setEnable()
        self.clicked = False
        self.player.structures.remove(self)

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
            "nombre": "Extractor",
            "funcion": "Extrae gas de un geyser"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
