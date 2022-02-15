import pygame
from pygame.locals import *
import sys

SCREEN_WIDTH = 620
SCREEN_HEIGHT = 480

IMAGEN_WIDTH = 120
IMAGEN_HEiGHT = 100

def main():
    pygame.init()

    dvd_move_x = 1
    dvd_move_y = 1

    dvd_pos_x = 300
    dvd_pos_y = 200     
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("dvd")

    # cargamos el fondo y una imagen (se crea objetos "Surface")
    # fondo = pygame.image.load("fondo.jpg").convert()
    # reajustar tamaño del imagen
    dvd = pygame.transform.scale(pygame.image.load("dvd.png").convert_alpha(), (IMAGEN_WIDTH, IMAGEN_HEiGHT))
    # Indicamos la posicion de las "Surface" sobre la ventana
    # screen.blit(fondo, (0, 0))
    screen.blit(dvd, (dvd_pos_x, dvd_pos_y))
    # se muestran lo cambios en pantalla
    pygame.display.flip()

    # el bucle principal del juego
    while True:
        # calcular el proximo movimiento
        dvd_pos_x = dvd_pos_x + dvd_move_x
        dvd_pos_y = dvd_pos_y + dvd_move_y
        if (dvd_pos_x < 1 or dvd_pos_x > screen.get_width() - IMAGEN_WIDTH -1):
            dvd_move_x = -dvd_move_x
        if (dvd_pos_y < 1 or dvd_pos_y > screen.get_height() - IMAGEN_HEiGHT -1):
            dvd_move_y = -dvd_move_y
         
        # clear pantalla y nueva posiscion
        screen.fill((0,0,0))
        screen.blit(dvd, (dvd_pos_x, dvd_pos_y))
        # se muestran lo cambios en pantalla
        pygame.display.flip()
        # añadir delay
        pygame.time.delay(5)
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == "__main__":
    main()
