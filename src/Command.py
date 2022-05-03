from enum import IntEnum

class CommandId(IntEnum):
    NULO = 0
    MOVER = 1
    MOVER_CAMARA_ARRIBA = 2
    MOVER_CAMARA_ABAJO = 3
    MOVER_CAMARA_DERECHA = 4
    MOVER_CAMARA_IZQUIERDA = 5
    GENERAR_UNIDAD = 6
    ROTAR = 7
    ORDENAR = 8
    MINE = 9
    MINAR_BUCLE = 10
    TRANSPORTAR_ORE = 11
    TRANSPORTAR_ORE_STILL = 12
    BUILD_BARRACKS = 13
    BUILD_STRUCTURE = 14
    BUILD_ZERG_BUILDER = 15
    GUARDAR_PARTIDA = 16
    ATTACK = 17
    GENERATE_WORKER = 18
    GENERATE_SOLDIER = 19
    MEJORAR_DAÑO_SOLDADO = 20
    MEJORAR_ARMADURA_SOLDADO = 21
    MEJORAR_MINADO_WORKER = 22

class Command:
    def __init__(self, id):
        self.id = id
        self.params = []

    def addParameter(self, par):
        self.params.append(par)

    def setId(self, id):
        self.id = id
