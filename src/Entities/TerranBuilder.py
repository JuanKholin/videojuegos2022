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
    TILES_HEIGHT = 4
    TILES_WIDTH = 5
    CENTER_TILE = [2, 2]
    sprites = []
    training = []
    rectOffY = 3
    generationTime = 0
    generationCount = 0
    heightPad = 25
    nBuildSprites = 4
    tileW = 5
    tileH = 4
    clicked = False
    frame = 8

    def __init__(self, xini, yini, player, map, building, raton):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, player)
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

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE
        self.count = 0

        self.training = []
        self.paths = []

        #MEJORAR LAS UNIDADES
        self.dañoMineralUpCost = 50
        self.dañoGasUpCost = 50
        self.armorMineralUpCost = 50
        self.armorGasUpCost = 50
        self.mineMineralUpCost = 50
        self.mineGasUpCost = 50

        self.type = TERRAN_BASE

    #def generateUnit(self, unit):
    #    pass

    def getOrder(self):
        return CommandId.TRANSPORTAR_ORE_STILL

    def execute(self, command_id):
        #if self.clicked:
        if (command_id == CommandId.GENERATE_UNIT or command_id == CommandId.GENERATE_WORKER) and self.player.resources >= TERRAN_WORKER_MINERAL_COST:
            self.player.resources -= TERRAN_WORKER_MINERAL_COST
            terranWorker = TerranWorker(self.x / 40, (self.y + self.rectn.h) / 40, self.player)
            print("xd")
            self.generateUnit(terranWorker)
            self.state = BuildingState.SPAWNING
        elif command_id == CommandId.UPGRADE_SOLDIER_DAMAGE and self.player.resources and self.player.resources >= self.dañoMineralUpCost and self.player.gas >= self.dañoGasUpCost:
            self.player.resources -= self.dañoMineralUpCost
            self.player.gas -= self.dañoGasUpCost
            self.player.dañoUpgrade += 1
            self.dañoMineralUpCost += 25
            self.dañoGasUpCost += 25
        elif command_id == CommandId.UPGRADE_SOLDIER_ARMOR and self.player.resources and self.player.gas >= self.armorGasUpCost and self.player.resources >= self.armorMineralUpCost:
            self.player.resources -= self.armorMineralUpCost
            self.player.gas -= self.armorGasUpCost
            self.player.armorUpgrade += 1
            self.armorMineralUpCost += 25
            self.armorGasUpCost += 25
        elif command_id == CommandId.UPGRADE_WORKER_MINING and self.player.resources and self.player.resources >= self.mineMineralUpCost and self.player.gas >= self.mineGasUpCost and self.player.mineUpgrade != LIMIT_MINADO:
            self.player.resources -= self.mineMineralUpCost
            self.player.gas -= self.mineGasUpCost
            self.player.mineUpgrade += 200
            self.mineMineralUpCost += 25
            self.mineGasUpCost += 25
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
        if (command == CommandId.BUILD_BARRACKS) or (command == CommandId.BUILD_REFINERY) or (command ==
                CommandId.BUILD_HATCHERY) or (command == CommandId.GENERATE_UNIT) or (command ==
                CommandId.UPGRADE_SOLDIER_ARMOR) or (command ==
                CommandId.UPGRADE_SOLDIER_DAMAGE) or (command == CommandId.UPGRADE_WORKER_MINING):
            return Command(command)
        else:
            return Command(CommandId.NULL)

    def getBuildSprite(self):
        return self.sprites[self.operativeIndex]

    def getOptions(self):
        if DEBBUG == True:
            return [Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.BUILD_REFINERY, Options.BUILD_HATCHERY, Options.DANYO_UPGRADE, Options.MINE_UPGRADE, Options.ARMOR_UPGRADE]
        else:
            return [Options.GENERATE_WORKER, Options.BUILD_BARRACKS, Options.BUILD_REFINERY, Options.DANYO_UPGRADE, Options.MINE_UPGRADE, Options.ARMOR_UPGRADE]

    def getTerranBarrack(self):
        return TerranBarracks(0, 0, None, self.mapa, True)

    def getHatchery(self):
        return Hatchery(0, 0, None, self.mapa, False)

    def getTerranRefinery(self):
        return TerranRefinery(0, 0, None, self.mapa, True)

    def toDictionary(self, map):
        #x, y = map.getTileIndex(self.originX, self.originY)
        return {
            "clase": "terranBuilder",
            "x": self.xIni,
            "y": self.yIni,
            "building": self.building,
            "nombre": "Base de comandos",
            "funcion": "Protege la base de comandos"
        }
