import pygame as pg


from .Zergling import *
from .Drone import *
from .ZergBarracks import *
from .ZergSupply import *
from .Extractor import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *
from .Entity import *

GENERATION_TIME = 40
MINERAL_COST = 50
WIDTH = 6
HEIGHT = 4
HP = 2000
CAPACITY = 10
LIMIT_MEJORA = 10
VISION_RADIUS = 9
DAMAGE_MINERAL_UP_COST = [30, 60, 100, 150, 200, 250, 250, 250, 250, 300]
DAMAGE_GAS_UP_COST = [10, 20, 50, 100, 150, 200, 200, 200, 200, 200, 200]
ARMOR_MINERAL_UP_COST = [30, 60, 100, 150, 200, 250, 250, 250, 250, 300]
ARMOR_GAS_UP_COST = [10, 20, 50, 100, 150, 200, 200, 200, 200, 200, 200]
MINE_MINERAL_UP_COST = [30, 60, 100, 150, 200, 250, 250, 250, 250, 300]
MINE_GAS_UP_COST = [10, 20, 50, 100, 150, 200, 200, 200, 200, 200, 200]


class Hatchery(Structure):
    TILES_HEIGHT = 4
    TILES_WIDTH = 6
    CENTER_TILE = [2, 2]
    sprites = []
    training = []
    HEIGHT_PAD = 10
    generationTime = 0
    generationCount = 0
    rectOffY = 90
    clicked = False
    frame = 12
    nSprites = HATCHERY_TOTAL_FRAMES
    options = [Options.BUILD_DEPOT_ZERG, Options.BUILD_BARRACKS_ZERG, Options.BUILD_REFINERY_ZERG, Options.DANYO_UPGRADE, Options.MINE_UPGRADE, Options.ARMOR_UPGRADE, Options.GENERATE_WORKER_ZERG]
    selectedSound = zergStructureSelectedSound
    deadSound = zergStructureDead
    

    def __init__(self, xini, yini, player, map, building, raton):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        sprites = Utils.HATCHERY_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]
        self.nDeadSprite = len(self.sprites) - len(self.shadows)
        self.image = self.sprites[self.index]

        self.operativeIndex = [0, 1, 2, 3]
        self.spawningIndex = [0, 1, 2, 3]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]

        self.raton = raton
        self.render = pg.transform.scale(pg.image.load(HATCHERY_RENDER), RENDER_SIZE)

        self.visionRadius = VISION_RADIUS

        self.building = building
        if building:
            self.state = BuildingState.BUILDING
        else:
            self.state = BuildingState.OPERATIVE
        self.count = 0

        self.count = 0
        self.training = []
        self.paths = []
        self.building = False
        #MEJORAR LAS UNIDADES
        self.damageMineralUpCost = DAMAGE_MINERAL_UP_COST[0]
        self.damageGasUpCost = DAMAGE_GAS_UP_COST[0]
        self.armorMineralUpCost = ARMOR_MINERAL_UP_COST[0]
        self.armorGasUpCost = ARMOR_GAS_UP_COST[0]
        self.mineMineralUpCost = MINE_MINERAL_UP_COST[0]
        self.mineGasUpCost = MINE_GAS_UP_COST[0]


        self.type = BASE
        
    def updateUpgrade(self):
        self.damageMineralUpCost = DAMAGE_MINERAL_UP_COST[self.player.dañoUpgrade]
        self.damageGasUpCost = DAMAGE_GAS_UP_COST[self.player.dañoUpgrade]
        self.armorMineralUpCost = ARMOR_MINERAL_UP_COST[self.player.armorUpgrade]
        self.armorGasUpCost = ARMOR_GAS_UP_COST[self.player.armorUpgrade]
        self.mineMineralUpCost = MINE_MINERAL_UP_COST[self.player.mineUpgrade]
        self.mineGasUpCost = MINE_GAS_UP_COST[self.player.mineUpgrade]

    def execute(self, command_id):
        #if self.clicked:
        if self.state != BuildingState.BUILDING and self.state != BuildingState.COLLAPSING and self.state != BuildingState.DESTROYED:
    
            if command_id == CommandId.GENERATE_WORKER and self.player.resources >= ZERG_T1_MINERAL_COST:
                #print("Haciendo un zerg")
                self.player.resources -= ZERG_T1_MINERAL_COST
                zergling = Drone(self.player)
                self.generateUnit(zergling)
                self.frame = 4
                self.state = BuildingState.SPAWNING
            elif command_id == CommandId.UPGRADE_SOLDIER_DAMAGE and self.player.resources and self.player.resources >= self.damageMineralUpCost and self.player.gas >= self.damageGasUpCost and self.player.dañoUpgrade <= LIMIT_MEJORA:
                self.player.resources -= self.damageMineralUpCost
                self.player.gas -= self.damageGasUpCost
                self.player.dañoUpgrade += 1
                self.damageMineralUpCost = DAMAGE_MINERAL_UP_COST[self.player.dañoUpgrade]
                self.damageGasUpCost = DAMAGE_GAS_UP_COST[self.player.dañoUpgrade]
            elif command_id == CommandId.UPGRADE_SOLDIER_ARMOR and self.player.resources and self.player.gas >= self.armorGasUpCost and self.player.resources >= self.armorMineralUpCost and self.player.armorUpgrade <= LIMIT_MEJORA:
                self.player.resources -= self.armorMineralUpCost
                self.player.gas -= self.armorGasUpCost
                self.player.armorUpgrade += 1
                self.armorMineralUpCost = ARMOR_MINERAL_UP_COST[self.player.armorUpgrade]
                self.armorGasUpCost = ARMOR_GAS_UP_COST[self.player.armorUpgrade]
            elif command_id == CommandId.UPGRADE_WORKER_MINING and self.player.resources and self.player.resources >= self.mineMineralUpCost and self.player.gas >= self.mineGasUpCost and self.player.mineUpgrade != LIMIT_MEJORA:
                self.player.resources -= self.mineMineralUpCost
                self.player.gas -= self.mineGasUpCost
                self.player.mineUpgrade += 1
                self.mineMineralUpCost = MINE_MINERAL_UP_COST[self.player.mineUpgrade]
                self.mineGasUpCost = MINE_GAS_UP_COST[self.player.mineUpgrade]
            elif command_id == CommandId.BUILD_REFINERY and self.player.resources >= EXTRACTOR_MINERAL_COST:
                self.raton.building = True
                self.raton.buildStructure = self.getZergRefinery()
            elif command_id == CommandId.BUILD_DEPOT and self.player.resources >= ZERG_DEPOT_MINERAL_COST:
                self.raton.building = True
                self.raton.buildStructure = self.getZergSupply()
            elif command_id == CommandId.BUILD_BARRACKS and self.player.resources >= ZERG_BARRACKS_MINERAL_COST:
                self.raton.building = True
                #print("mi raton: ", self.raton.id)
                self.raton.buildStructure = self.getZergBarrack()

    def command(self, command):
        if command == CommandId.BUILD_STRUCTURE:
            return Command(CommandId.BUILD_HATCHERY)
        elif command == CommandId.GENERATE_WORKER:
            return Command(CommandId.GENERATE_WORKER)
        else:
            return Command(CommandId.NULL)

    def getOrder(self):
        if self.state != BuildingState.BUILDING and self.state != BuildingState.COLLAPSING and self.state!= BuildingState.DESTROYED:
            return CommandId.TRANSPORTAR_ORE_STILL
        else:
            return CommandId.NULL

    def getBuildSprite(self):
        return self.sprites[3]

    def getZergBarrack(self):
        return ZergBarracks(0, 0, None, self.mapa, True)
    def getZergSupply(self):
        return ZergSupply(0, 0, None, self.mapa, True)
    def getZergRefinery(self):
        return Extractor(0, 0, None, self.mapa, True)

    def toDictionary(self, map):
        #print("x e y del zerg builder ", self.x, self.y)
        #x, y = map.getTileIndex(self.originX, self.originY)
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "hatchery",
            "building": self.building,
            "nombre": "Criadero de Zerg",
            "funcion": "Construir y engendrar Drone"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
