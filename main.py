from bird import Bird

import pygame
# import neat
import os

# Set up global vairables
WIN_SIZE = (1000, 500) # The size of the game window
WIN = pygame.display.set_mode(WIN_SIZE) # The pygame window itself
FPS = 60 # Set the FPS the game will run at

# Get all of the images loaded
NON_BIRD_IMGS = [
    pygame.image.load (os.path.join (os.getcwd (), "imgs", "pipe.png" )), # Pipe
    pygame.image.load (os.path.join (os.getcwd (), "imgs", "base.png" )), # A base section
    pygame.image.load (os.path.join (os.getcwd (), "imgs", "bg.png"   ))  # Background
]

BIRD_IMAGES = [pygame.transform.scale2x (pygame.image.load (os.path.join ("imgs", "bird" + str (number) + ".png"))) for number in range (1, 4)]



# ----------------------------
#     Drawing the window
# ----------------------------
#   This will handle all the 
#     drawing on the screen
# ----------------------------
def draw_window (window, birds):
    # Fill the background with white
    window.fill ( (255, 255, 255) )

    # Draw the birds
    for bird in birds:
        bird.draw (window)

    # Update the screen
    pygame.display.update ()



# ------------------------
#     Main function
# ------------------------
#   This will handle all
#        game logic
# ------------------------
def main ():

    # Make a clock to control FPS
    clock = pygame.time.Clock ()

    # Bird list
    birds = []
    birds.append (Bird ( 
        (WIN_SIZE[0] // 2), 
        (WIN_SIZE[1] // 2), 
        BIRD_IMAGES 
    ))
    

    # Main game loop
    run = True
    while (run):

        # Control fps
        clock.tick (FPS)

        # For each event that happens do
        for event in pygame.event.get ():

            # If the X button was pressed exit
            if (event.type == pygame.QUIT):
                run = False
        
        # Update the screen
        draw_window (WIN, birds)


# If this is the main file that is being run then
if (__name__ == "__main__"):
    main ()