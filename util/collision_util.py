import pygame

from constants import PLAYER_EXPLOSION_TIME, PLAYER_MOVEMENT_DISTANCE


def fix_player_movement_collision(player, collision_list, movement_direction):
    """
    Fixes player and objects collisions, depending on the direction the player is moving.
    It will keep the players within the borders of the object sprites. This is necessary so that players don't
    get stuck in the object sprites when moving.
    :param player: The player sprite to fix collisions for.
    :param collision_list: The list of sprite groups to get the objects to check for collisions with.
    :param movement_direction: The direction that the player is moving.
    """
    for objects in collision_list:
        # Updating the hitbox for this player before checking for rock collisions
        player.hitbox.update_rect(player, player.rect.width, player.rect.height / 4)

        # Getting the collisions between the rocks and this player's hitbox
        collisions = pygame.sprite.spritecollide(player.hitbox, objects, False)

        # If the player is colliding with other objects
        if collisions:
            # For each object that the player collides with, move that player to the correct
            # position depending on the movement direction
            for collision_object in collisions:
                if movement_direction is pygame.K_LEFT:
                    if player.hitbox.rect.midleft[1] < collision_object.rect.midright[1] - 8:
                        player.rect.y -= PLAYER_MOVEMENT_DISTANCE
                        if check_for_collision(player, collision_list) > 0:
                            player.rect.y += PLAYER_MOVEMENT_DISTANCE
                    elif player.hitbox.rect.midleft[1] > collision_object.rect.midright[1] + 8:
                        player.rect.y += PLAYER_MOVEMENT_DISTANCE
                        if check_for_collision(player, collision_list) > 0:
                            player.rect.y -= PLAYER_MOVEMENT_DISTANCE
                    player.rect.left = collision_object.rect.right
                elif movement_direction is pygame.K_RIGHT:
                    if player.hitbox.rect.midright[1] < collision_object.rect.midleft[1] - 4:
                        player.rect.y -= PLAYER_MOVEMENT_DISTANCE
                        if check_for_collision(player, collision_list) > 0:
                            player.rect.y += PLAYER_MOVEMENT_DISTANCE
                    elif player.hitbox.rect.midright[1] < collision_object.rect.midleft[1] + 4:
                        player.rect.y += PLAYER_MOVEMENT_DISTANCE
                        if check_for_collision(player, collision_list) > 0:
                            player.rect.y -= PLAYER_MOVEMENT_DISTANCE
                    player.rect.right = collision_object.rect.left
                elif movement_direction is pygame.K_UP:
                    # When a player is walking up, they don't get stopped at their head,
                    # they get stopped at a smaller hit box near their feet
                    if player.hitbox.rect.midbottom[0] < collision_object.rect.midbottom[0] - 4:
                        player.rect.x -= PLAYER_MOVEMENT_DISTANCE
                        if check_for_collision(player, collision_list) > 0:
                            player.rect.x += PLAYER_MOVEMENT_DISTANCE
                    elif player.hitbox.rect.midbottom[0] > collision_object.rect.midbottom[0] + 4:
                        player.rect.x += PLAYER_MOVEMENT_DISTANCE
                        if check_for_collision(player, collision_list) > 0:
                            player.rect.x -= PLAYER_MOVEMENT_DISTANCE
                    player.rect.bottom = collision_object.rect.bottom + player.hitbox.rect.height
                else:
                    if player.rect.midbottom[0] < collision_object.rect.midbottom[0] - 4:
                        player.rect.x -= PLAYER_MOVEMENT_DISTANCE
                        if check_for_collision(player, collision_list) > 0:
                            player.rect.x += PLAYER_MOVEMENT_DISTANCE
                    elif player.rect.midbottom[0] > collision_object.rect.midbottom[0] + 4:
                        player.rect.x += PLAYER_MOVEMENT_DISTANCE
                        if check_for_collision(player, collision_list) > 0:
                            player.rect.x -= PLAYER_MOVEMENT_DISTANCE
                    player.rect.bottom = collision_object.rect.top


def check_for_collision(player, collision_list):
    for objects in collision_list:
        # Updating the hitbox for this player before checking for rock collisions
        player.hitbox.update_rect(player, player.rect.width, player.rect.height / 4)

        # Getting the collisions between the rocks and this player's hitbox
        collisions = pygame.sprite.spritecollide(player.hitbox, objects, False)
        return collisions.__len__()


def fix_player_bomb_collision(player, bombs, movement_direction):
    # Updating the hitbox for this player before checking for rock collisions
    player.hitbox.update_rect(player, player.rect.width, player.rect.height / 4)

    # Getting the collisions between the rocks and this player's hitbox
    collisions = pygame.sprite.spritecollide(player.hitbox, bombs, False)

    # If the player is colliding with other objects
    if collisions:
        # For each object that the player collides with, move that player to the correct
        # position depending on the movement direction
        for bomb in collisions:
            if bomb.players_allowed_to_collide.__contains__(player):
                continue
            if movement_direction is pygame.K_LEFT:
                player.rect.left = bomb.rect.right
            elif movement_direction is pygame.K_RIGHT:
                player.rect.right = bomb.rect.left
            elif movement_direction is pygame.K_UP:
                # When a player is walking up, they don't get stopped at their head,
                # they get stopped at a smaller hit box near their feet
                player.rect.bottom = bomb.rect.bottom + player.hitbox.rect.height
            else:
                player.rect.bottom = bomb.rect.top


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
                player.explosionTime = PLAYER_EXPLOSION_TIME
