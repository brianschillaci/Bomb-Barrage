from os import path

import pygame

from board.gui_game_board import GUIGameBoard as GBoard
from constants import WIDTH, HEIGHT, \
    LEVEL_0_BRD, LEVEL_1_BRD, LEVEL_2_BRD, LEVEL_0_THEME, LEVEL_1_THEME, LEVEL_2_THEME, BLACK, \
    RESOURCE_FOLDER, BOMBSPRITESHEET, PLAYERSPRITESHEET
from sprites import bombs
from sprites.explosions import SuperExplosion
from sprites.map_elements import Wall, UnbreakableRock, BreakableRock
from sprites.players import Player
from sprites.spritesheet import Spritesheet
from util import collision_util, animation_util


def lan_mode(screen):
    # set to True - until the game ends
    is_game_running = True

    # Clock for the game - used for animations
    clock = pygame.time.Clock()

    # ---------------------------------------------
    # GAMEBOARDS
    # ---------------------------------------------
    level0 = GBoard(screen, LEVEL_0_THEME, LEVEL_0_BRD)
    level1 = GBoard(screen, LEVEL_1_THEME, LEVEL_1_BRD)
    level2 = GBoard(screen, LEVEL_2_THEME, LEVEL_2_BRD)

    # ---------------------------------------------
    # SPRITE_SHEETS
    # ---------------------------------------------
    cwd = path.dirname(__file__)
    parent = path.join(cwd, "..")
    img_dir = path.join(parent, RESOURCE_FOLDER)
    bomb_sprite_sheet = Spritesheet(path.join(img_dir, BOMBSPRITESHEET))
    player_sprite_sheet = Spritesheet(path.join(img_dir, PLAYERSPRITESHEET))

    # ---------------------------------------------
    # ROCKS
    # ---------------------------------------------
    unbreakable_rocks = pygame.sprite.Group()
    breakable_rocks = pygame.sprite.Group()

    # ---------------------------------------------
    # PLAYERS
    # ---------------------------------------------
    player_sprites = pygame.sprite.Group()
    player_hitboxes = pygame.sprite.Group()
    player1 = Player(33, 50, player_sprite_sheet)
    player_sprites.add(player1)
    player_hitboxes.add(player1.hitbox)

    # ---------------------------------------------
    # BOMBS AND EXPLOSIONS
    # ---------------------------------------------
    all_bombs = pygame.sprite.Group()
    all_explosions = pygame.sprite.Group()
    all_bombs_set = set()
    all_explosions_set = set()
    finished_bombs_to_remove = set()
    finished_explosions_to_remove = set()

    # ---------------------------------------------
    # WALLS
    # ---------------------------------------------
    walls_group = pygame.sprite.Group()
    wall_1 = Wall("BLACK", 0, 0, WIDTH, 5)
    wall_2 = Wall("BLACK", 0, 0, 5, HEIGHT)
    wall_3 = Wall("BLACK", 0, HEIGHT - 5, WIDTH, 5)
    wall_4 = Wall("BLACK", WIDTH - 5, 0, 5, HEIGHT)
    walls_list = list((wall_1, wall_2, wall_3, wall_4))
    walls_group.add(wall_1, wall_2, wall_3, wall_4)

    # ---------------------------------------------
    # LEVEL 2 BOARD INITIALIZATION
    # ---------------------------------------------

    # List of sprite groups to be passed to initialization function of the game board.
    # These sprite groups will we the sprite groups that the individual game board sprites will be added to.
    # The index in the theme configuration determines which sprite group in this list that the sprite gets added to.
    level2_sprite_groups = list((breakable_rocks, unbreakable_rocks))
    # This is a map between the string names of the classes and the actual class.
    # It is used to create sprite objects in the game board.
    level_2_class_map = {'BreakableRock': BreakableRock, 'UnbreakableRock': UnbreakableRock}
    # Adds all the sprites in the game board to the corresponding gameBoardSpriteGroups
    level2.initialize_board_sprites(level2_sprite_groups, level_2_class_map)

    # This is the main game loop. In this loop, there will be collision checking, user input handling
    # (Ex: movement, dropping bombs), and game logic (Ex: dropping bombs, losing lives, or picking up powerups,
    # determining a winner).
    while is_game_running:
        time = clock.tick(60)
        # Close the game if someone exits the screen.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_running = False

        # Updating the hitboxes for all the players in the game.
        # Also, updating the hitboxes in the player hitbox sprite group.
        for player in player_sprites:
            player.hitbox.update_rect(player, player.rect.width / 4, player.rect.height / 4)

        # Collisions between players and explosions - getting the collisions and then updating the players lives
        # that got hit.
        players_and_explosions = pygame.sprite.groupcollide(player_hitboxes, all_explosions, False, False)
        for hitbox in players_and_explosions:
            hitbox.player.isInExplosionAnimation = True
        collision_util.update_player_lives(player_sprites, time)

        # This loop will remove players and their hitboxes if they are dead. Players are dead when their lives get to 0
        for player in player_sprites:
            if player.is_dead():
                # Find this player's hitbox and remove it
                for hitbox in player_hitboxes:
                    if hitbox.player is player:
                        player_hitboxes.remove(hitbox)
                        break
                # Remove this player from the game
                player_sprites.remove(player)

        # Collisions between breakable rocks and explosions - these rocks need to be removed
        pygame.sprite.groupcollide(breakable_rocks, all_explosions, True, False)

        # Get the key that was pressed by the user.
        keys = pygame.key.get_pressed()

        # Check if any bombs on the screen have expired and are ready to explode.
        for bomb in all_bombs_set:
            bomb_ready_to_explode = animation_util.animate_with_limit(bomb, 125, bomb.images)
            if bomb_ready_to_explode:
                finished_bombs_to_remove.add(bomb)

        # if bombs to remove isn't empty, remove them from the bomb_set, which is the set of all active bombs
        if finished_bombs_to_remove:
            all_bombs_set -= finished_bombs_to_remove

        # Remove all the bombs that exploded from the list of all the sprites that are drawn each frame
        # Also create the explosion animation for that bomb
        for bomb in finished_bombs_to_remove:
            all_bombs.remove(bomb)
            bomb.player.active_bombs.remove(bomb)
            # Now that this bomb is removed, we need to animate the explosion to take it's place
            explosion = SuperExplosion(player1, time, bomb.rect.x, bomb.rect.y, bomb_sprite_sheet)
            all_explosions_set.add(explosion)

        finished_bombs_to_remove.clear()

        # Check if any explosions need to update their animation and also if they are done
        for explosion in all_explosions_set:
            explosion_not_done = explosion.update_explosion_list(time, unbreakable_rocks)
            # If the explosion isn't done, load the next set of sprites for it
            if explosion_not_done:
                for sub_explosion in explosion.explosion_list:
                    if not all_explosions.has(sub_explosion):
                        all_explosions.add(sub_explosion)
            # The explosion is done, add to the explosion remove list
            else:
                finished_explosions_to_remove.add(explosion)
                for sub_explosion in explosion.to_remove_at_end:
                    all_explosions.remove(sub_explosion)

        # Remove finished explosions from the active set
        if finished_explosions_to_remove:
            all_explosions_set -= finished_explosions_to_remove
            finished_explosions_to_remove.clear()

        # Update active bombs to make sure collisions with bombs are working properly
        bombs.update_active_bombs(player_sprites, all_bombs)

        # Section for handling user input, for both movement and combat
        # The user can use WASD or the arrow keys in order to move their character
        for player in player_sprites:
            player.handle_input(walls_list, level2_sprite_groups, bomb_sprite_sheet, all_bombs, all_bombs_set, keys,
                                player_sprites)

        # Updating the non-sprite board images for each board level
        level0.update_non_board_sprites()
        level1.update_non_board_sprites()
        level2.update_non_board_sprites()

        # Draw all of the sprites on the screen.
        breakable_rocks.draw(screen)
        unbreakable_rocks.draw(screen)
        all_bombs.draw(screen)
        all_explosions.draw(screen)
        player_sprites.draw(screen)
        walls_group.draw(screen)

        # Updating the screen and setting the frames per second
        pygame.display.flip()
        screen.fill(BLACK)
        clock.tick(60)

    # Game has ended, we can close pygame
    pygame.quit()
