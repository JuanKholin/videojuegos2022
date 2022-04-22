from . import Unit

class Zerg(Unit.Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, faces, frames, padding, id, player):
        Unit.Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, faces, frames, padding, id, player)
