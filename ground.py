import pygame


class Ground:

    VElOCITY = 5

    def __init__ (self, image: pygame.Surface, x: int, y: int):
        """
        :parm image: The image to use for the ground.
        :param x: The x position of the ground.
        :param y: The y position of the ground.
        """
        self.image = pygame.transform.scale2x (image).convert_alpha ()
        self.width = self.image.get_width ()

        self.x = x
        self.y = y
        self.x2 = self.width

    
    def move (self):
        """
        Used to move the ground at the same speed as the pipes.
        This is to simulate motion / flying.
        """
        self.x -= self.VELOCITY
        self.x2 -= self.VELOCITY

        # If the box is off screen then
        if (self.x + self.width < 0):
            self.x = self.x2 + self.width
        
        # If the box is off screen then
        if (self.x2 + self.width < 0):
            self.x2 = self.x + self.width


    def draw (self, window: pygame.Surface):
        """
        :parm window: The window to draw on.
        """

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