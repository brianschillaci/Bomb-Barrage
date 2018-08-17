from typing import List
import pygame
from Settings import WHITE


class Bomb(pygame.sprite.Sprite):
    images: List[None]

    def __init__(self, player, spritesheet):
        """
        Constructor for a Bomb object.
        Initializes the bomb image, time, and background pygame.rect object.
        """
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)

        self.player = player
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
        image3 = pygame.transform.scale(spritesheet.get_image(32, 0, 16, 16), (32, 32))

        # Images for the walking backward animation.
        self.images = [image1, image1, image1, image1, image2, image1, image2, image1, image2, image3, image2, image3, image2, image3, image2, image3, image2, image3]

        for frame in self.images:
            frame.set_colorkey(WHITE)


def drop_bomb(player, bombspritesheet, otherSprites, bomb_set):
    """
    This function will drop a bomb sprite under a player. It only allows a certain
    amount of bomb drops in a certain time frame. The bombs will always be placed in
    the center of a tile. This is so that the explosions from the bomb stay in the correct rows
    and columns.
    """
    player.placingBomb = True
    now = pygame.time.get_ticks()
    # Drop a bomb only if sufficient amount of time has passed since the last bomb was dropped
    if now - player.lastBombPlacementTime > 2000 and player.placingBomb:
        # Update the player's last bomb drop time
        player.lastBombPlacementTime = now
        # Create a new bomb object and add to the bomb set and sprites list
        bomb = Bomb(player, bombspritesheet)
        otherSprites.add(bomb)
        bomb_set.add(bomb)
        # Update the location of the bomb to the (x,y) of where the player dropped it
        bomb.rect.x = (player.rect.centerx // 32) * 32
        bomb.rect.y = ((player.rect.bottom - 5) // 32) * 32
