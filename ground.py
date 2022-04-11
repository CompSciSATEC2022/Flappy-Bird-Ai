import pygame


class Ground:

    VElOCITY = 5

    def __init__ (self, image: pygame.Surface, x: int, y: int):
        self.image = pygame.transform.scale2x (image).convert_alpha ()
        self.width = self.image.get_width ()

        self.x = x
        self.y = y
        self.x2 = self.width

    
    def move (self):
        self.x -= self.VELOCITY
        self.x2 -= self.VELOCITY

        # If the box is off screen then
        if (self.x + self.width < 0):
            self.x = self.x2 + self.width
        
        # If the box is off screen then
        if (self.x2 + self.width < 0):
            self.x2 = self.x + self.width


    def draw (self, window: pygame.Surface):

        # Draw the ground twice 
        # next to each other
        window.blit (
            self.image, 
            (self.x, self.y)
        )

        window.blit (
            self.image, 
            (self.x2, self.y)
        )