import pygame

# Make the class for the bird objects
class Bird:
    def __init__ (self, x: int, y: int, images: list) -> object:
        """
        This will initalize the bird object.

        :param x: The x position of the bird.
        :param y: The y position of the bird.
        :param images: A list of images to use for the bird.
        """

        # Set the inital position of the bird
        self.x = x
        self.y = y

        # Set the images for the bird
        self.images = images
        self.image = images[0]
    
    def jump (self):
        pass

    def draw (self, window: pygame.surface.Surface) -> bool:
        """
        :param window: The surface to draw the bird on.
        :return: True if the bird was drawn, False if not.
        """

        # Try statment to make sure the bird was drawn
        try:
            # Draw the bird to the screen
            window.blit (
                self.image, 
                (self.x, self.y)
            )

            return True
        except:
            return False

    def get_mask (self):
        """
        :return: A mask for the bird. Used for collision detection.
        """
        
        # Used for collision detection
        return pygame.mask.from_surface (self.image)
        