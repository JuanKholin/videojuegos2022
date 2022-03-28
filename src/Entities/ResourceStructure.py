from . import Structure

class ResourceStructure(Structure.Structure):
    def __init__(self, hp, mineralCost, generationTime):
        super.__init__(hp, mineralCost)
        self.generationTime = generationTime

    def update():
        pass