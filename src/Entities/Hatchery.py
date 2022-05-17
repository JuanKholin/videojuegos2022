import pygame


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

WHITE   = (255,255,255)
GENERATION_TIME = 10
MINERAL_COST = 50
WIDTH = 6
HEIGHT = 4
HP = 200
CAPACITY = 10
LIMIT_MEJORA = 10

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
    nSprites = 4
    options = [Options.BUILD_DEPOT_ZERG, Options.BUILD_BARRACKS_ZERG, Options.BUILD_REFINERY_ZERG, Options.DANYO_UPGRADE, Options.MINE_UPGRADE, Options.ARMOR_UPGRADE, Options.GENERATE_WORKER_ZERG]

    def __init__(self, xini, yini, player, map, building, raton):
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, map, player, CAPACITY)
        self.sprites = cargarSprites(HATCHERY_PATH, self.nSprites, False, BLUE2, 1.8, 0)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        deadSprites = Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)

        self.sprites += deadSprites
        self.image = self.sprites[self.index]
        self.operativeIndex = [0, 1, 2, 3]
        self.spawningIndex = [0, 1, 2, 3]
        self.finalImage = self.sprites[self.operativeIndex[self.indexCount]]
        self.raton = raton
        self.render = pygame.transform.scale(pygame.image.load(HATCHERY_RENDER), RENDER_SIZE)

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
        self.damageMineralUpCost = 25
        self.damageGasUpCost = 5
        self.armorMineralUpCost = 25
        self.armorGasUpCost = 5
        self.mineMineralUpCost = 25
        self.mineGasUpCost = 5


        self.type = BASE

    def execute(self, command_id):
        #if self.clicked:
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
            self.damageMineralUpCost += 25
            self.damageGasUpCost += 5
        elif command_id == CommandId.UPGRADE_SOLDIER_ARMOR and self.player.resources and self.player.gas >= self.armorGasUpCost and self.player.resources >= self.armorMineralUpCost and self.player.armorUpgrade <= LIMIT_MEJORA:
            self.player.resources -= self.armorMineralUpCost
            self.player.gas -= self.armorGasUpCost
            self.player.armorUpgrade += 1
            self.armorMineralUpCost += 25
            self.armorGasUpCost += 5
        elif command_id == CommandId.UPGRADE_WORKER_MINING and self.player.resources and self.player.resources >= self.mineMineralUpCost and self.player.gas >= self.mineGasUpCost and self.player.mineUpgrade != LIMIT_MEJORA:
            self.player.resources -= self.mineMineralUpCost
            self.player.gas -= self.mineGasUpCost
            self.player.mineUpgrade += 1
            self.mineMineralUpCost += 25
            self.mineGasUpCost += 5
        elif command_id == CommandId.BUILD_REFINERY and self.player.resources >= EXTRACTOR_MINERAL_COST:
            self.raton.building = True
            self.raton.buildStructure = self.getZergRefinery()
        elif command_id == CommandId.BUILD_DEPOT and self.player.resources >= SUPPLY_ZERG_MINERAL_COST:
            self.raton.building = True
            self.raton.buildStructure = self.getZergSupply()
        elif command_id == CommandId.BUILD_BARRACKS and self.player.resources >= BARRACKS_ZERG_MINERAL_COST:
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
            "nombre": "Criadera de Zerg",
            "funcion": "Base enemiga"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
