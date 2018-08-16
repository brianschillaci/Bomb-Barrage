from typing import List
import pygame
from Settings import WHITE, BOMB_DETONATION_TIME


class Bomb(pygame.sprite.Sprite):
    bomb_place_frames: List[None]

    def __init__(self, player, spritesheet):
        """
        Constructor for a Bomb object.
        Initializes the bomb image, time, and background pygame.rect object.
        """
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)

        # Time until the bomb explodes - in seconds
        self.time = BOMB_DETONATION_TIME
        self.player = player
        self.image = pygame.transform.scale(spritesheet.get_image(0, 0, 16, 16), (32, 32))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def animate(self, time, spritesheet):
        """
        This function will update the time variable for a specific bomb. If the time of this bomb has expired,
        it will 'explode'. This explosion means removing this bomb sprite, and replacing it by the proper explosion
        sprites. These explosion sprites will then need to do collision checks with all the other sprites, like
        players and rocks, and do the appropriate function for each case of collision.
        :param spritesheet: The image that has all the smaller bomb images.
        :param time: Input time to subtract from the time remaining on this bomb object.
        :return: True - if bomb is ready to explode. False - if the bomb isn't ready to explode yet.
        """
        self.time -= time
        # Animate the explosion if the time is right
        if self.time <= BOMB_DETONATION_TIME - 1110:
            return True
        elif self.time <= BOMB_DETONATION_TIME - 1060:
            self.set_bomb_image(32, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 1010:
            self.set_bomb_image(16, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 960:
            self.set_bomb_image(32, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 910:
            self.set_bomb_image(16, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 860:
            self.set_bomb_image(32, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 810:
            self.set_bomb_image(16, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 760:
            self.set_bomb_image(32, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 700:
            self.set_bomb_image(16, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 600:
            self.set_bomb_image(32, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 500:
            self.set_bomb_image(0, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 400:
            self.set_bomb_image(16, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 300:
            self.set_bomb_image(0, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 200:
            self.set_bomb_image(16, 0, 16, 16, 32, spritesheet)
            return False

    def set_bomb_image(self, x, y, l, w, scaleAmount, spritesheet):
        """
        This function will set the image of the bomb for the particular stage of the bomb explosion animation.
        """
        self.image = pygame.transform.scale(spritesheet.get_image(x, y, l, w), (scaleAmount, scaleAmount))
        self.image.set_colorkey(WHITE)


def drop_bomb(player, bombspritesheet, otherSprites, bomb_set):
    """
    This function will drop a bomb sprite under a player. It only allows a certain
    amount of bomb drops in a certaain time frame. The bombs will always be placed in
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
