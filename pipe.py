from bird import Bird

import random
import pygame
import main

class Pipe:

    VELOCITY = 5
    GAP = 200

    def __init__ (self, image, x):
        self.x = x
        self.height = 0

        self.image = pygame.transform.scale2x(image).convert_alpha()

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(self.image, False, True)
        self.PIPE_BOTTOM = self.image

        self.passed = False

        # Set the height of the pipes
        # right awway
        self.set_height ()


    def set_height (self):
        
        # Get a random height for 
        # the pipes space to be
        self.height = random.randrange (50, main.WIN_SIZE[1] - 50)

        # Top pipe y position
        self.top = self.height - self.PIPE_TOP.get_height ()

        # Bottom pipe y position
        self.bottom = self.height + self.GAP
    

    def move (self):
        self.x -= self.VELOCITY


    def draw (self, window: pygame.Surface):
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
    

    def collide (self, bird: Bird, window: pygame.Surface):
        pass
