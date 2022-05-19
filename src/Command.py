from enum import IntEnum, auto
import pygame

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
    PAUSE_GAME = auto()
    HELP = auto()
    SAVE_EXIT_GAME = auto()
    EXIT_GAME = auto()
    DESELECT = auto()
    PLUS_BGM = auto()
    MINUS_BGM = auto()
    PLUS_SOUND = auto()
    MINUS_SOUND = auto()

class Command:
    def __init__(self, id):
        self.id = id
        self.params = []

    def addParameter(self, par):
        self.params.append(par)

    def setId(self, id):
        self.id = id

COMMAND_TO_TEXT = {
  CommandId.NULL: "",
  CommandId.MOVE_CAMERA_UP: "Mover cámara arriba",
  CommandId.MOVE_CAMERA_DOWN: "Mover cámara abajo",
  CommandId.MOVE_CAMERA_RIGHT: "Mover cámara a la derecha",
  CommandId.MOVE_CAMERA_LEFT: "Mover cámara a la izquierda",
  CommandId.ROTATE: "Rotar unidad",
  CommandId.BUILD_BARRACKS: "Construir barracas",
  CommandId.BUILD_DEPOT: "Construir Depósito de recursos",
  CommandId.BUILD_REFINERY: "Construir refinería",
  CommandId.GENERATE_T1: "Generar unidad de combate de nivel 1",
  CommandId.GENERATE_T2: "Generar unidad de combate de nivel 2",
  CommandId.GENERATE_T3: "Generar unidad de combate de nivel 3",
  CommandId.GENERATE_WORKER: "Generar obrero",
  CommandId.UPGRADE_SOLDIER_DAMAGE: "Mejorar daño de los soldados",
  CommandId.UPGRADE_SOLDIER_ARMOR: "Mejorar armadura de los soldados",
  CommandId.UPGRADE_WORKER_MINING: "Mejorar tiempo de minado",
  CommandId.SAVE_GAME: "Guardar partida",
  CommandId.ROTATE: "Rotar unidad",
}

DEFAULT_KEY_MAP ={
  pygame.K_w: CommandId.MOVE_CAMERA_UP,
  pygame.K_s: CommandId.MOVE_CAMERA_DOWN,
  pygame.K_d: CommandId.MOVE_CAMERA_RIGHT,
  pygame.K_a: CommandId.MOVE_CAMERA_LEFT,
  pygame.K_e: CommandId.BUILD_BARRACKS,
  pygame.K_r: CommandId.BUILD_DEPOT,
  pygame.K_t: CommandId.BUILD_REFINERY,
  pygame.K_z: CommandId.GENERATE_T1,
  pygame.K_x: CommandId.GENERATE_T2,
  pygame.K_c: CommandId.GENERATE_T3,
  pygame.K_q: CommandId.GENERATE_WORKER,
  pygame.K_i: CommandId.UPGRADE_SOLDIER_DAMAGE,
  pygame.K_o: CommandId.UPGRADE_SOLDIER_ARMOR,
  pygame.K_p: CommandId.UPGRADE_WORKER_MINING,
  pygame.K_g: CommandId.SAVE_GAME,
  pygame.K_m: CommandId.ROTATE,
}

DEFAULT_COMMAND_MAP = {
 CommandId.MOVE_CAMERA_UP: pygame.K_w,
 CommandId.MOVE_CAMERA_DOWN: pygame.K_s,
 CommandId.MOVE_CAMERA_RIGHT: pygame.K_d,
 CommandId.MOVE_CAMERA_LEFT: pygame.K_a,
 CommandId.BUILD_BARRACKS: pygame.K_e,
 CommandId.BUILD_DEPOT: pygame.K_r,
 CommandId.BUILD_REFINERY: pygame.K_t,
 CommandId.GENERATE_T1: pygame.K_z,
 CommandId.GENERATE_T2: pygame.K_x,
 CommandId.GENERATE_T3: pygame.K_c,
 CommandId.GENERATE_WORKER: pygame.K_q,
 CommandId.UPGRADE_SOLDIER_DAMAGE: pygame.K_i,
 CommandId.UPGRADE_SOLDIER_ARMOR: pygame.K_o,
 CommandId.UPGRADE_WORKER_MINING: pygame.K_p,
 CommandId.SAVE_GAME: pygame.K_g,
 CommandId.ROTATE: pygame.K_m,
}
