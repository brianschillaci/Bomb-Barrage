import pygame


class Wall(pygame.sprite.Sprite):

    def __init__(self, color, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.color.Color(color))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class UnbreakableRock(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class BreakableRock(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y