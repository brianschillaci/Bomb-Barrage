from os import path
from typing import List
import pygame
from Settings import SPRITESHEET, RESOURCE_FOLDER, ANIMATION_SPEED, WHITE
from sprites.Spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
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

        # Boolean values for current states of action for this player
        self.walking = False
        self.walkingLeft = False
        self.walkingRight = False
        self.walkingForward = False
        self.walkingBackward = False
        self.placingBomb = False

        # Time that the last bomb was placed, this allows us to control the amount of time in between bomb placements.
        self.lastBombPlacementTime = -2000

        # Index of the current sprite/frame that the player is displayed as
        self.current_frame = 0

        # Time since last frame update - this allows us to control how fast the animations move
        self.last_update = 0

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

    # End of load_images() function

    def animate_player(self):
        """
        This function will animate the movement/non-movement of a player object.
        :return: No return.
        """
        now = pygame.time.get_ticks()
        # Display the current frame for the walking animation.
        if self.walking:
            # Only update the frame and move the player if a certain amount of time has passed.
            # This will allow us to control the speed of the animation.
            # Change ANIMATION_SPEED in Settings.py in order to see the effect.
            if now - self.last_update > ANIMATION_SPEED:
                self.last_update = now
                if self.walkingRight:
                    # Calculate the index of the next frame to display in the animaation.
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                    # Update the image to the current frame of the animation.
                    self.image = self.walk_frames_r[self.current_frame]
                    # Move the underlying rectangle of which the image of the player will be drawn onto.
                elif self.walkingLeft:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                    self.image = self.walk_frames_l[self.current_frame]
                elif self.walkingForward:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_forward)
                    self.image = self.walk_frames_forward[self.current_frame]
                elif self.walkingBackward:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_back)
                    self.image = self.walk_frames_back[self.current_frame]
            self.walking = False
        # Display the frame for if the player is standing still
        elif not self.walking:
            self.last_update = now
            if self.walkingRight:
                self.current_frame = 1
            elif self.walkingLeft:
                self.current_frame = 2
            elif self.walkingForward:
                self.current_frame = 3
            elif self.walkingBackward:
                self.current_frame = 0
            self.image = self.standing_frames[self.current_frame]

    def walk_right(self):
        self.reset_walking_booleans()
        self.walking = True
        self.walkingRight = True
        self.animate_player()

    def walk_forward(self):
        self.reset_walking_booleans()
        self.walking = True
        self.walkingForward = True
        self.animate_player()

    def walk_left(self):
        self.reset_walking_booleans()
        self.walking = True
        self.walkingLeft = True
        self.animate_player()

    def walk_backward(self):
        self.reset_walking_booleans()
        self.walking = True
        self.walkingBackward = True
        self.animate_player()

    def reset_walking_booleans(self):
        self.walking = False
        self.walkingLeft = False
        self.walkingRight = False
        self.walkingForward = False
        self.walkingBackward = False
        self.placingBomb = False

    def place_bomb(self):
        self.reset_walking_booleans()
        self.placingBomb = True
        return True
