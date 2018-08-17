import pygame

from constants import WHITE


class ExplosionImage:
    """
    Take in the x and y position of the location of an image in a spritesheet as
    well as whether the image needs to be rotated. The constructor then cuts the
    image from the spritesheet and scales it to 32 x 32 for display. After
    initialization, set an Explosion.image to be self.image for final display.
    """
    def __init__(self, sprite_x, sprite_y, rotate, sprite_sheet):
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.rotate = rotate
        self.image = pygame.transform.scale(sprite_sheet.get_image(self.sprite_x, self.sprite_y, 16, 16), (32, 32))
        if rotate:
            self.image = pygame.transform.rotate(self.image, 180)


images_initialized = False

center = None
vertical_pipe = None
horizontal_pipe = None
end_up = None
end_left = None
end_down = None
end_right = None


def init_images(sprite_sheet):
    """
    Initialize all of the ExplosionImages that are to be used in drawing
    explosion animations on the screen.
    :param sprite_sheet: The sprite sheet which contains the explosion components.
    :return: None, updates global ExplosionImage variables.
    """
    global center, vertical_pipe, horizontal_pipe, end_up, end_left, end_down, end_right, images_initialized
    center = ExplosionImage(85, 17, False, sprite_sheet)
    vertical_pipe = ExplosionImage(51, 17, False, sprite_sheet)
    horizontal_pipe = ExplosionImage(68, 17, False, sprite_sheet)
    end_up = ExplosionImage(0, 17, True, sprite_sheet)
    end_left = ExplosionImage(34, 17, True, sprite_sheet)
    end_down = ExplosionImage(0, 17, False, sprite_sheet)
    end_right = ExplosionImage(34, 17, False, sprite_sheet)

    images_initialized = True


class Explosion(pygame.sprite.Sprite):
    def __init__(self, player, x, y, width, height, bomb_rect_x, bomb_rect_y, x_amount_to_add, y_amount_to_add, explosion_image):

        # Calling super constructor for the Sprite class, since we are extending the Sprite class
        pygame.sprite.Sprite.__init__(self)
        self.player = player
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = explosion_image.image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = bomb_rect_x
        self.rect.y = bomb_rect_y

        self.rect.x += x_amount_to_add
        self.rect.y += y_amount_to_add


# noinspection PyTypeChecker
class SuperExplosion:
    explosion_list = list()
    to_remove_at_end = list()

    def __init__(self, player, time, rect_x, rect_y, bombspritesheet):
        global images_initialized
        if not images_initialized:
            init_images(bombspritesheet)
        self.time = 400
        self.player = player
        self.origin_x = rect_x
        self.origin_y = rect_y
        self.bombspritesheet = bombspritesheet
        self.update_explosion_list(time, None)

    def update_explosion_list(self, time, blockers):
        """
        Build an explosion animation in the form of a +. The size of the
        explosion is determined by self.player.explosion_size.
        :param time: Time that has passed since the explosion started.
        :param blockers: Any sprites that are blocking the explosion.
        :return: True if animation is not done, false if the aanimation is done
        """

        self.time -= time
        if self.time >= 380:
            three = Explosion(self.player, 102, 85, 16, 16, self.origin_x, self.origin_y, 0, 0, center)
            self.explosion_list.clear()
            self.explosion_list.append(three)
            self.to_remove_at_end.append(three)
            return True
        elif self.time >= 360:
            three = Explosion(self.player, 85, 85, 16, 16, self.origin_x, self.origin_y, 0, 0, center)
            self.explosion_list.clear()
            self.explosion_list.append(three)
            self.to_remove_at_end.append(three)
            return True
        elif self.time >= 340:
            three = Explosion(self.player, 68, 85, 16, 16, self.origin_x, self.origin_y, 0, 0, center)
            self.explosion_list.clear()
            self.explosion_list.append(three)
            self.to_remove_at_end.append(three)
            return True
        elif self.time >= 320:

            self.explosion_list.clear()
            # Center explosion
            cexp = Explosion(self.player, center.sprite_x, center.sprite_y, 16, 16, self.origin_x, self.origin_y, 0, 0, center)
            self.explosion_list.append(cexp)
            self.to_remove_at_end.append(cexp)

            # Build explosion path from bomb center towards the right.
            self.build_explosion_path(32, 0, True, cexp, blockers)

            # Build explosion path from bomb center towards the left.
            self.build_explosion_path(-32, 0, True, cexp, blockers)

            # Build explosion path from bomb center towards the bottom.
            self.build_explosion_path(0, 32, False, cexp, blockers)

            # Build explosion path from bomb center towards the top.
            self.build_explosion_path(0, -32, False, cexp, blockers)

            return True
        elif self.time >= 240:
            # Done with the explosion
            return True
        else:
            return False

    def build_explosion_path(self, dx, dy, is_horizontal, center_explosion, blockers):
        """
        Given a pixel sized dx and dy value from center, build the path of the
        explosion in the vector direction <dx, dy>. Appends Explosions to
        self.explosion_list dynamically and returns None.
        :param dx: The change in pixel values along x coordinate from center pos.
        :param dy: The change in pixel values along y coordinate from center pos.
        :param is_horizontal: Boolean value is true for horizontal direction,
                              false if vertical from center.
        :param center_explosion: The Explosion object representing the center of
                                 the explosion.
        :param blockers: Any sprites that are blocking the explosion.
        :return: None
        """
        if abs(dx) <= 0 and abs(dy) <= 0:
            return

        piece_number = 1
        last_explosion = center_explosion

        if is_horizontal:
            direction_piece = horizontal_pipe
        else:
            direction_piece = vertical_pipe

        while piece_number < self.player.explosion_size:
            temp = Explosion(self.player, direction_piece.sprite_x, direction_piece.sprite_y, 16, 16, self.origin_x,
                             self.origin_y, dx * piece_number, dy * piece_number, direction_piece)
            if not pygame.sprite.spritecollideany(temp, blockers) and self.explosion_list.__contains__(last_explosion):
                self.explosion_list.append(temp)
            self.to_remove_at_end.append(temp)

            last_explosion = temp
            piece_number = piece_number + 1

        end_explosion = SuperExplosion.get_end_explosion_piece(dx, dy)
        temp = Explosion(self.player, end_explosion.sprite_x, end_explosion.sprite_y, 16, 16, self.origin_x,
                         self.origin_y, dx * piece_number, dy * piece_number, end_explosion)
        if not pygame.sprite.spritecollideany(temp, blockers) and self.explosion_list.__contains__(last_explosion):
            self.explosion_list.append(temp)
        self.to_remove_at_end.append(temp)

    @staticmethod
    def get_end_explosion_piece(dx, dy):
        """
        Determine the end direction for single part of an explosion on one of the
        four cardinal directions, then return the image for that end piece.
        :param dx: The relative direction from the center of an explosion on x axis.
        :param dy: The relative direction from the center of an explosion on y axis.
        :return: The ExplosionImage for the given edge of the explosion.
        """
        if dx < 0 and dy == 0:
            return end_left
        elif dx > 0 and dy == 0:
            return end_right
        elif dx == 0 and dy < 0:
            return end_down
        else:
            return end_up