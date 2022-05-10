import pygame

from .TerranSoldier import *
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from .Entity import *
from ..Utils import *

HP = 200
GENERATION_TIME = 5
CAPACITY = 5

class TerranBarracks(Structure):
    TILES_WIDTH = 4
    TILES_HEIGHT = 3
    CENTER_TILE = [1, 1]
    sprites = []
    training = []
    generationTime = 0
    generationCount = 0
    nBuildSprites = 4
    deafault_index = 4
    generationStartTime = 0
    heightPad = 15
    rectOffY = 8
    tileW = 4
    tileH = 3
    clicked = False
    frame = 8
    nSprites = 6
    options = [Options.GENERATE_SOLDIER]

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, TERRAN_BARRACKS_MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)

        self.sprites = cargarSprites(TERRAN_BARRACKS_PATH, self.nSprites, False, WHITE, 1.1)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        deadSprites = Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.sprites += deadSprites

        self.image = self.sprites[self.index]
        self.operativeIndex = [4]
        self.spawningIndex = [4, 5]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]

        self.render = pygame.transform.scale(pygame.image.load(BARRACKS_RENDER), RENDER_SIZE)

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE

        self.training = []
        self.paths = []

        self.type = TERRAN_BARRACKS
        print("SOY UNA BARRACA Y TENGO CAPACISAS ", self.capacity)

    def execute(self, command_id):
        #if self.clicked:
        #print("soy clickeado?")
        if (command_id == CommandId.GENERATE_UNIT or command_id == CommandId.GENERATE_SOLDIER) and self.player.resources >= TERRAN_SOLDIER_MINERAL_COST:
            self.player.resources -= TERRAN_SOLDIER_MINERAL_COST
            terranSoldier = TerranSoldier(self.player)
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
        return self.sprites[4]

    def toDictionary(self, map):
        #print("barracke x e y Ini ", self.xIni, self.yIni)
        #x, y = map.getTileIndex(self.originX, self.originY)
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "terranBarracks",
            "building": self.building,
            "nombre": "Terran cuartel",
            "funcion": "entrena tropas de infanteria"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
