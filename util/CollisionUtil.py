import pygame

from sprites.MapElements import BreakableRock, UnbreakableRock


def fix_player_collisions(player, collisionList, movementDirection):
    for collision in collisionList:
        if collision is type(BreakableRock) or type(UnbreakableRock):
            fix_player_rock_collision(player, collision, movementDirection)


def fix_player_rock_collision(player, rocks, movementDirection):
    player.hitbox.update_rect(player, player.rect.width - 5, player.rect.height / 4)

    rockCollisions = pygame.sprite.spritecollide(player.hitbox, rocks, False)

    # If the player is colliding with other objects
    if rockCollisions:
        # For each object that the player collides with, move that player to the correct
        # position depending on the movement direction
        for collisionObject in rockCollisions:
            if movementDirection is "left":
                player.rect.left = collisionObject.rect.right
            elif movementDirection is "right":
                player.rect.right = collisionObject.rect.left
            elif movementDirection is "up":
                # When a player is walking up, they don't get stopped at their head,
                # they get stopped at a smaller hit box near their feet
                player.rect.top = collisionObject.rect.top
            else:
                player.rect.bottom = collisionObject.rect.top


def update_player_lives(players, time):
    for player in players:
        if player.isInExplosionAnimation:
            if player.hitbox.explosionTime > 0:
                player.hitbox.explosionTime -= time
            else:
                # The animation is done, we can subtract one from the players lives
                # and reset values for explosion animation timer
                player.lives -= 1
                player.isInExplosionAnimation = False
                player.hitbox.explosionTime = 90


def update_player_hitboxes(playerHitboxes):
    # Add all the update hitboxes
    for hitbox in playerHitboxes:
        hitbox.update_rect(hitbox.player, hitbox.player.rect.width, hitbox.player.rect.height / 4)