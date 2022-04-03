from . import Entity

class Structure(Entity.Entity):
    

    def s__init__(self, hp, mineralCost, generationTime, id):
        Entity.Entity.__init__(self, hp, mineralCost, generationTime, id)
    def getPosition(self):
        return (self.rectn.x, self.rectn.y)

    def update():
        pass
