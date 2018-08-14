import pygame
from Settings import WHITE


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
            if self.bool1 is True:
                return True
            three = Explosion(self.player, 102, 85, 16, 16, self.originX, self.originY, 0, 0,
                              self.bombspritesheet, False)
            self.explosionList.clear()
            self.explosionList.append(three)
            self.toRemoveAtEnd.append(three)
            self.bool1 = True
            return True
        elif self.time >= 360:
            if self.bool2 is True:
                return True
            three = Explosion(self.player, 85, 85, 16, 16, self.originX, self.originY, 0, 0,
                              self.bombspritesheet, False)
            self.explosionList.clear()
            self.explosionList.append(three)
            self.toRemoveAtEnd.append(three)
            self.bool2 = True
            return True
        elif self.time >= 340:
            if self.bool3 is True:
                return True
            three = Explosion(self.player, 68, 85, 16, 16, self.originX, self.originY, 0, 0,
                              self.bombspritesheet, False)
            self.explosionList.clear()
            self.explosionList.append(three)
            self.toRemoveAtEnd.append(three)
            self.bool3 = True
            return True
        elif self.time >= 320:
            if self.bool5 is True:
                return True

            self.explosionList.clear()
            # Center explosion
            three = Explosion(self.player, 85, 17, 16, 16, self.originX, self.originY, 0, 0,
                              self.bombspritesheet, False)
            self.explosionList.append(three)

            # First 4 squares
            two = Explosion(self.player, 68, 17, 16, 16, self.originX, self.originY, -32, 0,
                            self.bombspritesheet,
                            False)
            if not pygame.sprite.spritecollideany(two, blockers):
                self.explosionList.append(two)

            six = Explosion(self.player, 51, 17, 16, 16, self.originX, self.originY, 0, -32,
                            self.bombspritesheet, False)
            if not pygame.sprite.spritecollideany(six, blockers):
                self.explosionList.append(six)

            four = Explosion(self.player, 68, 17, 16, 16, self.originX, self.originY, 32, 0,
                             self.bombspritesheet, False)
            if not pygame.sprite.spritecollideany(four, blockers):
                self.explosionList.append(four)

            eight = Explosion(self.player, 51, 17, 16, 16, self.originX, self.originY, 0, 32,
                              self.bombspritesheet, False)
            if not pygame.sprite.spritecollideany(eight, blockers):
                self.explosionList.append(eight)

            # Second 4 squares
            one = Explosion(self.player, 34, 17, 16, 16, self.originX, self.originY, -64, 0,
                            self.bombspritesheet, True)

            if not pygame.sprite.spritecollideany(one, blockers) and self.explosionList.__contains__(
                    two):
                self.explosionList.append(one)

            seven = Explosion(self.player, 0, 17, 16, 16, self.originX, self.originY, 0, -64,
                              self.bombspritesheet, False)

            if not pygame.sprite.spritecollideany(seven, blockers) and self.explosionList.__contains__(
                    six):
                self.explosionList.append(seven)

            five = Explosion(self.player, 34, 17, 16, 16, self.originX, self.originY, 64, 0,
                             self.bombspritesheet, False)

            if not pygame.sprite.spritecollideany(five, blockers) and self.explosionList.__contains__(
                    four):
                self.explosionList.append(five)

            nine = Explosion(self.player, 0, 17, 16, 16, self.originX, self.originY, 0, 64,
                             self.bombspritesheet, True)
            if not pygame.sprite.spritecollideany(nine, blockers) and self.explosionList.__contains__(
                    eight):
                self.explosionList.append(nine)

            self.toRemoveAtEnd.append(one)
            self.toRemoveAtEnd.append(two)
            self.toRemoveAtEnd.append(three)
            self.toRemoveAtEnd.append(four)
            self.toRemoveAtEnd.append(five)
            self.toRemoveAtEnd.append(six)
            self.toRemoveAtEnd.append(seven)
            self.toRemoveAtEnd.append(eight)
            self.toRemoveAtEnd.append(nine)
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
