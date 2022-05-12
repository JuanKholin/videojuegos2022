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

class Zerg3(Structure):
    TILES_WIDTH = 3
    TILES_HEIGHT = 2
    CENTER_TILE = [1, 1]
    sprites = []
    training = []
    heightPad = 10
    generationTime = 0
    generationCount = 0
    widthPad = -15
    rectOffY = 30
    tileW = 3
    clicked = False
    tileH = 2
    frame = 10
    nSprites = 3
    options = []

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        self.sprites = cargarSprites(S3_PATH, self.nSprites, False, BLUE2, 1.2, 0)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        deadSprites = Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.sprites += deadSprites
        self.image = self.sprites[self.index]
        self.operativeIndex = [0, 1, 2]
        self.spawningIndex = [0, 1, 2]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]
        #self.raton = raton
        self.render = pygame.transform.scale(pygame.image.load(S3_RENDER), RENDER_SIZE)

        self.building = building
        if building:
            self.state = BuildingState.OPERATIVE
        self.count = 0
        
        self.training = []
        self.paths = []
        self.building = False

        self.type = ZERG_S1

    def execute(self, command_id):
        if self.clicked:
            pass

    def command(self, command):
        return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[3]

    def toDictionary(self, map):
        #print("x e y del zerg builder ", self.x, self.y)
        #x, y = map.getTileIndex(self.originX, self.originY)
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "s1",
            "building": self.building,
            "nombre": "Criadera de Zerg",
            "funcion": "Base enemiga"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
