from typing import List

import pygame

from constants import WHITE


class Bomb(pygame.sprite.Sprite):
    images: List[None]

    def __init__(self, player, spritesheet, all_players):
        """
        Constructor for a Bomb object.
        Initializes the bomb image, time, and background pygame.rect object.
        """
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)

        # Player that dropped this bomb
        self.player = player

        # Bombs are allowed to collide with everyone initially - players get removed from this set once they step off the bomb
        self.players_allowed_to_collide = None
        player_set = set()
        for player in all_players:
            player_set.add(player)
        self.players_allowed_to_collide = player_set

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


def update_active_bombs(players, all_bombs):
    for bomb in all_bombs:
        for player in players:
            player.hitbox.update_rect(player, player.rect.width, player.rect.height / 4)
            collision = pygame.sprite.collide_rect(player.hitbox, bomb)
            if collision == 0 and bomb.players_allowed_to_collide.__contains__(player):
                bomb.players_allowed_to_collide.remove(player)
