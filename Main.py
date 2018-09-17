import pygame
from os import path
from gui_game_board import GUIGameBoard as GBoard
from Settings import WIDTH, HEIGHT, TITLE, RESOURCE_FOLDER, SPRITESHEET, BOMBSPRITESHEET, \
    LEVEL_0_BRD, LEVEL_1_BRD, LEVEL_2_BRD, LEVEL_0_THEME, LEVEL_1_THEME, LEVEL_2_THEME, BLACK, MOVEMENT_DISTANCE
from sprites.Bombs import drop_bomb
from sprites.MapElements import Wall, UnbreakableRock, BreakableRock
from sprites.Players import Player
from sprites.Explosions import SuperExplosion
from util import CollisionUtil, Animations
from sprites import Spritesheet
import os

# This code will center the window on the screen of a 1920x1080p monitor
x = 720
y = 332
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

# Initialization function needed by Pygame
pygame.init()

# Size of the screen/window for the game
size = (WIDTH, HEIGHT)

# Pygame screen object which all the sprites and backgrounds will be drawn onto
screen = pygame.display.set_mode(size)

# Setting the title of the game which appears in the top bar of the application
pygame.display.set_caption(TITLE)

# Rock sprite groups
unbreakableRocks = pygame.sprite.Group()
breakableRocks = pygame.sprite.Group()

# List of sprite groups to be passed to initialization function of the game board.
# These sprite groups will we the sprite groups that the individual game board sprites will be added to.
# The index in the theme configuration determines which sprite group in this list that the sprite gets added to.
gameBoardSpriteGroups = list((breakableRocks, unbreakableRocks))

# This is a map between the string names of the classes and the actual class.
# It is used to create sprite objects in the game board.
level2BoardSpriteClassMap = {'BreakableRock': BreakableRock, 'UnbreakableRock': UnbreakableRock}

# Initialize the gui_game_board for drawing the static background on screen.
level0 = GBoard(screen, LEVEL_0_THEME, LEVEL_0_BRD)

level1 = GBoard(screen, LEVEL_1_THEME, LEVEL_1_BRD)

level2 = GBoard(screen, LEVEL_2_THEME, LEVEL_2_BRD)

# Adds all the sprites in the game board to the corresponding gameBoardSpriteGroups
level2.initialize_board_sprites(gameBoardSpriteGroups, level2BoardSpriteClassMap)

# Boolean value that keeps the game running until someone wins or the game is closed
carryOn = True

# Clock for the game, helps with timing of animations like bomb explosion
clock = pygame.time.Clock()

# Set of all player sprites
playerSprites = pygame.sprite.Group()
playerHitboxes = pygame.sprite.Group()

explosions = pygame.sprite.Group()

bombs = pygame.sprite.Group()

# Creation of the players in the game
player1 = Player(33, 50)
# Adding player1 to the player sprite group as well as
# its hitbox to the playerhitbox group
playerSprites.add(player1)
playerHitboxes.add(player1.hitbox)

# Set of all active bombs
bomb_set = set()

# Set of all explosions active
explosion_set = set()

# create sprite for collision detection  ( all this wall sprites are meant for detecting collissions)
walls = pygame.sprite.Group()

wall_1 = Wall("BLACK", 0, 0, WIDTH, 5)
wall_2 = Wall("BLACK", 0, 0, 5, HEIGHT)
wall_3 = Wall("BLACK", 0, HEIGHT - 5, WIDTH, 5)
wall_4 = Wall("BLACK", WIDTH - 5, 0, 5, HEIGHT)

walls.add(wall_1, wall_2, wall_3, wall_4)

# Set of bombs that have exploded at a certain frame and need to be removed from the bomb_set and the all_sprites list
bombs_to_remove = set()

# Set of all explosions to remove
explosions_to_remove = set()

x = path.dirname(__file__)
img_dir = path.join(x, RESOURCE_FOLDER)
spritesheet = Spritesheet.Spritesheet(path.join(img_dir, SPRITESHEET))
bombspritesheet = Spritesheet.Spritesheet(path.join(img_dir, BOMBSPRITESHEET))

# This is the main game loop. In this loop, there will be collision checking, user input handling
# (Ex: movement, dropping bombs), and game logic (Ex: dropping bombs, losing lives, or picking up powerups,
# determining a winner).
while carryOn:
    time = clock.tick(60)
    # Close the game if someone exits the screen.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carryOn = False

    # Updating the non-sprite board images for each board level
    level0.update_non_board_sprites()
    level1.update_non_board_sprites()
    level2.update_non_board_sprites()

    # Updating the hitboxes for all the players in the game.
    # Also, updating the hitboxes in the player hitbox sprite group.
    for player in playerSprites:
        player.hitbox.update_rect(player, player.rect.width - 5, player.rect.height / 4)
    CollisionUtil.update_player_hitboxes(playerHitboxes)

    # Checking for collisions with the walls of the game
    collission_1 = pygame.sprite.spritecollideany(wall_1, playerSprites)
    collission_2 = pygame.sprite.spritecollideany(wall_2, playerSprites)
    collission_3 = pygame.sprite.spritecollideany(wall_3, playerSprites)
    collission_4 = pygame.sprite.spritecollideany(wall_4, playerSprites)

    # Collisions between players and explosions - getting the collisions and then updating the players lives
    # that got hit
    playersAndExplosions = pygame.sprite.groupcollide(playerHitboxes, explosions, False, False)
    for hitbox in playersAndExplosions:
        hitbox.player.isInExplosionAnimation = True
    CollisionUtil.update_player_lives(playerSprites, time)

    # This loop will remove players and their hitboxes if they are dead. Players are dead when their lives get to 0
    for player in playerSprites:
        if player.is_dead():
            # Find this player's hitbox and remove it
            for hitbox in playerHitboxes:
                if hitbox.player is player:
                    playerHitboxes.remove(hitbox)
                    break
            # Remove this player from the game
            playerSprites.remove(player)

    # Collisions between breakable rocks and explosions - these rocks need to be removed
    breakableRocksAndExplosions = pygame.sprite.groupcollide(breakableRocks, explosions, True, False)

    # Get the key that was pressed by the user.
    keys = pygame.key.get_pressed()

    # Draw all of the sprites on the screen.
    breakableRocks.draw(screen)
    unbreakableRocks.draw(screen)
    bombs.draw(screen)
    explosions.draw(screen)
    playerSprites.draw(screen)
    walls.draw(screen)

    # Check if any bombs on the screen have expired and are ready to explode.
    for bomb in bomb_set:
        bombReadyToExplode = Animations.animate_time_limit(bomb, 125, bomb.images)
        if bombReadyToExplode:
            bombs_to_remove.add(bomb)

    # if bombs to remove isn't empty, remove them from the bomb_set, which is the set of all active bombs
    if bombs_to_remove:
        bomb_set -= bombs_to_remove

    # Remove all the bombs that exploded from the list of all the sprites that are drawn each frame
    # Also create the explosion animation for that bomb
    for bomb in bombs_to_remove:
        bombs.remove(bomb)

        # Now that this bomb is removed, we need to animate the explosion to take it's place
        explosion = SuperExplosion(player1, time, bomb.rect.x, bomb.rect.y, bombspritesheet)
        explosion_set.add(explosion)

    bombs_to_remove.clear()
    # Check if any explosions need to update their animation and also if they are done
    for explosion in explosion_set:
        explosionIsNotDone = explosion.update_explosion_list(time, unbreakableRocks)
        # If the explosion isn't done, load the next set of sprites for it
        if explosionIsNotDone:
            for sub_explosion in explosion.explosionList:
                if not explosions.has(sub_explosion):
                    explosions.add(sub_explosion)
        # The explosion is done, add to the explosion remove list
        else:
            explosions_to_remove.add(explosion)
            for subExplosion in explosion.toRemoveAtEnd:
                explosions.remove(subExplosion)

    if explosions_to_remove:
        explosion_set -= explosions_to_remove

    explosions_to_remove.clear()

    # Section for handling user input, for both movement and combat
    # The user can use WASD or the arrow keys in order to move their character
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if collission_2 is not None:
            player1.animate_player(pygame.K_LEFT)
        else:
            player1.rect.x -= MOVEMENT_DISTANCE
            CollisionUtil.fix_player_collisions(player1, gameBoardSpriteGroups, pygame.K_LEFT)
            player1.animate_player(pygame.K_LEFT)
        if keys[pygame.K_SPACE]:
            drop_bomb(player1, bombspritesheet, bombs, bomb_set)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if collission_4 is not None:
            player1.animate_player(pygame.K_RIGHT)
        else:
            player1.rect.x += MOVEMENT_DISTANCE
            CollisionUtil.fix_player_collisions(player1, gameBoardSpriteGroups, pygame.K_RIGHT)
            player1.animate_player(pygame.K_RIGHT)
        if keys[pygame.K_SPACE]:
            drop_bomb(player1, bombspritesheet, bombs, bomb_set)
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        if collission_1 is not None:
            player1.animate_player(pygame.K_UP)
        else:
            player1.rect.y -= MOVEMENT_DISTANCE
            CollisionUtil.fix_player_collisions(player1, gameBoardSpriteGroups, pygame.K_UP)
            player1.animate_player(pygame.K_UP)
        if keys[pygame.K_SPACE]:
            drop_bomb(player1, bombspritesheet, bombs, bomb_set)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if collission_3 is not None:
            player1.animate_player(pygame.K_DOWN)
        else:
            player1.rect.y += MOVEMENT_DISTANCE
            CollisionUtil.fix_player_collisions(player1, gameBoardSpriteGroups, pygame.K_DOWN)
            player1.animate_player(pygame.K_DOWN)
        if keys[pygame.K_SPACE]:
            drop_bomb(player1, bombspritesheet, bombs, bomb_set)
    elif keys[pygame.K_SPACE]:
        drop_bomb(player1, bombspritesheet, bombs, bomb_set)
    else:
        player1.placingBomb = False
        player1.animate_player(None)

    pygame.display.flip()
    screen.fill(BLACK)
    clock.tick(60)

# Game has ended, we can close pygame
pygame.quit()
