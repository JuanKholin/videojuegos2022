import pygame as pg


from .. import Command

from .Entity import *
from ..Utils import *
from .Soldier import *
from ..Music import *

# Constantes
HP = 175
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 6
ATTACK_INFO[COOLDOWN_IND] = 10
ATTACK_INFO[RANGE_IND] = 2 * RANGE_UNIT + RANGE_BASIC
MINE_POWER = 0
MINERAL_COST = 50
GAS_COST = 20
TIME_TO_MINE = 1000
GENERATION_TIME = 30
SPEED = 4
FRAMES_TO_REFRESH = 3
FACES = 8
FRAME = 0
                    

WEIGHT_PADDING =    10
HEIGHT_PADDING =    10
X_PADDING =         20
Y_PADDING =         15
PADDING = 20

IS_EXPLOSIVE = True

class Firebat(Soldier):
    generateSound = soldierGenerateSound
    deadSound = soldierDeadSound
    attackSound = firebatAttackSound 
    
    def __init__(self, player, xIni = -1, yIni = -1):
        Soldier.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST,
                GENERATION_TIME, SPEED, FRAMES_TO_REFRESH, FACES, FRAME,
                PADDING,  takeID(), player, FIREBAT_INVERSIBLE_FRAMES, FIREBAT_FRAMES, DIR_OFFSET, FIREBAT_ATTACK_FRAMES,
                FIREBAT_STILL_FRAMES, FIREBAT_MOVE_FRAMES, FIREBAT_DIE_FRAMES, X_PADDING,
                Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ATTACK_INFO, IS_EXPLOSIVE)

        sprites = Utils.FIREBAT_SPRITES
        self.sprites = sprites[0]
        self.shadows = sprites[1]
        self.dir = 8
        self.changeToStill()
        if xIni != -1:
            self.updateOwnSpace()
        #self.imageRect = rect(self.x, self.y, self.image.get_width() - WEIGHT_PADDING,
                #self.image.get_height() - HEIGHT_PADDING)
        #self.imageRect = rect(self.x - self.image.get_width()/2, self.y -self.image.get_height() , self.image.get_width(), self.image.get_height())
        #self.imageRect = rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.render = pg.transform.scale(pg.image.load(TERRAN_T2_RENDER), UNIT_RENDER_SIZE)
        self.type = SOLDIER

    def makeAnAttack(self):
        for tile in self.mapa.getAllTileVecinas(self.attackedOne.getTile()):
            if tile.type == UNIT and tile.ocupante.player != self.player:
                tile.ocupante.beingAttacked(self.damage + self.player.dañoUpgrade, self)
        hpLeft = self.attackedOne.beingAttacked(self.damage + self.player.dañoUpgrade, self)
        if hpLeft <= 0:
            #print("Se queda sin vida")
            enemy = self.mapa.getNearbyRival(self.occupiedTile, self.player)
            if enemy != None:
                self.attack(enemy)
            else:
                self.changeToStill()

    def toDictionary(self, map):
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "firebat",
            "nombre": "Firebat",
            "funcion": "Unidad Terran de daño en area"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
