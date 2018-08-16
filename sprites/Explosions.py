import pygame
from Settings import WHITE

class ExplosionImage:
    def __init__(self, sprite_x, sprite_y, rotate, spriteSheet):
        self.sprite_x = sprite_x
        self.sprite_y = sprite_y
        self.rotate = rotate


center = ExplosionImage(85, 17, False)
vertical_pipe = ExplosionImage(51, 17, False)
horizontal_pipe = ExplosionImage(68, 17, False)
end_up = ExplosionImage(0, 17, True)
end_left = ExplosionImage(34, 17, True)
end_down = ExplosionImage(0, 17, False)
end_right = ExplosionImage(34, 17, False)


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
        self.update_explosion_list(time, None)

    def update_explosion_list(self, time, blockers):
        """
        Explosion sprite numbering:
        ##7##
        ##6##
        12345
        ##8##
        ##9##
        :param time: Time that has passed since the explosion started.
        :param blockers: Any sprites that are blocking the explosion.
        :return: True if animation is not done, false if the aanimation is done
        """
        self.time -= time
        if self.time >= 380:
            three = Explosion(self.player, 102, 85, 16, 16, self.originX, self.originY, 0, 0,
                              self.bombspritesheet, False)
            self.explosionList.clear()
            self.explosionList.append(three)
            self.toRemoveAtEnd.append(three)
            return True
        elif self.time >= 360:
            three = Explosion(self.player, 85, 85, 16, 16, self.originX, self.originY, 0, 0,
                              self.bombspritesheet, False)
            self.explosionList.clear()
            self.explosionList.append(three)
            self.toRemoveAtEnd.append(three)
            return True
        elif self.time >= 340:
            three = Explosion(self.player, 68, 85, 16, 16, self.originX, self.originY, 0, 0,
                              self.bombspritesheet, False)
            self.explosionList.clear()
            self.explosionList.append(three)
            self.toRemoveAtEnd.append(three)
            return True
        elif self.time >= 320:

            self.explosionList.clear()
            # Center explosion
            cexp = Explosion(self.player, center.sprite_x, center.sprite_y, 16, 16, self.originX, self.originY, 0, 0,
                              self.bombspritesheet, center.rotate)
            self.explosionList.append(cexp)
            self.toRemoveAtEnd.append(cexp)

            self.build_explosion_path(32, 0, True, cexp, blockers)
            self.build_explosion_path(-32, 0, True, cexp, blockers)
            self.build_explosion_path(0, 32, False, cexp, blockers)
            self.build_explosion_path(0, -32, False, cexp, blockers)

            return True
        elif self.time >= 240:
            # Done with the explosion
            return True
        else:
            return False

    def build_explosion_path(self, dx, dy, is_horizontal, center_explosion, blockers):
        if abs(dx) <= 0 and abs(dy) <= 0:
            return

        piece_number = 1
        last_explosion = center_explosion

        if is_horizontal:
            direction_piece = horizontal_pipe
        else:
            direction_piece = vertical_pipe

        while piece_number < self.player.explosion_size:
            temp = Explosion(self.player, direction_piece.sprite_x, direction_piece.sprite_y, 16, 16, self.originX,
                             self.originY, dx * piece_number, dy * piece_number, self.bombspritesheet, direction_piece.rotate)
            if not pygame.sprite.spritecollideany(temp, blockers) and self.explosionList.__contains__(last_explosion):
                self.explosionList.append(temp)
            self.toRemoveAtEnd.append(temp)

            last_explosion = temp
            piece_number = piece_number + 1

        end_explosion = self.get_end_explosion_piece(dx, dy)
        temp = Explosion(self.player, end_explosion.sprite_x, end_explosion.sprite_y, 16, 16, self.originX,
                         self.originY, dx * piece_number, dy * piece_number, self.bombspritesheet,
                         end_explosion.rotate)
        if not pygame.sprite.spritecollideany(temp, blockers) and self.explosionList.__contains__(last_explosion):
            self.explosionList.append(temp)
        self.toRemoveAtEnd.append(temp)

    def get_end_explosion_piece(self, dx, dy):
        if dx < 0 and dy == 0:
            return end_left
        elif dx > 0 and dy == 0:
            return end_right
        elif dx == 0 and dy < 0:
            return end_down
        else:
            return end_up
