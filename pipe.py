from main import WIN_SIZE, NON_BIRD_IMGS
from bird import Bird

import random
import pygame


class Pipe:

    VELOCITY = 5
    GAP = 200

    def __init__ (self, image: pygame.Surface, x: int):
        """
        :parm image: The image to use for the pipe.
        :param x: The x position of the pipe.
        :return: None.
        """

        self.x = x
        self.height = 0

        self.image = pygame.transform.scale2x (image).convert_alpha ()

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip (self.image, False, True)
        self.PIPE_BOTTOM = self.image

        self.passed = False

        # Set the height of the pipes
        # right awway
        self.set_height ()


    def set_height (self):
        """
        Set the height of the pipes.
        """
        
        # Get a random height for 
        # the pipes space to be
        self.height = random.randrange (
            50, 
            (WIN_SIZE[1] - NON_BIRD_IMGS[1].get_height ()) - (self.GAP + 50)
        )

        # Top pipe y position
        self.top = self.height - self.PIPE_TOP.get_height ()

        # Bottom pipe y position
        self.bottom = self.height + self.GAP
    

    def move (self):
        """
        Move the pipes by the velocity.
        """
        self.x -= self.VELOCITY


    def draw (self, window: pygame.Surface):
        """
        :parm window: The window to draw on.
        """
        # Draw the top pipe
        window.blit (
            self.PIPE_TOP, 
            (self.x, self.top)
        )

        # Draw the bottom pipe
        window.blit (
            self.PIPE_BOTTOM, 
            (self.x, self.bottom)
        )
    

    def collide (self, bird: Bird):
        """
        :parm bird: The bird to check for collision against.
        :return: True if the bird collides with the pipe.
        """

        # Get the mask of the bird
        bird_mask = bird.get_mask ()

        # Get the mask of the top and bottom pipe
        top_mask = pygame.mask.from_surface (self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface (self.PIPE_BOTTOM)

        #                          (X, Y)
        top_offset = (self.x - bird.x, self.top - round (bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round (bird.y))

        # Check for collision
        top_point = bird_mask.overlap (top_mask, top_offset)
        bottom_point = bird_mask.overlap (bottom_mask, bottom_offset)

        # If there is a collision
        if (top_point or bottom_point):
            return True
        
        return False
