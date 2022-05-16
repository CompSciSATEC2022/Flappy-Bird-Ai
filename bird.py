import pygame

# Make the class for the bird objects
class Bird:

    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

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

        # Set other vairables needed
        self.vel = 0
        self.tilt = 0
        self.img_count = 0
        self.tick_count = 0
        self.height = self.y
        
    
    def jump (self) -> None:
        """
        Make the bird jump.
        :return: None.
        """

        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y


    def move (self) -> None:
        """
        Make the bird move.
        :return: None.
        """

        self.tick_count += 1

        # Gravity
        #     _ 
        #   /   \
        #  /     \
        # 0       X
        displacement = self.vel * (self.tick_count) + 0.5 * (3) * (self.tick_count) ** 2

        # Terminal velocity
        if displacement >= 16:
            displacement = (displacement / abs (displacement)) * 16
        
        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement # (displacement / (4/3))
        
        if self.y < 0:
            self.y = 0

        # Tilt the bird up
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        
        # Tilt the bird down
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL


    def draw (self, window: pygame.surface.Surface) -> bool:
        """
        :param window: The surface to draw the bird on.
        :return: True if the bird was drawn, False if not.
        """

        self.img_count += 1

        # Deals with the animation of the bird
        # Loops through the images that were given
        if self.img_count <= self.ANIMATION_TIME:
            self.image = self.images[0]
        
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.image = self.images[1]
        
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.image = self.images[2]

        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.image = self.images[1]

        elif self.img_count <= (self.ANIMATION_TIME * 4) + 1:
            self.image = self.images[0]
            self.img_count = 0

        
        # When the bird is nose diving it should not
        # be able to flap
        if self.tilt <= -80:
            self.image = self.images[1]
            self.img_count = self.ANIMATION_TIME * 2
        

        # Tilt the bird
        rotated_image = pygame.transform.rotate (self.image, self.tilt)
        new_rect = rotated_image.get_rect (
            center=self.image.get_rect ( 
                center=(self.x, self.y)
            ).center
        )

        # Draw the rotated bird
        window.blit (rotated_image, new_rect.topleft)


    def get_mask (self):
        """
        :return: A mask for the bird. Used for collision detection.
        """
        
        # Used for collision detection
        return pygame.mask.from_surface (self.image)
        