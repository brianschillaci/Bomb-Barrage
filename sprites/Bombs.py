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
        :param time: Input time to subtract from the time remaining on this bomb object.
        :return: True - if bomb is ready to explode. False - if the bomb isn't ready to explode yet.
        """
        self.time -= time
        # Animate the explosion if the time is right
        if self.time <= BOMB_DETONATION_TIME - 1110:
            return True
        elif self.time <= BOMB_DETONATION_TIME - 1060:
            set_bomb_image(self, 32, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 1010:
            set_bomb_image(self, 16, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 960:
            set_bomb_image(self, 32, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 910:
            set_bomb_image(self, 16, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 860:
            set_bomb_image(self, 32, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 810:
            set_bomb_image(self, 16, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 760:
            set_bomb_image(self, 32, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 700:
            set_bomb_image(self, 16, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 600:
            set_bomb_image(self, 32, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 500:
            set_bomb_image(self, 0, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 400:
            set_bomb_image(self, 16, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 300:
            set_bomb_image(self, 0, 0, 16, 16, 32, spritesheet)
            return False
        elif self.time <= BOMB_DETONATION_TIME - 200:
            set_bomb_image(self, 16, 0, 16, 16, 32, spritesheet)
            return False


def set_bomb_image(self, x, y, l, w, scaleAmount, spritesheet):
    self.image = pygame.transform.scale(spritesheet.get_image(x, y, l, w), (scaleAmount, scaleAmount))
    self.image.set_colorkey(WHITE)


def drop_bomb(player, bombspritesheet, otherSprites, bomb_set):
    now = pygame.time.get_ticks()
    # Drop a bomb only if sufficient amount of time has passed since the last bomb was dropped
    if now - player.lastBombPlacementTime > 2000 and player.place_bomb():
        # Update the player's last bomb drop time
        player.lastBombPlacementTime = now
        # Create a new bomb object and add to the bomb set and sprites list
        bomb = Bomb(player, bombspritesheet)
        otherSprites.add(bomb)
        bomb_set.add(bomb)
        # Update the location of the bomb to the (x,y) of where the player dropped it
        bomb.rect.x = (player.rect.centerx // 32) * 32
        bomb.rect.y = ((player.rect.bottom - 5) // 32) * 32
