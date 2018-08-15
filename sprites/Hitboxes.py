import pygame


class PlayerHitbox(pygame.sprite.Sprite):
    def __init__(self, player, width, height):
        """
        Constructor for a hitbox sprite.
        """
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)

        self.player = player

        # Creating rect object for the hitbox
        self.rect = pygame.rect.Rect((0, 0), (width, height))

        self.rect.midbottom = player.rect.midbottom

        self.explosionTime = 90

    def update_rect(self, parent, width, height):
        self.player = parent
        self.rect = pygame.rect.Rect((0, 0), (width, height))
        self.rect.midbottom = parent.rect.midbottom
