import pygame

from .TerranSoldier import *
from .TerranWorker import *
from .TerranBarracks import *
from .TerranRefinery import *
from .TerranSupplyDepot import *
from .Hatchery import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from .Entity import *
from ..Utils import *

HP = 1500
GENERATION_TIME = 120
MINERAL_COST = 400
LIMIT_MEJORA = 10
CAPACITY = 10

class TerranBuilder(Structure):
    TILES_HEIGHT = 4
    TILES_WIDTH = 5
    CENTER_TILE = [2, 2]
    sprites = []
    training = []
    rectOffY = 3
    generationTime = 0
    generationCount = 0
    HEIGHT_PAD = 25
    nBuildSprites = 4
    clicked = False
    frame = 8
    nSprites = 6
    options = [Options.BUILD_DEPOT_TERRAN, Options.BUILD_BARRACKS_TERRAN, Options.BUILD_REFINERY_TERRAN, 
            Options.DANYO_UPGRADE, Options.MINE_UPGRADE, Options.ARMOR_UPGRADE, Options.GENERATE_WORKER_TERRAN]

    def __init__(self, xini, yini, player, map, building, raton):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        self.sprites = cargarSprites(TERRAN_BUILDER_PATH, self.nSprites, False, WHITE, 1.5)

        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        deadSprites = Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.sprites += deadSprites

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
        self.damageMineralUpCost = 25
        self.damageGasUpCost = 5
        self.armorMineralUpCost = 25
        self.armorGasUpCost = 5
        self.mineMineralUpCost = 25
        self.mineGasUpCost = 5

        self.type = BASE
       
        ("ESTOY SIENDO CREADO ", self.toDictionary(self.mapa)['clase'])


    #def generateUnit(self, unit):
    #    pass

    def getOrder(self):
        if self.state != BuildingState.BUILDING and self.state != BuildingState.COLLAPSING and self.state!= BuildingState.DESTROYED: 
            return CommandId.TRANSPORTAR_ORE_STILL
        else:
            return CommandId.NULL

    def execute(self, command_id):
        #if self.clicked:
        if self.state != BuildingState.BUILDING and self.state != BuildingState.COLLAPSING and self.state != BuildingState.DESTROYED:
            
            if (command_id == CommandId.GENERATE_UNIT or command_id == CommandId.GENERATE_WORKER) and self.player.resources >= TERRAN_WORKER_MINERAL_COST:
                if len(self.player.units) + 1 <= (self.player.limitUnits):
                    self.player.resources -= TERRAN_WORKER_MINERAL_COST
                    terranWorker = TerranWorker(self.player)
                    #print("xd")
                    self.generateUnit(terranWorker)
                    self.state = BuildingState.SPAWNING
            elif command_id == CommandId.UPGRADE_SOLDIER_DAMAGE and self.player.resources and self.player.resources >= self.damageMineralUpCost and self.player.gas >= self.damageGasUpCost and self.player.dañoUpgrade <= LIMIT_MEJORA:
                self.player.resources -= self.damageMineralUpCost
                self.player.gas -= self.damageGasUpCost
                self.player.dañoUpgrade += 1
                self.damageMineralUpCost += 25
                self.damageGasUpCost += 5
            elif command_id == CommandId.UPGRADE_SOLDIER_ARMOR and self.player.resources and self.player.gas >= self.armorGasUpCost and self.player.resources >= self.armorMineralUpCost and self.player.armorUpgrade <= LIMIT_MEJORA:
                self.player.resources -= self.armorMineralUpCost
                self.player.gas -= self.armorGasUpCost
                self.player.armorUpgrade += 1
                self.armorMineralUpCost += 25
                self.armorGasUpCost += 5
            elif command_id == CommandId.UPGRADE_WORKER_MINING and self.player.resources and self.player.resources >= self.mineMineralUpCost and self.player.gas >= self.mineGasUpCost and self.player.mineUpgrade <= LIMIT_MEJORA:
                self.player.resources -= self.mineMineralUpCost
                self.player.gas -= self.mineGasUpCost
                self.player.mineUpgrade += 1
                self.mineMineralUpCost += 25
                self.mineGasUpCost += 5
            elif command_id == CommandId.BUILD_BARRACKS and self.player.resources >= TERRAN_BARRACKS_MINERAL_COST:
                self.raton.building = True
                #print("mi raton: ", self.raton.id)
                self.raton.buildStructure = self.getTerranBarrack()
            elif command_id == CommandId.BUILD_HATCHERY and self.player.resources >= HATCHERY_MINERAL_COST:
                self.raton.building = True
                self.raton.buildStructure = self.getHatchery()
            elif command_id == CommandId.BUILD_REFINERY and self.player.resources >= TERRAN_REFINERY_MINERAL_COST:
                self.raton.building = True
                self.raton.buildStructure = self.getTerranRefinery()
            elif command_id == CommandId.BUILD_DEPOT and self.player.resources >= TERRAN_DEPOT_MINERAL_COST:
                self.raton.building = True
                self.raton.buildStructure = self.getTerranSupply()

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

    def getTerranBarrack(self):
        return TerranBarracks(0, 0, None, self.mapa, True)

    def getHatchery(self):
        return Hatchery(0, 0, None, self.mapa, False)

    def getTerranRefinery(self):
        return TerranRefinery(0, 0, None, self.mapa, True)
    
    def getTerranSupply(self):
        return TerranSupplyDepot(0, 0, None, self.mapa, True)

    def toDictionary(self, map):
        #x, y = map.getTileIndex(self.originX, self.originY)
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "terranBuilder",
            "building": self.building,
            "nombre": "Centro de comandos",
            "funcion": "Construir y construir SCV",
            "damageMineralUpCost": self.damageMineralUpCost,
            "damageGasUpCost": self.damageGasUpCost,
            "armorMineralUpCost": self.armorMineralUpCost,
            "armorGasUpCost": self.armorGasUpCost,
            "mineMineralUpCost": self.mineMineralUpCost,
            "mineGasUpCost": self.mineGasUpCost,
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
