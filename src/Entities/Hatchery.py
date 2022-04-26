import pygame
from .Structure import *
from .. import Player, Map, Utils, Tile
from ..Command import *
from src.Utils import *
from .Drone import *

GENERATION_TIME = 10
MINERAL_COST = DRONE_MINERAL_COST
HP = 10


class Hatchery(Structure):
    sprites = []
    training = []
    heightPad = 100
    widthPad = -20
    rectOffY = 5

    def __init__(self, xini, yini, player, map):
        (x, y) = map.getTileCenter(xini, yini)
        x -= 20
        y -= 10
        Structure.__init__(self, HP, MINERAL_COST, GENERATION_TIME, xini, yini, takeID(), player)
        self.player = player
        self.sprites = cargarSprites(HATCHERY_PATH, 4, False, BLUE, 1.8)
        self.map = map
        self.generationCount = 0
        self.image = self.sprites[self.index]
        self.image.set_colorkey(BLUE)
        self.rectn = pygame.Rect(x, y, self.sprites[0].get_width() + self.widthPad, self.sprites[0].get_height() - self.heightPad)
        self.count = 0
        self.framesToRefresh = 10
        self.paths = []

    def update(self):
        if len(self.training) > 0:
            self.generationCount += 1
            if self.generationCount == CLOCK_PER_SEC * self.training[0].generationTime:
                unit = self.training[0]
                unitPos = unit.getPosition()
                unitTile = self.map.getTile(unitPos[0], unitPos[1])
                if unitTile.type != 0:
                    vecinas = self.map.getTileVecinas(unitTile)
                    unit.setTilePosition(vecinas[0])
                self.player.addUnits(unit)
                self.generationCount = 0
                del self.training[0]
        self.count += 1
        if self.count >= self.framesToRefresh:
            self.count = 0
            self.index = self.index + 1
            self.index = self.index % 4
            self.image = self.sprites[self.index]
            self.image.set_colorkey(BLUE)

    def generateUnit(self, unit):
        self.training.append(unit)

    def execute(self, command_id):
        if self.clicked:
            if command_id == CommandId.GENERAR_UNIDAD and self.player.resources >= self.mineralCost:
                self.player.resources -= self.mineralCost
                drone = Drone(self.x / 40, (self.y + self.rectn.h) / 40, 1)
                self.generateUnit(drone)
