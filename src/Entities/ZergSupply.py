import pygame
from .Zergling import *
from .Structure import *
from ..Command import *
from ..Utils import *
from .Entity import *

WHITE   = (255,255,255)
GENERATION_TIME = 10
MINERAL_COST = 50
WIDTH = 6
HEIGHT = 4
HP = 200
CAPACITY = 10

class ZergSupply(Structure):
    TILES_WIDTH = 3
    TILES_HEIGHT = 2
    CENTER_TILE = [1, 1]
    sprites = []
    training = []
    HEIGHT_PAD = 10
    generationTime = 0
    generationCount = 0
    widthPad = -15
    rectOffY = 30
    clicked = False
    frame = 10
    nSprites = ZERG_DEPOT_TOTAL_FRAMES
    options = []

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        sprites = Utils.ZERG_DEPOT_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]
        self.image = self.sprites[self.index]
        self.operativeIndex = [0, 1, 2]
        self.spawningIndex = [0, 1, 2]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]
        #self.raton = raton
        self.render = pg.transform.scale(pg.image.load(ZERG_DEPOT_RENDER), RENDER_SIZE)

        self.building = building
        if building:
            self.state = BuildingState.OPERATIVE
        self.count = 0
        
        self.training = []
        self.paths = []
        self.building = False

        self.type = DEPOT

    def execute(self, command_id):
        if self.clicked:
            pass

    def command(self, command):
        return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[0]

    def toDictionary(self, map):
        #print("x e y del zerg builder ", self.x, self.y)
        #x, y = map.getTileIndex(self.originX, self.originY)
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "zergSupply",
            "building": self.building,
            "nombre": "Guarida",
            "funcion": "Aumenta capacidad del ejercito"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
