from typing import List

import pygame

from constants import PLAYER_ANIMATION_SPEED, WHITE, PLAYER_MOVEMENT_DISTANCE, PLAYER_EXPLOSION_TIME
from sprites.bombs import Bomb
from sprites.hitboxes import PlayerHitbox
from util import animation_util, collision_util


class Player(pygame.sprite.Sprite):
    """
    This is the class for a player object. There should be a max of 4 players in a game.
    """
    # Lists of frames for the different animations for the player object
    standing_frames: List[None]
    walk_frames_r: List[None]
    walk_frames_l: List[None]
    walk_frames_up: List[None]
    walk_frames_down: List[None]

    def __init__(self, start_x, start_y, player_sprite_sheet):
        """
        Constructor for a player object.
        """
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)

        # Amount of times the player can get hit before dying
        self.lives = 1

        # Last direction the player moved
        self.lastMovementDirection = None

        # Whether the player is plaacing a bomb or not
        self.placingBomb = False

        # Group of bombs that were just dropped - used for bomb collision detection
        self.active_bombs = pygame.sprite.Group()

        # Time for an explosion animation to occur after hitting the player
        # Needed so that the player's lives are only subtracted after the explosion animation is done.
        self.explosionTime = PLAYER_EXPLOSION_TIME

        # Set to true if this player was hit by an explosion and
        # is waiting for the explosion to be done before subtracting from its number of lives
        self.isInExplosionAnimation = False

        # Time that the last bomb was placed, this allows us to control the amount of time in between bomb placements.
        self.lastBombPlacementTime = -2000

        # Index of the current sprite/frame that the player is displayed as
        self.current_frame = 0

        # Time since last frame update - this allows us to control how fast the animations move
        self.last_update = 0

        # Size of bomb to start, bomberman has no powerups initially.
        self.explosion_size = 1

        self.spritesheet = player_sprite_sheet

        # Calling load_images() in order to create all of the arrays of sprite images for each set of animations
        self.load_player_images()

        # Setting the initial image of the player when it is first created
        self.image = self.standing_frames[0]

        # Setting the rect object for this player object - every sprite has a hidden rectangle behind its image
        # This rectangle allows for collision detection, movement, and more
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        # The hitbox sprite for this player. This sprite will need to be updated as the player moves. This is needed for
        # some collision detection since some collisions need a smaller rectangle for the collision.
        self.hitbox = PlayerHitbox(self, self.rect.width / 2, self.rect.height / 5)

    def load_player_images(self):
        """
        This function will initialize all of the animation arrays for a player object.
        These arrays will be looped through/used in order to emulate 2d animations for the player object based on
        different user inputs.
        :return: No return.
        """
        # Images for all the different standing positions.
        self.standing_frames = [pygame.transform.scale(self.spritesheet.get_image(0, 69, 15, 23), (30, 46)),
                                pygame.transform.scale(self.spritesheet.get_image(0, 37, 16, 23), (32, 46)),
                                pygame.transform.scale(self.spritesheet.get_image(0, 101, 16, 23), (32, 46)),
                                pygame.transform.scale(self.spritesheet.get_image(0, 7, 15, 21), (30, 42))]
        for frame in self.standing_frames:
            frame.set_colorkey(WHITE)

        # Images for the walking right animation.
        self.walk_frames_r = [pygame.transform.scale(self.spritesheet.get_image(0, 37, 16, 23), (32, 46)),
                              pygame.transform.scale(self.spritesheet.get_image(16, 38, 15, 22), (30, 44)),
                              pygame.transform.scale(self.spritesheet.get_image(32, 39, 16, 21), (32, 42))]
        for frame in self.walk_frames_r:
            frame.set_colorkey(WHITE)

        # Images for the walking left animation.
        self.walk_frames_l = [pygame.transform.scale(self.spritesheet.get_image(0, 101, 16, 23), (32, 46)),
                              pygame.transform.scale(self.spritesheet.get_image(16, 103, 16, 21), (32, 42)),
                              pygame.transform.scale(self.spritesheet.get_image(33, 102, 15, 22), (30, 44))]
        for frame in self.walk_frames_l:
            frame.set_colorkey(WHITE)

        # Images for the walking forward animation.
        self.walk_frames_up = [pygame.transform.scale(self.spritesheet.get_image(0, 7, 15, 21), (30, 42)),
                               pygame.transform.scale(self.spritesheet.get_image(16, 7, 15, 23), (30, 46)),
                               pygame.transform.scale(self.spritesheet.get_image(32, 7, 15, 23), (30, 46))]
        for frame in self.walk_frames_up:
            frame.set_colorkey(WHITE)

        # Images for the walking backward animation.
        self.walk_frames_down = [pygame.transform.scale(self.spritesheet.get_image(0, 69, 15, 23), (30, 46)),
                                 pygame.transform.scale(self.spritesheet.get_image(16, 69, 15, 23), (30, 46)),
                                 pygame.transform.scale(self.spritesheet.get_image(32, 69, 15, 23), (30, 46))]
        for frame in self.walk_frames_down:
            frame.set_colorkey(WHITE)

    def animate_player(self, movement_direction):
        """
        This function will animate the movement/non-movement of a player object. If the player is not moving,
        it will use that last movement direction to pick which standing frame to use.
        """
        now = pygame.time.get_ticks()
        # Display the current frame for the walking animation.
        if movement_direction is not None:
            self.lastMovementDirection = movement_direction
            # Only update the frame and move the player if a certain amount of time has passed.
            # This will allow us to control the speed of the animation.
            # Change ANIMATION_SPEED in constants.py in order to see the effect.
            if movement_direction is pygame.K_RIGHT:
                animation_util.animate(self, PLAYER_ANIMATION_SPEED, self.walk_frames_r)
            elif movement_direction is pygame.K_LEFT:
                animation_util.animate(self, PLAYER_ANIMATION_SPEED, self.walk_frames_l)
            elif movement_direction is pygame.K_UP:
                animation_util.animate(self, PLAYER_ANIMATION_SPEED, self.walk_frames_up)
            elif movement_direction is pygame.K_DOWN:
                animation_util.animate(self, PLAYER_ANIMATION_SPEED, self.walk_frames_down)
        # Display the frame for if the player is standing still
        else:
            self.last_update = now
            if self.lastMovementDirection is pygame.K_RIGHT:
                self.current_frame = 1
            elif self.lastMovementDirection is pygame.K_LEFT:
                self.current_frame = 2
            elif self.lastMovementDirection is pygame.K_UP:
                self.current_frame = 3
            elif self.lastMovementDirection is pygame.K_DOWN:
                self.current_frame = 0
            self.image = self.standing_frames[self.current_frame]

    def handle_input(self, walls, collision_sprite_groups, bomb_sprite_sheet, all_bombs, active_bomb_set, keys,
                     all_players):
        # Checking for collisions with the walls of the game
        collision_1 = pygame.sprite.collide_rect(walls[0], self)
        collision_2 = pygame.sprite.collide_rect(walls[1], self)
        collision_3 = pygame.sprite.collide_rect(walls[2], self)
        collision_4 = pygame.sprite.collide_rect(walls[3], self)

        # Handle the input keys for this player
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if collision_2 != 0:
                self.animate_player(pygame.K_LEFT)
            else:
                self.rect.x -= PLAYER_MOVEMENT_DISTANCE
                collision_util.fix_player_movement_collision(self, collision_sprite_groups, pygame.K_LEFT)
                collision_util.fix_player_bomb_collision(self, all_bombs, pygame.K_LEFT)
                self.animate_player(pygame.K_LEFT)
            if keys[pygame.K_SPACE]:
                self.drop_bomb(bomb_sprite_sheet, all_bombs, active_bomb_set, all_players)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if collision_4 != 0:
                self.animate_player(pygame.K_RIGHT)
            else:
                self.rect.x += PLAYER_MOVEMENT_DISTANCE
                collision_util.fix_player_movement_collision(self, collision_sprite_groups, pygame.K_RIGHT)
                collision_util.fix_player_bomb_collision(self, all_bombs, pygame.K_RIGHT)
                self.animate_player(pygame.K_RIGHT)
            if keys[pygame.K_SPACE]:
                self.drop_bomb(bomb_sprite_sheet, all_bombs, active_bomb_set, all_players)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if collision_1 != 0:
                self.animate_player(pygame.K_UP)
            else:
                self.rect.y -= PLAYER_MOVEMENT_DISTANCE
                collision_util.fix_player_movement_collision(self, collision_sprite_groups, pygame.K_UP)
                collision_util.fix_player_bomb_collision(self, all_bombs, pygame.K_UP)
                self.animate_player(pygame.K_UP)
            if keys[pygame.K_SPACE]:
                self.drop_bomb(bomb_sprite_sheet, all_bombs, active_bomb_set, all_players)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if collision_3 != 0:
                self.animate_player(pygame.K_DOWN)
            else:
                self.rect.y += PLAYER_MOVEMENT_DISTANCE
                collision_util.fix_player_movement_collision(self, collision_sprite_groups, pygame.K_DOWN)
                collision_util.fix_player_bomb_collision(self, all_bombs, pygame.K_DOWN)
                self.animate_player(pygame.K_DOWN)
            if keys[pygame.K_SPACE]:
                self.drop_bomb(bomb_sprite_sheet, all_bombs, active_bomb_set, all_players)
        elif keys[pygame.K_SPACE]:
            self.drop_bomb(bomb_sprite_sheet, all_bombs, active_bomb_set, all_players)
        else:
            self.placingBomb = False
            self.animate_player(None)

    def drop_bomb(self, bombspritesheet, all_bombs, all_bombs_set, all_players):
        """
        This function will drop a bomb sprite under a player. It only allows a certain
        amount of bomb drops in a certain time frame. The bombs will always be placed in
        the center of a tile. This is so that the explosions from the bomb stay in the correct rows
        and columns.
        """
        self.placingBomb = True
        now = pygame.time.get_ticks()
        # Drop a bomb only if sufficient amount of time has passed since the last bomb was dropped
        if now - self.lastBombPlacementTime > 2000 and self.placingBomb:
            # Update the player's last bomb drop time
            self.lastBombPlacementTime = now
            # Create a new bomb object and add to the all bombs set, all bombs sprite group, and self bomb group
            bomb = Bomb(self, bombspritesheet, all_players)
            all_bombs.add(bomb)
            all_bombs_set.add(bomb)
            self.active_bombs.add(bomb)
            # Update the location of the bomb to the (x,y) of where the player dropped it
            bomb.rect.x = (self.rect.centerx // 32) * 32
            bomb.rect.y = ((self.rect.bottom - 5) // 32) * 32

    def is_alive(self):
        """
        Checks if a player is still alive, meaning that the player has more than 0 lives.
        :return: lives > 0
        """
        return self.lives > 0

    def is_dead(self):
        """
        Checks if a player is still dead, meaning that the player has less or equal to 0 lives.
        :return: lives <= 0
        """
        return self.lives <= 0
