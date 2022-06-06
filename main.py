import pygame
import pickle
import neat
import os

from ground import Ground
from bird import Bird

# Set up global vairables
WIN_SIZE = (600, 800) # The size of the game window
WIN = pygame.display.set_mode (WIN_SIZE) # The pygame window itself
FPS = 30 # Set the FPS the game will run at
gen = 0

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
    
    for bird in birds:
        for pipe in pipes:
            if pipe.passed == False:
                pygame.draw.line (
                    window, 
                    (255, 0, 0),
                    (bird.x, bird.y),
                    (pipe.x + (pipe.PIPE_TOP.get_width () // 2), pipe.height),
                    width=3
                )
                pygame.draw.line (
                    window, 
                    (255, 0, 0),
                    (bird.x, bird.y),
                    (pipe.x + (pipe.PIPE_TOP.get_width () // 2), pipe.bottom),
                    width=3
                )
                break

    # Update the screen
    pygame.display.update ()



# ------------------------
#     Main function
# ------------------------
#   This will handle all
#        game logic
# ------------------------
def main (genomes_in, config) -> None:
    global gen
    gen += 1

    # Make a clock to control FPS
    clock = pygame.time.Clock ()

    # Make the bird list
    # Add the birds to the bird list
    birds = []
    nets = []
    genomes = []
    for _, genome in genomes_in:
        genome.fitness = 0
        
        net = neat.nn.FeedForwardNetwork.create (genome, config)
        nets.append (net)

        birds.append (Bird (230, 350, BIRD_IMAGES))
        genomes.append (genome)
    
        

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
    while (run and len (birds) != 0):
        if len (birds) == 0:
            print ("End")

        # Control fps
        clock.tick (FPS)

        # For each event that happens do
        for event in pygame.event.get ():

            # If the X button was pressed exit
            if (event.type == pygame.QUIT):
                run = False
                pygame.quit ()
                quit ()
            
            """
            # If the user pressed a key
            if (event.type == pygame.KEYDOWN):
                # If the user pressed the space bar
                if (event.key == pygame.K_SPACE):
                    # Make the bird jump
                    for bird in birds:
                        bird.jump ()
            """
        
        pipe_ind = 0
        if len (birds) > 0:
            if len (pipes) > 1:
                if birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width ():
                    pipe_ind = 1
        
        for x, bird in enumerate (birds):
            genomes[x].fitness += 0.1
            bird.move ()

            output = nets[birds.index(bird)].activate (
                (
                    bird.y,
                    abs (bird.y - pipes[pipe_ind].height),
                    abs (bird.y - pipes[pipe_ind].bottom)
                )
            )

            if (output[0] > .5):
                bird.jump ()
        
        base.move ()


        remove = []
        add_pipe = False
        for pipe in pipes:
            # Check for collisions
            if len (birds) > 0:
                bird = birds[0]
                for bird in birds:
                    # If the bird collides with the pipe
                    if (pipe.collide (bird)):
                        genomes[birds.index(bird)].fitness -= 1
                        nets.pop (birds.index(bird))
                        genomes.pop (birds.index(bird))
                        birds.pop (birds.index(bird))

                    bird = bird


            # If the pipe is off the screen
            if (pipe.x + pipe.PIPE_TOP.get_width () < 0):
                # Remove the pipe
                remove.append (pipe)
            

            # If the pipe has not been marked as
            # passed then do so
            if len (birds) > 0:
                if (not pipe.passed and pipe.x < bird.x):
                    pipe.passed = True
                    add_pipe = True

            # Move the pipe
            pipe.move ()

        
        # If a pipe was passed
        if (add_pipe):
            score += 1

            for genome in genomes:
                genome.fitness += 5


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


        # Move the bird
        remove = []
        for bird in birds:
            if (bird.y + bird.image.get_height() >= (WIN_SIZE[1] - NON_BIRD_IMGS[1].get_height ())):
                remove.append (bird)

            elif bird.y < -50:
                nets.pop(birds.index(bird))
                genomes.pop(birds.index(bird))
                birds.pop(birds.index(bird))
        
        for bird in remove:
            nets.pop(birds.index(bird))
            genomes.pop(birds.index(bird))
            birds.pop(birds.index(bird))


        # Update the screen
        draw_window (WIN, birds, base, pipes)



def run ():
    config_file = os.path.join (os.getcwd (), "config-feedforward.txt")
    config = neat.config.Config (
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )

    population = neat.Population (config)

    population.add_reporter (neat.StdOutReporter (True))
    stats = neat.StatisticsReporter ()
    population.add_reporter (stats)

    # Run for 50 gens
    best = population.run (main, 25)

    print (f"\nBest ai: \n{best}")

    pickle.dump (best, open ("best.pickle", "wb"))


def play_old ():
    config_file = os.path.join (os.getcwd (), "config-feedforward.txt")
    config = neat.config.Config (
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation, 
        config_file
    )
    best = pickle.load (open ("best.pickle", "rb"))
    
    genomes = [(1, best)]

    main (genomes, config)
    


# If this is the main file that is being run then
if (__name__ == "__main__"):
    if (False):
        play_old ()
    else:
        run ()
