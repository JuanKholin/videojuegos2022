import pygame
from src.Entities import Entity

pygame.init()

white = (255, 255, 255)
BLACK = (0,0,0)

# assigning values to X and Y variable
X = 640
Y = 640

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))

pygame.display.set_caption("Zerling")
spritesheet = pygame.image.load("./sprites/zergling.bmp")
spritesheet.set_colorkey(BLACK)
images = Entity.Entity.divideSpritesheetByRows(spritesheet, 128)
image = images[0]

# infinite loop
while True :

	# completely fill the surface object
	# with white colour
	display_surface.fill(white)

	# copying the image surface object
	# to the display surface object at
	# (0, 0) coordinate.
	display_surface.blit(image, (0, 0))

	# iterate over the list of Event objects
	# that was returned by pygame.event.get() method.
	for event in pygame.event.get() :

		# if event object type is QUIT
		# then quitting the pygame
		# and program both.
		if event.type == pygame.QUIT :

			# deactivates the pygame library
			pygame.quit()

			# quit the program.
			quit()

		# Draws the surface object to the screen.
		pygame.display.update()
			
