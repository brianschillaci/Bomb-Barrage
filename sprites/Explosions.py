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
