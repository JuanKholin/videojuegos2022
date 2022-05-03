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

class TerranBarracks(Structure):
    sprites = []
    training = []
    generationTime = 0
    generationCount = 0
    nBuildSprites = 4
    deafault_index = 4
    generationStartTime = 0
    heightPad = 5
    rectOffY = 8
    tileW = 4
    tileH = 3
    clicked = False
    frame = 8

    def __init__(self, xini, yini, player, map, building, id):
        Structure.__init__(self, HP, TERRAN_BARRACK_MINERAL_COST, GENERATION_TIME, xini, yini, map, id, player)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        self.sprites = cargarSprites(TERRAN_BARRACK_PATH, 6, False, WHITE, 
                1.1) + Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)
        
        self.image = self.sprites[self.index]
        self.operativeIndex = [4]
        self.spawningIndex = [4, 5]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]
        
        self.render = pygame.transform.scale(pygame.image.load(BARRACKS_RENDER), RENDER_SIZE)

        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE

        self.training = []
        self.paths = []

    def execute(self, command_id):
        if self.clicked:
            print("soy clickeado?")
            if (command_id == CommandId.GENERAR_UNIDAD or command_id == CommandId.GENERATE_SOLDIER) and self.player.resources >= TERRAN_WORKER_MINERAL_COST:
                self.player.resources -= TERRAN_WORKER_MINERAL_COST
                terranSoldier = TerranSoldier(self.x / 40, (self.y + self.rectn.h) / 40, self.player)
                self.generateUnit(terranSoldier)
                self.state = BuildingState.SPAWNING

    def command(self, command):
        if self.state != BuildingState.BUILDING:
            if command == CommandId.BUILD_STRUCTURE:
                return Command(CommandId.BUILD_BARRACKS)
            elif command == CommandId.GENERAR_UNIDAD:
                return Command(CommandId.GENERAR_UNIDAD)
            return Command(CommandId.NULO)
        else:
            print(3)
            return Command(CommandId.NULO)

    def getBuildSprite(self):
        return self.sprites[4]
    
    def getOptions(self):
        return [Options.GENERATE_SOLDIER]

    def toDictionary(self, map):
        #print("barracke x e y Ini ", self.xIni, self.yIni)
        #x, y = map.getTileIndex(self.originX, self.originY)
        return {
            "clase": "terranBarracks",
            "x": self.xIni,
            "y": self.yIni,
            "building": self.building,
            "id": self.id,
        }
