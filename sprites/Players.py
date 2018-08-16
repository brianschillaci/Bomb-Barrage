from os import path
from typing import List
import pygame
from Settings import SPRITESHEET, RESOURCE_FOLDER, ANIMATION_SPEED, WHITE
from sprites.Hitboxes import PlayerHitbox
from sprites.Spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
    """
    This is the class for a player object. There should be a max of 4 players in a game.
    """
    # Lists of frames for the different animations for the player object
    standing_frames: List[None]
    walk_frames_r: List[None]
    walk_frames_l: List[None]
    walk_frames_forward: List[None]
    walk_frames_back: List[None]

    def __init__(self, startX, startY):
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

        # Time for an explosion animation to occur after hitting the player
        # Needed so that the player's lives are only subtracted after the explosion animation is done.
        self.explosionTime = 90

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

        # Getting the spritesheet file for this player - res is the folder it is in, SPRITESHEET is the filename
        self.dir = path.dirname(__file__)
        parent = path.join(self.dir, path.pardir)
        res = path.join(parent, RESOURCE_FOLDER)
        img_dir = path.join(res, SPRITESHEET)
        self.spritesheet = Spritesheet(img_dir)

        # Calling load_images() in order to create all of the arrays of sprite images for each set of animations
        self.load_player_images()

        # Setting the initial image of the player when it is first created
        self.image = self.standing_frames[0]

        # Setting the rect object for this player object - every sprite has a hidden rectangle behind its image
        # This rectangle allows for collision detection, movement, and more
        self.rect = self.image.get_rect()
        self.rect.x = startX
        self.rect.y = startY

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
        self.walk_frames_forward = [pygame.transform.scale(self.spritesheet.get_image(0, 7, 15, 21), (30, 42)),
                                    pygame.transform.scale(self.spritesheet.get_image(16, 7, 15, 23), (30, 46)),
                                    pygame.transform.scale(self.spritesheet.get_image(32, 7, 15, 23), (30, 46))]
        for frame in self.walk_frames_forward:
            frame.set_colorkey(WHITE)

        # Images for the walking backward animation.
        self.walk_frames_back = [pygame.transform.scale(self.spritesheet.get_image(0, 69, 15, 23), (30, 46)),
                                 pygame.transform.scale(self.spritesheet.get_image(16, 69, 15, 23), (30, 46)),
                                 pygame.transform.scale(self.spritesheet.get_image(32, 69, 15, 23), (30, 46))]
        for frame in self.walk_frames_back:
            frame.set_colorkey(WHITE)

    def animate_player(self, movementDirection):
        """
        This function will animate the movement/non-movement of a player object. If the player is not moving,
        it will use that last movement direction to pick which standing frame to use.
        """
        now = pygame.time.get_ticks()
        # Display the current frame for the walking animation.
        if movementDirection is not None:
            self.lastMovementDirection = movementDirection
            # Only update the frame and move the player if a certain amount of time has passed.
            # This will allow us to control the speed of the animation.
            # Change ANIMATION_SPEED in Settings.py in order to see the effect.
            if now - self.last_update > ANIMATION_SPEED:
                self.last_update = now
                if movementDirection is pygame.K_RIGHT:
                    # Calculate the index of the next frame to display in the animaation.
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                    # Update the image to the current frame of the animation.
                    self.image = self.walk_frames_r[self.current_frame]
                    # Move the underlying rectangle of which the image of the player will be drawn onto.
                elif movementDirection is pygame.K_LEFT:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                    self.image = self.walk_frames_l[self.current_frame]
                elif movementDirection is pygame.K_UP:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_forward)
                    self.image = self.walk_frames_forward[self.current_frame]
                elif movementDirection is pygame.K_DOWN:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_back)
                    self.image = self.walk_frames_back[self.current_frame]
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
