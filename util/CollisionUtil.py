import pygame

from sprites.Players import Player
from sprites.MapElements import BreakableRock, UnbreakableRock


def fix_player_collisions(player, collisionList, movementDirection):
    for collision in collisionList:
        if collision is type(BreakableRock) or type(UnbreakableRock):
            fix_player_rock_collision(player, collision, movementDirection)


def fix_player_rock_collision(spriteObject, rocks, movementDirection):
    # Creating a temporary copy of the player sprite
    spriteObjectTemp = Player(spriteObject.rect.x, spriteObject.rect.y)
    spriteObjectTemp.rect = pygame.rect.Rect((0, 0), (9, 15))
    if movementDirection is "left":
        spriteObjectTemp.rect.bottomleft = spriteObject.rect.bottomleft
    elif movementDirection is "right":
        spriteObjectTemp.rect.bottomright = spriteObject.rect.bottomright
    else:
        spriteObjectTemp.rect.midbottom = spriteObject.rect.midbottom

    rockCollisions = pygame.sprite.spritecollide(spriteObjectTemp, rocks, False)

    # If the player is colliding with other objects
    if rockCollisions:
        # For each object that the player collides with, move that player to the correct
        # position depending on the movement direction
        for collisionObject in rockCollisions:
            if movementDirection is "left":
                spriteObject.rect.left = collisionObject.rect.right
            elif movementDirection is "right":
                spriteObject.rect.right = collisionObject.rect.left
            elif movementDirection is "up":
                # When a player is walking up, they don't get stopped at their head,
                # they get stopped at a smaller hit box near their feet
                spriteObject.rect.top = collisionObject.rect.top + 5
            else:
                spriteObject.rect.bottom = collisionObject.rect.top
