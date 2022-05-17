from enum import IntEnum, auto

class CommandId(IntEnum):
    NULL = auto()
    MOVE = auto()
    MOVE_CAMERA_UP = auto()
    MOVE_CAMERA_DOWN = auto()
    MOVE_CAMERA_RIGHT = auto()
    MOVE_CAMERA_LEFT = auto()
    GENERATE_UNIT = auto()
    ROTATE = auto()
    ORDER = auto()
    MINE = auto()
    TRANSPORTAR_ORE = auto()
    TRANSPORTAR_ORE_STILL = auto()
    BUILD_BARRACKS = auto()
    BUILD_STRUCTURE = auto()
    BUILD_DEPOT = auto()
    BUILD_HATCHERY = auto()
    SAVE_GAME = auto()
    ATTACK = auto()
    GENERATE_WORKER = auto()
    GENERATE_T1 = auto()
    GENERATE_T2 = auto()
    GENERATE_T3 = auto()
    UPGRADE_SOLDIER_DAMAGE = auto()
    UPGRADE_SOLDIER_ARMOR = auto()
    UPGRADE_WORKER_MINING = auto()
    BUILD_REFINERY = auto()
    EXTRACT_GAS = auto()
    SEARCH_NEARBY_RIVAL = auto()
    NEXT_PAGE = auto()
    PREVIOUS_PAGE = auto()
    RETURN_GAME = auto()

class Command:
    def __init__(self, id):
        self.id = id
        self.params = []

    def addParameter(self, par):
        self.params.append(par)

    def setId(self, id):
        self.id = id
