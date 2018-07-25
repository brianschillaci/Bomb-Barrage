import pygame


def player_movement_collision_allowed(spriteObject, objectsToCollideWith, movementDirection):

    collisionObjects = pygame.sprite.spritecollide(spriteObject, objectsToCollideWith, False)

    if collisionObjects:
        for collisionObject in collisionObjects:
            if movementDirection is "left":
                spriteObject.rect.left = collisionObject.rect.right
            elif movementDirection is "right":
                spriteObject.rect.right = collisionObject.rect.left
            elif movementDirection is "up":
                spriteObject.rect.top = collisionObject.rect.bottom
            else:
                spriteObject.rect.bottom = collisionObject.rect.top
        return False
    else:
        return True

