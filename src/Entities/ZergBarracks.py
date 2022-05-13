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

class ZergBarracks(Structure):
    TILES_HEIGHT = 3
    TILES_WIDTH = 4
    CENTER_TILE = [1, 1]
    sprites = []
    training = []
    heightPad = 10
    generationTime = 0
    generationCount = 0
    rectOffY = 20
    tileW = 4
    clicked = False
    tileH = 3
    frame = 20
    nSprites = 3
    options = [Options.GENERATE_SOLDIER_ZERG]

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        self.sprites = cargarSprites(BARRACKS_ZERG_PATH, self.nSprites, False, BLUE2, 1.4, 0)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        deadSprites = Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.sprites += deadSprites
        self.image = self.sprites[self.index]
        self.operativeIndex = [0, 1, 2]
        self.spawningIndex = [0, 1, 2]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]
        #self.raton = raton
        self.render = pygame.transform.scale(pygame.image.load(BARRACKS_ZERG_RENDER), RENDER_SIZE)

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE
        self.count = 0
        
        self.training = []
        self.paths = []
        self.building = False

        self.type = ZERG_BARRACKS

    def execute(self, command_id):
        #if self.clicked:
        #print("soy clickeado?")
        if (command_id == CommandId.GENERATE_UNIT or command_id == CommandId.GENERATE_SOLDIER) and self.player.resources >= TERRAN_SOLDIER_MINERAL_COST:
            self.player.resources -= TERRAN_SOLDIER_MINERAL_COST
            terranSoldier = Zergling(self.player)
            self.generateUnit(terranSoldier)
            self.state = BuildingState.SPAWNING

    def command(self, command):
        if self.state != BuildingState.BUILDING:
            if command == CommandId.GENERATE_UNIT:
                return Command(CommandId.GENERATE_SOLDIER)
            return Command(CommandId.NULL)
        else:
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
            "nombre": "Criadera de Zerling",
            "funcion": "Crear zerling"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
