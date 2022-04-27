import pygame
from .Zergling import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *

WHITE   = (255,255,255)

class ZergBuilder(Structure):
    sprites = []
    training = []
    heightPad = 10
    generationTime = 0
    generationCount = 0
    widthPad = -20
    rectOffY = 90
    tileW = 6
    clicked = False
    tileH = 4

    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, building, id):
        Structure.__init__(self, hp, mineralCost, generationTime, xini, yini, map, id, player)
        self.sprites = cargarSprites(HATCHERY_PATH, 4, False, BLUE, 1.8)
        self.building = building
        self.image = self.sprites[self.index]
        self.finalImage = self.sprites[3]

        self.count = 0
        self.training = []
        self.paths = []
        
    def update(self):
        if self.building:
            self.building = False
        elif len(self.training) > 0:
            self.updateTraining()
        self.index = (self.index + frame(8)) % 4
        self.image = self.sprites[self.index]
        self.image.set_colorkey(BLUE)

    def execute(self, command_id):
        if self.clicked:
            if command_id == CommandId.GENERAR_UNIDAD and self.player.resources >= ZERGLING_MINERAL_COST:
                self.player.resources -= ZERGLING_MINERAL_COST
                zergling = Zergling(self.x / 40, (self.y + self.rectn.h) / 40, 1)
                self.generateUnit(zergling)
            
                
    def command(self, command):
        if command == CommandId.BUILD_STRUCTURE:
            return Command(CommandId.BUILD_ZERG_BUILDER)
        elif command == CommandId.GENERAR_UNIDAD:
            return Command(CommandId.GENERAR_UNIDAD)
        else:
            return Command(CommandId.NULO)
        
    def getBuildSprite(self):
        return self.sprites[3]
