from enum import IntEnum

class CommandId(IntEnum):
    MOVER = 1
    MOVER_CAMARA_ARRIBA = 2
    MOVER_CAMARA_ABAJO = 3
    MOVER_CAMARA_DERECHA = 4
    MOVER_CAMARA_IZQUIERDA = 5
    GENERAR_UNIDAD = 6
    ROTAR = 7
    ORDENAR = 8
    MINAR = 9
    MINAR_BUCLE = 10
    TRANSPORTAR_ORE = 11
class Command:
    def __init__(self, id):
        self.id = id
        self.params = []

    def addParameter(self, par):
        self.params.append(par)

    def setId(self, id):
        self.id = id