from . import Unit

class Worker(Unit.Unit):
    def __init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, faces, frames, padding, id):
        Unit.Unit.__init__(self, hp, xini, yini, mineral_cost, generation_time, speed, framesToRefresh, sprites, faces, frames, padding, id)

    def update():
        pass

    def work():
        pass