import pygame
import neat
import os

from ground import Ground
from bird import Bird

# Set up global vairables
WIN_SIZE = (600, 800) # The size of the game window
WIN = pygame.display.set_mode (WIN_SIZE) # The pygame window itself
FPS = 30 # Set the FPS the game will run at

if (__name__ == "__main__"):
    from pipe import Pipe


# Get all of the images loaded
NON_BIRD_IMGS = [
    pygame.image.load (os.path.join (os.getcwd (), "imgs", "pipe.png" )), # Pipe
    pygame.image.load (os.path.join (os.getcwd (), "imgs", "base.png" )), # A base section
    pygame.image.load (os.path.join (os.getcwd (), "imgs", "bg.png"   ))  # Background
]

NON_BIRD_IMGS[2] = pygame.transform.scale (
    NON_BIRD_IMGS[2].convert_alpha(), 
    WIN_SIZE
)

BIRD_IMAGES = [pygame.transform.scale2x (pygame.image.load (os.path.join ("imgs", "bird" + str (number) + ".png"))) for number in range (1, 4)]



# ----------------------------
#     Drawing the window
# ----------------------------
#   This will handle all the 
#     drawing on the screen
# ----------------------------
def draw_window (window: pygame.surface.Surface, birds: list, base: Ground, pipes: list) -> None:
    """
    Darwing all items to the screen

    :param window: The window to draw on.
    :param birds: The birds to draw.
    :param base: The base to draw.
    :param pipes: The pipes to draw.
    :return: None.
    """

    # Fill the background with white
    window.fill ( (255, 255, 255) )
    window.blit(NON_BIRD_IMGS[2], (0, 0))

    # Draw the pipes
    for pipe in pipes:
        pipe.draw (window)

    # Draw the base
    base.draw (window)

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
def main () -> None:

    # Make a clock to control FPS
    clock = pygame.time.Clock ()

    # Make the bird list
    birds = []

    # Add the birds to the bird list
    birds.append (Bird ( 
        (WIN_SIZE[0] // 2), 
        (WIN_SIZE[1] // 2), 
        BIRD_IMAGES 
    ))

    # Make the base
    base = Ground (
        NON_BIRD_IMGS[1], 
        0, 
        (WIN_SIZE[1] - NON_BIRD_IMGS[1].get_height ())
    )

    # Make the pipes
    pipes = []
    pipes.append (
        Pipe (
            NON_BIRD_IMGS[0],
            700
        )
    )

    # Make the score
    score = 0
    
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
            
            # If the user pressed a key
            if (event.type == pygame.KEYDOWN):
                # If the user pressed the space bar
                if (event.key == pygame.K_SPACE):
                    # Make the bird jump
                    for bird in birds:
                        bird.jump ()
        

        remove = []
        add_pipe = False
        for pipe in pipes:
            # Move the pipe
            pipe.move ()

            # Check for collisions
            for pos, bird in enumerate (birds):
                # If the bird collides with the pipe
                if (pipe.collide (bird)):
                    # Remove the bird
                    birds.pop (pos)
            
            # If the pipe is off the screen
            if (pipe.x + pipe.PIPE_TOP.get_width () < 0):
                # Remove the pipe
                remove.append (pipe)
            
            # If the pipe has not been marked as
            # passed then do so
            if (not pipe.passed and pipe.x < bird.x):
                pipe.passed = True
                add_pipe = True
        
        # If a pipe was passed
        if (add_pipe):
            score += 1

            # Add a new pipe
            pipes.append (
                Pipe (
                    NON_BIRD_IMGS[0],
                    700
                )
            )
        
        # Remove the pipes that are off the screen
        for pipe in remove:
            pipes.remove (pipe)
        

        # Update the screen
        draw_window (WIN, birds, base, pipes)


# If this is the main file that is being run then
if (__name__ == "__main__"):
    main ()
