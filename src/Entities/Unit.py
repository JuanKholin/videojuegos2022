from . import Entity


class Unit(Entity.Entity):
    def __init__(self, hp, xIni, yIni, mineral_cost, generation_time, speed, framesToRefresh, 
                sprites, face, frame, padding, id, player):
        Entity.Entity.__init__(self, hp, xIni, yIni, mineral_cost, generation_time, id, player)
        self.paths = []
        self.clicked = False
        self.angle = 0
        self.speed = speed
        self.rectOffY = padding
        self.face = face
        self.frame = frame
        self.framesToRefresh = framesToRefresh
        self.count = 0
        self.spritesName = sprites
        self.sprites = []
        self.distanceToPoint = 0

    def update(self):
        pass
