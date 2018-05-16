from os import path
from typing import List
import pygame
from Settings import SPRITESHEET, WHITE, RESOURCE_FOLDER, ANIMATION_SPEED


class UnbreakableRock(pygame.sprite.Sprite):
    def __init__(self):
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)


class BreakableRock(pygame.sprite.Sprite):
    def __init__(self):
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)


class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)


class Spritesheet:
    def __init__(self, filename):
        # Loading the full spritesheet image and storing it as a variable in this object
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x: object, y: object, width: object, height: object) -> object:
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width, height))
        return image


class Player(pygame.sprite.Sprite):
    standing_frames: List[None]
    walk_frames_r: List[None]
    walk_frames_l: List[None]
    walk_frames_forward: List[None]
    walk_frames_back: List[None]

    def __init__(self):
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)

        # Boolean values for current states of action for this player
        self.walking = False
        self.walkingLeft = False
        self.walkingRight = False
        self.walkingForward = False
        self.walkingBackward = False
        self.placingBomb = False

        # Index of the current sprite/frame that the player is displayed as
        self.current_frame = 0

        # Time since last frame update - this allows us to control how fast the animations move
        self.last_update = 0

        # Getting the spritesheet file for this player - res is the folder it is in, SPRITESHEET is the filename
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, RESOURCE_FOLDER)
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

        # Calling load_images() in order to create all of the arrays of sprite images for each set of animations
        self.load_player_images()

        # Setting the initial image of the player when it is first created
        self.image = self.standing_frames[0]

        # Setting the rect object for this player object - every sprite has a hidden rectangle behind its image
        # This rectangle allows for collision detection, movement, and more
        self.rect = self.image.get_rect()

    # End of constructor for Player object

    def load_player_images(self):
        self.standing_frames = [pygame.transform.scale(self.spritesheet.get_image(0, 66, 16, 32), (32, 64)),
                                pygame.transform.scale(self.spritesheet.get_image(0, 37, 16, 30), (32, 64)),
                                pygame.transform.scale(self.spritesheet.get_image(0, 98, 16, 32), (32, 64)),
                                pygame.transform.scale(self.spritesheet.get_image(0, 5, 16, 32), (32, 64))]
        for frame in self.standing_frames:
            frame.set_colorkey(WHITE)

        self.walk_frames_r = [pygame.transform.scale(self.spritesheet.get_image(0, 37, 16, 30), (32, 64)),
                              pygame.transform.scale(self.spritesheet.get_image(16, 37, 16, 30), (32, 64)),
                              pygame.transform.scale(self.spritesheet.get_image(32, 37, 16, 30), (32, 64))]
        for frame in self.walk_frames_r:
            frame.set_colorkey(WHITE)

        self.walk_frames_l = [pygame.transform.scale(self.spritesheet.get_image(0, 98, 16, 32), (32, 64)),
                              pygame.transform.scale(self.spritesheet.get_image(16, 98, 16, 32), (32, 64)),
                              pygame.transform.scale(self.spritesheet.get_image(32, 98, 16, 32), (32, 64))]
        for frame in self.walk_frames_l:
            frame.set_colorkey(WHITE)

        self.walk_frames_forward = [pygame.transform.scale(self.spritesheet.get_image(0, 5, 16, 32), (32, 64)),
                                    pygame.transform.scale(self.spritesheet.get_image(16, 5, 16, 32), (32, 64)),
                                    pygame.transform.scale(self.spritesheet.get_image(32, 5, 16, 32), (32, 64))]
        for frame in self.walk_frames_forward:
            frame.set_colorkey(WHITE)

        self.walk_frames_back = [pygame.transform.scale(self.spritesheet.get_image(0, 66, 16, 32), (32, 64)),
                                 pygame.transform.scale(self.spritesheet.get_image(16, 66, 16, 32), (32, 64)),
                                 pygame.transform.scale(self.spritesheet.get_image(32, 66, 16, 32), (32, 64))]
        for frame in self.walk_frames_back:
            frame.set_colorkey(WHITE)

    # End of load_images() function

    def animate_player(self):
        now = pygame.time.get_ticks()
        if self.walking:
            if now - self.last_update > ANIMATION_SPEED:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                if self.walkingRight:
                    self.image = self.walk_frames_r[self.current_frame]
                    self.rect.x += 10
                elif self.walkingLeft:
                    self.image = self.walk_frames_l[self.current_frame]
                    self.rect.x -= 10
                elif self.walkingForward:
                    self.image = self.walk_frames_forward[self.current_frame]
                    self.rect.y -= 10
                elif self.walkingBackward:
                    self.image = self.walk_frames_back[self.current_frame]
                    self.rect.y += 10
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
