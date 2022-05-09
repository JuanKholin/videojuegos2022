import pygame as pg



from .Entity import *
from ..Utils import *
from .Worker import *

# Constantes
HP = 40
ATTACK_INFO = [0, 0, 0]
ATTACK_INFO[DAMAGE_IND] = 1
ATTACK_INFO[COOLDOWN_IND] = 7
ATTACK_INFO[RANGE_IND] = 67
MINE_POWER = 8
MINERAL_COST = 50
TIME_TO_MINE = 2000
GENERATION_TIME = 2
speed = 2
FRAMES_TO_REFRESH = 10
SPRITES = "scvJusto.bmp"
SCALE = 1.5
SPRITE_PIXEL_ROWS = 72
FACES = 8
FRAME = 0
#Esto es mentira, salen 220 frames no 296
TOTAL_FRAMES = 296  # [0:15] MOVERSE Y STILL
                    # [16:31] MOVER ORE
                    # [32:47] MOVER BARRIL
                    # [48:217] ATACAR Y MINAR
                    # [289:295] MORICION
FRAMES = [list(range(1, 17)), list(range(18, 34)), list(range(35, 51)),
          list(range(52, 68)), list(range(69, 85)), list(range(86, 102)),
          list(range(103, 119)), list(range(120, 136)), list(range(137, 153)),
          list(range(154, 170)), list(range(171, 187)), list(range(188, 204)),
          list(range(205, 221)), [221] * 16, [222] * 16, [223] * 16, [224] * 16,
          [225] * 16, [226] * 16, [227] * 16, [228] * 16, [229] * 16, [230] * 16]
STILL_FRAMES = [0]
ORE_TRANSPORTING_FRAMES = [3]
BARREL_TRANSPORTING_FRAMES = [2]
ATTACK_FRAMES = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12]
MOVE_FRAMES = [0]
DIE_FRAMES = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

INVERSIBLE_FRAMES = len(FRAMES) - len(DIE_FRAMES) # los die frames no se invierten
# Cada ristra de frames es un frame en todas las direcciones, por lo que en sentido
# horario y empezando desde el norte, el mapeo dir-flist(range(289, 296))rame es:
DIR_OFFSET = [0, 2, 4, 6, 8, 10, 12, 14, 15, 13, 11, 9, 7, 5, 3, 1]
WEIGHT_PADDING =    60
HEIGHT_PADDING =    60
X_PADDING =         25
Y_PADDING =         30
PADDING = 110

class TerranWorker(Worker):
    def __init__(self, xIni, yIni, player):
        Worker.__init__(self, HP, xIni * TILE_WIDTH + 20, yIni * TILE_HEIGHT, MINERAL_COST,
                GENERATION_TIME, speed, FRAMES_TO_REFRESH, SPRITES, FACES, FRAME,
                PADDING,  takeID(), player, MINE_POWER, TIME_TO_MINE, INVERSIBLE_FRAMES,
                FRAMES, DIR_OFFSET, ATTACK_FRAMES, STILL_FRAMES, MOVE_FRAMES, DIE_FRAMES, X_PADDING,
                Y_PADDING, WEIGHT_PADDING, HEIGHT_PADDING, ORE_TRANSPORTING_FRAMES,BARREL_TRANSPORTING_FRAMES, ATTACK_INFO)
        #print(self.speed)
        spritesheet = pg.image.load("./sprites/" + self.spritesName).convert()
        spritesheet.set_colorkey(BLACK)
        deadSpritesheet = pg.image.load("./sprites/explosion1.bmp").convert()
        deadSpritesheet.set_colorkey(BLACK)
        self.sprites = Entity.divideSpritesheetByRows(spritesheet,
                SPRITE_PIXEL_ROWS, SCALE) + Entity.divideSpritesheetByRowsNoScale(deadSpritesheet, 200)
        self.mirrorTheChosen()
        self.dir = 8
        self.changeToStill()
        self.updateOwnSpace()
        #self.imageRect = rect(self.x, self.y, self.image.get_width() - WEIGHT_PADDING,
                #self.image.get_height() - HEIGHT_PADDING)
        #self.imageRect = rect(self.x - self.image.get_width()/2, self.y -self.image.get_height() , self.image.get_width(), self.image.get_height())
        #self.imageRect = rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.render = pygame.transform.scale(pygame.image.load(WORKER_RENDER), UNIT_RENDER_SIZE)

        self.type = TERRAN_WORKER

    def getUpgrades(self):
        upgrades = []
        if self.player.mineUpgrade == 0:
            upgrades.append({'upgrade': Upgrades.NO_MINE, 'cantidad': 0})
        else:
            upgrades.append({'upgrade': Upgrades.MINE, 'cantidad': int(self.player.mineUpgrade/200)})
        if self.player.armorUpgrade == 0:
            upgrades.append({'upgrade': Upgrades.NO_ARMOR, 'cantidad': 0})
        else:
            upgrades.append({'upgrade': Upgrades.ARMOR, 'cantidad': self.player.armorUpgrade})
        if self.player.dañoUpgrade == 0:
            upgrades.append({'upgrade': Upgrades.NO_DANYO, 'cantidad': 0})
        else:
            upgrades.append({'upgrade': Upgrades.DANYO, 'cantidad': self.player.dañoUpgrade})
        return upgrades

    def toDictionary(self, map):
        fatherDictionary = super().toDictionary(map)
        sonDictionary = {
            "clase": "terranWorker",
            "nombre": "Terran Worker",
            "funcion": "Unidad obrera"
        }
        sonDictionary.update(fatherDictionary)
        return sonDictionary
