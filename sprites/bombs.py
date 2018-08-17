from typing import List
import pygame
from contants import WHITE


class Bomb(pygame.sprite.Sprite):
    images: List[None]

    def __init__(self, player, spritesheet):
        """
        Constructor for a Bomb object.
        Initializes the bomb image, time, and background pygame.rect object.
        """
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)

        # Player that dropped this bomb
        self.player = player

        # Initially set to the current player, once the player moves off this bomb, set to None
        self.playerAllowedToCollide = self.player

        # Load images and pre-setup for animation
        self.load_bomb_images(spritesheet)
        self.image = self.images[0]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.last_update = 0
        self.current_frame = 0

    def load_bomb_images(self, spritesheet):
        """
        This function will initialize animation image array for a bomb object.
        """
        image1 = pygame.transform.scale(spritesheet.get_image(0, 0, 16, 16), (32, 32))
        image2 = pygame.transform.scale(spritesheet.get_image(16, 0, 16, 16), (32, 32))

        # Images for the bomb animation.
        self.images = [image1, image1, image1, image1, image2, image2, image1, image1, image2,
                       image2, image1, image1, image2, image1, image2, image1, image2, image1]

        for frame in self.images:
            frame.set_colorkey(WHITE)
