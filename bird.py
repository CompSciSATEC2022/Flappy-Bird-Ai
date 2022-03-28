import pygame

class Bird:
    def __init__ (self, x: int, y: int, images: list):
        self.x = x
        self.y = y
        self.images = images
        self.image = images[0]
    
    def jump (self):
        pass

    def draw (self, window: pygame.surface.Surface):
        
        window.blit (self.image, (self.x, self.y))

    def get_mask (self):
        # Used for collision detection
        return pygame.mask.from_surface (self.image)
        