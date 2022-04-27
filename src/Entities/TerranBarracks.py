import pygame
from .TerranWorker import *
from .Structure import *
from .. import Player, Map
from ..Command import *
from ..Utils import *

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
    
    def __init__(self, hp, mineralCost, generationTime, xini, yini, player, map, building, id):
        Structure.__init__(self, hp, mineralCost, generationTime, xini, yini, map, id, player)
        self.sprites = Utils.cargarSprites(Utils.TERRAN_BARRACK_PATH, 6, False, Utils.WHITE, 1.1)
        self.building = building
        self.image = self.sprites[self.index]
        self.finalImage = self.sprites[4]
 
        self.count = 0
        self.training = []
        self.paths = []

    def update(self):
        if self.building:
            self.updateBuilding(4)
        elif len(self.training) > 0:
            if frame(10) == 1:
                if self.index == 5:
                    self.index = 4
                else:
                    self.index = 5
            self.updateTraining()
        else:
            self.index = 4
        self.image = self.sprites[self.index]
        self.image.set_colorkey(WHITE)

    def execute(self, command_id):
        if self.clicked:
            print("soy clickeado?")
            if command_id == CommandId.GENERAR_UNIDAD and self.player.resources >= TERRAN_WORKER_MINERAL_COST:
                self.player.resources -= TERRAN_WORKER_MINERAL_COST
                terranWorker = TerranWorker(self.x / 40, (self.y + self.rectn.h) / 40, self.player)
                self.generateUnit(terranWorker)

    def command(self, command):
        if not self.building:
            if command == CommandId.BUILD_STRUCTURE:
                return Command(CommandId.BUILD_BARRACKS)
            elif command == CommandId.GENERAR_UNIDAD:
                return Command(CommandId.GENERAR_UNIDAD)
        else:
            return Command(CommandId.NULO)
        
    def getBuildSprite(self):
        return self.sprites[4]