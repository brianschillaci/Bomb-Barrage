import pygame

from sprites.MapElements import BreakableRock, UnbreakableRock


def fix_player_collisions(player, collisionList, movementDirection):
    """
    General method to fix all types of player collisions.
    :param player: The player sprite to fix collisions for.
    :param collisionList: The list of possible collision sprite groups.
    :param movementDirection: The direction that the player is moving.
    """
    for collision in collisionList:
        if collision is type(BreakableRock) or type(UnbreakableRock):
            fix_player_rock_collision(player, collision, movementDirection)


def fix_player_rock_collision(player, rocks, movementDirection):
    """
    Fixes player and rock collisions, depending on the direction the player is moving.
    It will keep the players within the borders of the rock sprites. This is necessary so that players don't
    get stuck in the rock sprites when moving.
    :param player: The player sprite to fix collisions for.
    :param rocks: The rocks to check for collisions with.
    :param movementDirection: The direction that the player is moving.
    """
    # Changing widths depending on the movement direction to make movement smoother.
    if movementDirection is pygame.K_DOWN or movementDirection is pygame.K_UP:
        hitboxWidth = player.rect.width - 15
    else:
        hitboxWidth = player.rect.width

    # Updating the hitbox for this player before checking for rock collisions
    player.hitbox.update_rect(player, hitboxWidth, player.rect.height / 4)

    # Getting the collisions between the rocks and this player's hitbox
    rockCollisions = pygame.sprite.spritecollide(player.hitbox, rocks, False)

    # If the player is colliding with other objects
    if rockCollisions:
        # For each object that the player collides with, move that player to the correct
        # position depending on the movement direction
        for collisionObject in rockCollisions:
            if movementDirection is pygame.K_LEFT:
                player.rect.left = collisionObject.rect.right
            elif movementDirection is pygame.K_RIGHT:
                player.rect.right = collisionObject.rect.left
            elif movementDirection is pygame.K_UP:
                # When a player is walking up, they don't get stopped at their head,
                # they get stopped at a smaller hit box near their feet
                player.rect.top = collisionObject.rect.top
            else:
                player.rect.bottom = collisionObject.rect.top


def update_player_lives(players, time):
    """
    Updates player lives based on if a player was hit by an explosion.
    Only subtracts from the player's lives once the animation is done.
    :param players: Sprite group that contains all the player sprites.
    :param time: Time that has passed. This will be subtracted from the explosion time.
    """
    for player in players:
        if player.isInExplosionAnimation:
            if player.explosionTime > 0:
                # Animation not done yet, can't subtract lives yet
                player.explosionTime -= time
            else:
                # The animation is done, we can subtract one from the players lives
                # and reset values for explosion animation timer
                player.lives -= 1
                player.isInExplosionAnimation = False
                player.explosionTime = 90


def update_player_hitboxes(playerHitboxes):
    """
    Updates all the hitboxes in the player hitboxes sprite group. Does this by using the associated player field
    in the hitbox object to change the hitbox's rectangle object in relation to the player's position.
    :param playerHitboxes: Sprite group containing all the player hitboxes.
    :return:
    """
    # Add all the updated hitboxes
    for hitbox in playerHitboxes:
        hitbox.update_rect(hitbox.player, hitbox.player.rect.width / 4, hitbox.player.rect.height / 4)
