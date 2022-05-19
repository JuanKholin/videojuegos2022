import pygame as pg
from .Zergling import *
from .Broodling import *
from .Hydralisk import *
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
    HEIGHT_PAD = 10
    generationTime = 0
    generationCount = 0
    rectOffY = 20
    clicked = False
    frame = 20
    nSprites = ZERG_BARRACKS_TOTAL_FRAMES
    options = [Options.GENERATE_T1_ZERG, Options.GENERATE_T2_ZERG, Options.GENERATE_T3_ZERG]

    def __init__(self, xini, yini, player, map, building):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        sprites = Utils.ZERG_BARRACKS_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]
        self.image = self.sprites[self.index]
        self.nDeadSprite = len(self.sprites) - len(self.shadows)
        
        self.operativeIndex = [0, 1, 2]
        self.spawningIndex = [0, 1, 2]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]
        #self.raton = raton
        self.render = pg.transform.scale(pg.image.load(ZERG_BARRACKS_RENDER), RENDER_SIZE)

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE
        self.count = 0
        
        self.training = []
        self.paths = []
        self.building = False

        self.type = BARRACKS
        
    def execute(self, command_id):
        if self.state != BuildingState.BUILDING and self.state != BuildingState.COLLAPSING and self.state != BuildingState.DESTROYED:
            if (command_id == CommandId.GENERATE_UNIT or command_id == CommandId.GENERATE_T1) and self.player.resources >= TERRAN_T1_MINERAL_COST:
                self.player.resources -= TERRAN_T1_MINERAL_COST
                terranSoldier = Zergling(self.player)
                self.generateUnit(terranSoldier)
                self.state = BuildingState.SPAWNING
            elif (command_id == CommandId.GENERATE_T2) and self.player.resources >= ZERG_T2_MINERAL_COST and self.player.gas >= ZERG_T2_GAS_COST:
                self.player.resources -= ZERG_T2_MINERAL_COST
                self.player.gas -= ZERG_T2_GAS_COST
                terranSoldier = Broodling(self.player)
                self.generateUnit(terranSoldier)
                self.state = BuildingState.SPAWNING
            elif (command_id == CommandId.GENERATE_T3) and self.player.resources >= ZERG_T3_MINERAL_COST and self.player.gas >= ZERG_T3_GAS_COST:
                self.player.resources -= ZERG_T3_MINERAL_COST
                self.player.gas -= ZERG_T3_GAS_COST
                terranSoldier = Hydralisk(self.player)
                self.generateUnit(terranSoldier)
                self.state = BuildingState.SPAWNING

    def command(self, command):
        if self.state != BuildingState.BUILDING:
            if command == CommandId.GENERATE_UNIT:
                return Command(CommandId.GENERATE_T1)
            elif command == CommandId.GENERATE_T2:
                return Command(CommandId.GENERATE_T2)
            elif command == CommandId.GENERATE_T3:
                return Command(CommandId.GENERATE_T3)
            return Command(CommandId.NULL)
        else:
            return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[0]

    def toDictionary(self, map):
        #print("x e y del zerg builder ", self.x, self.y)
        #x, y = map.getTileIndex(self.originX, self.originY)
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "zergBarracks",
            "building": self.building,
            "nombre": "Colmena",
            "funcion": "Engendrar unidades ofensivas"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
