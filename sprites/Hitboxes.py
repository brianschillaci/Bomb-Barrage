import pygame


class PlayerHitbox(pygame.sprite.Sprite):
    """
    This class is used as a hit box for a player.
    It is a sprite that is within the rectangle object of a player,
    but has a smaller rectangle at a specific location on the player.
    This location for this hitbox is at the bottom middle of the player's rectangle object.
    """
    def __init__(self, player, width, height):
        """
        Constructor for a hitbox sprite.
        """
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)

        self.player = player

        # Creating rect object for the hitbox
        self.rect = pygame.rect.Rect((0, 0), (width, height))

        # Positioning the hitbox in relation to the player
        self.rect.midbottom = player.rect.midbottom

    def update_rect(self, player, width, height):
        """
        Updates this hitbox's rect object.
        :param player: The player sprite associated with this hitbox sprite.
        :param width: The width of the hitbox's rect
        :param height: The height of the hitbox's rect
        :return:
        """
        self.player = player
        self.rect = pygame.rect.Rect((0, 0), (width, height))
        self.rect.midbottom = player.rect.midbottom
