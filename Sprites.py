from os import path
from typing import List
import pygame
from Settings import SPRITESHEET, WHITE, RESOURCE_FOLDER, ANIMATION_SPEED, CUSTOM


class Explosion(pygame.sprite.Sprite):
    def __init__(self, player, x, y, width, height, bombRectX, bombRectY, xAmountToAdd, yAmountToAdd, spriteSheet,
                 rotateBool):
        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = pygame.transform.scale(spriteSheet.get_image(self.x, self.y, self.width, self.height), (32, 32))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = bombRectX
        self.rect.y = bombRectY

        self.rect.x += xAmountToAdd
        self.rect.y += yAmountToAdd
        if rotateBool:
            self.image = pygame.transform.rotate(self.image, 180)


class SuperExplosion:
    explosionList = list()
    toRemoveAtEnd = list()

    def __init__(self, player, time, rectX, rectY, bombspritesheet):
        self.time = 400
        self.player = player
        self.originX = rectX
        self.originY = rectY
        self.bombspritesheet = bombspritesheet
        self.bool1 = False
        self.bool2 = False
        self.bool3 = False
        self.bool4 = False
        self.bool5 = False
        self.bool6 = False
        self.update_explosion_list(time)

    def update_explosion_list(self, time):
        self.time -= time
        if self.time >= 380:
            if self.bool1 is True:
                return True
            explosion_square1 = Explosion(self.player, 102, 85, 16, 16, self.originX, self.originY, 0, 0,
                                          self.bombspritesheet, False)
            self.explosionList.clear()
            self.explosionList.append(explosion_square1)
            self.toRemoveAtEnd.append(explosion_square1)
            self.bool1 = True
            return True
        elif self.time >= 360:
            if self.bool2 is True:
                return True
            explosion_square1 = Explosion(self.player, 85, 85, 16, 16, self.originX, self.originY, 0, 0,
                                          self.bombspritesheet, False)
            self.explosionList.clear()
            self.explosionList.append(explosion_square1)
            self.toRemoveAtEnd.append(explosion_square1)
            self.bool2 = True
            return True
        elif self.time >= 340:
            if self.bool3 is True:
                return True
            explosion_square1 = Explosion(self.player, 68, 85, 16, 16, self.originX, self.originY, 0, 0,
                                          self.bombspritesheet, False)
            self.explosionList.clear()
            self.explosionList.append(explosion_square1)
            self.toRemoveAtEnd.append(explosion_square1)
            self.bool3 = True
            return True
        elif self.time >= 320:
            if self.bool5 is True:
                return True

            self.explosionList.clear()
            # Center explosion
            explosionSquare1 = Explosion(self.player, 85, 17, 16, 16, self.originX, self.originY, 0, 0,
                                         self.bombspritesheet, False)
            # First 4 squares
            explosionSquare2 = Explosion(self.player, 68, 17, 16, 16, self.originX, self.originY, -32, 0,
                                         self.bombspritesheet,
                                         False)
            explosionSquare3 = Explosion(self.player, 51, 17, 16, 16, self.originX, self.originY, 0, -32,
                                         self.bombspritesheet,
                                         False)
            explosionSquare4 = Explosion(self.player, 68, 17, 16, 16, self.originX, self.originY, 32, 0,
                                         self.bombspritesheet, False)
            explosionSquare5 = Explosion(self.player, 51, 17, 16, 16, self.originX, self.originY, 0, 32,
                                         self.bombspritesheet, False)
            # Second 4 squares
            explosionSquare6 = Explosion(self.player, 34, 17, 16, 16, self.originX, self.originY, -64, 0,
                                         self.bombspritesheet, True)
            explosionSquare7 = Explosion(self.player, 0, 17, 16, 16, self.originX, self.originY, 0, -64,
                                         self.bombspritesheet, False)
            explosionSquare8 = Explosion(self.player, 34, 17, 16, 16, self.originX, self.originY, 64, 0,
                                         self.bombspritesheet, False)
            explosionSquare9 = Explosion(self.player, 0, 17, 16, 16, self.originX, self.originY, 0, 64,
                                         self.bombspritesheet, True)
            self.explosionList.append(explosionSquare1)
            self.explosionList.append(explosionSquare2)
            self.explosionList.append(explosionSquare3)
            self.explosionList.append(explosionSquare4)
            self.explosionList.append(explosionSquare5)
            self.toRemoveAtEnd.append(explosionSquare1)
            self.toRemoveAtEnd.append(explosionSquare2)
            self.toRemoveAtEnd.append(explosionSquare3)
            self.toRemoveAtEnd.append(explosionSquare4)
            self.toRemoveAtEnd.append(explosionSquare5)
            self.explosionList.append(explosionSquare6)
            self.explosionList.append(explosionSquare7)
            self.explosionList.append(explosionSquare8)
            self.explosionList.append(explosionSquare9)
            self.toRemoveAtEnd.append(explosionSquare6)
            self.toRemoveAtEnd.append(explosionSquare7)
            self.toRemoveAtEnd.append(explosionSquare8)
            self.toRemoveAtEnd.append(explosionSquare9)
            self.bool5 = True
            return True
        elif self.time >= 240:
            if self.bool6 is True:
                return True
            # Done with the explosion
            self.bool6 = True
            return True
        else:
            return False


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
        self.time = 400
        self.player = player
        self.image = pygame.transform.scale(spritesheet.get_image(0, 0, 16, 16), (32, 32))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def animate(self, time):
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
        if self.time <= -500:
            return True
        else:
            return False


class Spritesheet:
    def __init__(self, filename):
        """
        Constructor for a Spritesheet object.
        Creates a pygame image object from the input filename parameter.
        :param filename: Filename string to create pygame image for this Spritesheet/image of sprites.
        """
        # Loading the full spritesheet image and storing it as a variable in this object
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x: object, y: object, width: object, height: object) -> object:
        """
        Cuts an image out from the larger Spritesheet and returns it as a regular pygame image.
        :param x: x-coordinate on spritesheet of the top left pixel of the image.
        :param y: y-coordinate on spritesheet of the top left pixel of the image.
        :param width: Width amount of pixels of the image.
        :param height: Height amount of pixels of the image.
        :return:
        """
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width, height))
        return image


class Wall(pygame.sprite.Sprite):

    def __init__(self, color, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.color.Color(color))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    # Lists of frames for the different animations for the player object
    standing_frames: List[None]
    walk_frames_r: List[None]
    walk_frames_l: List[None]
    walk_frames_forward: List[None]
    walk_frames_back: List[None]

    def __init__(self):
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
        """
        This function will initialize all of the animation arrays for a player object.
        These arrays will be looped through/used in order to emulate 2d animations for the player object based on
        different user inputs.
        :return: No return.
        """
        # Images for all the different standing positions.
        self.standing_frames = [pygame.transform.scale(self.spritesheet.get_image(0, 66, 16, 32), (32, 64)),
                                pygame.transform.scale(self.spritesheet.get_image(0, 37, 16, 30), (32, 64)),
                                pygame.transform.scale(self.spritesheet.get_image(0, 98, 16, 32), (32, 64)),
                                pygame.transform.scale(self.spritesheet.get_image(0, 5, 16, 32), (32, 64))]
        for frame in self.standing_frames:
            frame.set_colorkey(WHITE)

        # Images for the walking right animation.
        self.walk_frames_r = [pygame.transform.scale(self.spritesheet.get_image(0, 37, 16, 30), (32, 64)),
                              pygame.transform.scale(self.spritesheet.get_image(16, 37, 16, 30), (32, 64)),
                              pygame.transform.scale(self.spritesheet.get_image(32, 37, 16, 30), (32, 64))]
        for frame in self.walk_frames_r:
            frame.set_colorkey(WHITE)

        # Images for the walking left animation.
        self.walk_frames_l = [pygame.transform.scale(self.spritesheet.get_image(0, 98, 16, 32), (32, 64)),
                              pygame.transform.scale(self.spritesheet.get_image(16, 98, 16, 32), (32, 64)),
                              pygame.transform.scale(self.spritesheet.get_image(32, 98, 16, 32), (32, 64))]
        for frame in self.walk_frames_l:
            frame.set_colorkey(WHITE)

        # Images for the walking forward animation.
        self.walk_frames_forward = [pygame.transform.scale(self.spritesheet.get_image(0, 5, 16, 32), (32, 64)),
                                    pygame.transform.scale(self.spritesheet.get_image(16, 5, 16, 32), (32, 64)),
                                    pygame.transform.scale(self.spritesheet.get_image(32, 5, 16, 32), (32, 64))]
        for frame in self.walk_frames_forward:
            frame.set_colorkey(WHITE)

        # Images for the walking backward animation.
        self.walk_frames_back = [pygame.transform.scale(self.spritesheet.get_image(0, 66, 16, 32), (32, 64)),
                                 pygame.transform.scale(self.spritesheet.get_image(16, 66, 16, 32), (32, 64)),
                                 pygame.transform.scale(self.spritesheet.get_image(32, 66, 16, 32), (32, 64))]
        for frame in self.walk_frames_back:
            frame.set_colorkey(WHITE)

    # End of load_images() function

    def animate_player(self, distance):
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
                    self.rect.x += distance
                elif self.walkingLeft:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                    self.image = self.walk_frames_l[self.current_frame]
                    self.rect.x -= distance
                elif self.walkingForward:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_forward)
                    self.image = self.walk_frames_forward[self.current_frame]
                    self.rect.y -= distance
                elif self.walkingBackward:
                    self.current_frame = (self.current_frame + 1) % len(self.walk_frames_back)
                    self.image = self.walk_frames_back[self.current_frame]
                    self.rect.y += distance
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

    def walk_right(self, walk):
        self.reset_walking_booleans()

        self.walking = True
        self.walkingRight = True
        if walk:
            self.animate_player(8)
        else:
            self.animate_player(0)

    def walk_forward(self, walk):
        self.reset_walking_booleans()

        self.walking = True
        self.walkingForward = True
        if walk:
            self.animate_player(8)
        else:
            self.animate_player(0)

    def walk_left(self, walk):
        self.reset_walking_booleans()

        self.walking = True
        self.walkingLeft = True
        if walk:
            self.animate_player(8)
        else:
            self.animate_player(0)

    def walk_backward(self, walk):
        self.reset_walking_booleans()

        self.walking = True
        self.walkingBackward = True
        if walk:
            self.animate_player(8)
        else:
            self.animate_player(0)

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
