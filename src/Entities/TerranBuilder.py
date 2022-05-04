import pygame
from .TerranWorker import *
from .. import Player, Map, Tile
from .Structure import *
from ..Command import *
from .Entity import *
from src.Utils import *
from .TerranBarracks import *
from .TerranRefinery import *
from .Hatchery import *

HP = 200
GENERATION_TIME = 40
MINERAL_COST = 600
LIMIT_MINADO = 1600

class TerranBuilder(Structure):
    sprites = []
    training = []
    rectOffY = 3
    generationTime = 0
    generationCount = 0
    heightPad = 25
    nBuildSprites = 4
    hola = 0
    tileW = 5
    tileH = 4
    clicked = False
    frame = 8

    def __init__(self, xini, yini, player, map, building, raton, id):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, id, player)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        self.sprites = cargarSprites(TERRAN_BUILDER_PATH, 6, False, WHITE, 1.5)
        #+ Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)
        self.raton = raton
        self.image = self.sprites[self.index]
        self.operativeIndex = [4]
        self.spawningIndex = [4, 5]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]

        self.render = pygame.transform.scale(pygame.image.load(BUILDER_RENDER), RENDER_SIZE)
        
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE
        self.count = 0

        self.training = []
        self.paths = []

        #MEJORAR LAS UNIDADES
        self.dañoUpCost = 50
        self.armorUpCost = 50
        self.mineUpCost = 50

    #def generateUnit(self, unit):
    #    pass

    def getOrder(self):
        return CommandId.TRANSPORTAR_ORE_STILL

    def execute(self, command_id):
        if self.clicked:
            if (command_id == CommandId.GENERAR_UNIDAD or command_id == CommandId.GENERATE_WORKER) and self.player.resources >= TERRAN_WORKER_MINERAL_COST:
                self.player.resources -= TERRAN_WORKER_MINERAL_COST
                terranWorker = TerranWorker(self.x / 40, (self.y + self.rectn.h) / 40, self.player)
                print("xd")
                self.generateUnit(terranWorker)
                self.state = BuildingState.SPAWNING
            elif command_id == CommandId.MEJORAR_DAÑO_SOLDADO and self.player.resources and self.player.resources >= self.dañoUpCost:
                self.player.resources -= self.dañoUpCost
                self.player.dañoUpgrade += 1
                self.dañoUpCost += 50
            elif command_id == CommandId.MEJORAR_ARMADURA_SOLDADO and self.player.resources and self.player.resources >= self.armorUpCost:
                self.player.resources -= self.armorUpCost
                self.player.armorUpgrade += 1
                self.armorUpCost += 50
            elif command_id == CommandId.MEJORAR_MINADO_WORKER and self.player.resources and self.player.resources >= self.mineUpCost and self.player.mineUpgrade != LIMIT_MINADO:
                self.player.resources -= self.mineUpCost
                self.player.mineUpgrade += 200
                self.mineUpCost += 50
            elif command_id == CommandId.BUILD_BARRACKS and self.player.resources >= TERRAN_BARRACK_MINERAL_COST:
                self.raton.building = True
                self.raton.buildStructure = self.getTerranBarrack()
            elif command_id == CommandId.BUILD_HATCHERY and self.player.resources >= HATCHERY_MINERAL_COST:
                self.raton.building = True
                self.raton.buildStructure = self.getHatchery()
            elif command_id == CommandId.BUILD_REFINERY and self.player.resources >= TERRAN_REFINERY_MINERAL_COST:
                self.raton.building = True
                self.raton.buildStructure = self.getTerranRefinery()

    def command(self, command):
        if command == CommandId.BUILD_BARRACKS:
            return Command(CommandId.BUILD_BARRACKS)
        elif command == CommandId.BUILD_REFINERY:
            return Command(CommandId.BUILD_REFINERY)
        elif command == CommandId.BUILD_HATCHERY:
            return Command(CommandId.BUILD_HATCHERY)
        elif command == CommandId.GENERAR_UNIDAD:
            return Command(CommandId.GENERAR_UNIDAD)
        elif command == CommandId.MEJORAR_ARMADURA_SOLDADO:
            return Command(CommandId.MEJORAR_ARMADURA_SOLDADO)
        elif command == CommandId.MEJORAR_DAÑO_SOLDADO:
            return Command(CommandId.MEJORAR_DAÑO_SOLDADO)
        elif command == CommandId.MEJORAR_MINADO_WORKER:
            return Command(CommandId.MEJORAR_MINADO_WORKER)
        else:
            return Command(CommandId.NULO)

    def getBuildSprite(self):
        return self.sprites[self.operativeIndex]
    
    def getOptions(self):
        #return [Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.GENERATE_WORKER, Options.BUILD_BARRACKS]
        return [Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.BUILD_REFINERY]

    def getTerranBarrack(self):
        return TerranBarracks(0, 0, None, self.mapa, True, 5)

    def getHatchery(self):
        return Hatchery(0, 0, None, self.mapa, False, 8)
    
    def getTerranRefinery(self):
        return TerranRefinery(0, 0, None, self.mapa, True, 8)

    def toDictionary(self, map):
        #x, y = map.getTileIndex(self.originX, self.originY)
        return {
            "clase": "terranBuilder",
            "x": self.xIni,
            "y": self.yIni,
            "building": self.building,
            "id": self.id,
        }
