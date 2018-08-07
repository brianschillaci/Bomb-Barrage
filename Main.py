from os import path

from CollisionUtil import player_collision_allowed_rocks
from gui_game_board import GUIGameBoard as GBoard
import pygame
from Settings import WIDTH, HEIGHT, TITLE, RESOURCE_FOLDER, SPRITESHEET, BOMBSPRITESHEET, \
    LEVEL_0_BRD, LEVEL_1_BRD, LEVEL_2_BRD, LEVEL_0_THEME, LEVEL_1_THEME, LEVEL_2_THEME, BLACK, MOVEMENT_DISTANCE
from Sprites import Player, Spritesheet, SuperExplosion, Wall, BreakableRock, UnbreakableRock

# Initialization function needed by Pygame
from Utilities import drop_bomb

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

# Set of all active sprites, that will be drawn each frame
playerSprites = pygame.sprite.Group()

explosions = pygame.sprite.Group()

bombs = pygame.sprite.Group()

# Creation of the players in the game
player1 = Player(33,50)

# Adding player1 to the active list of all sprites
playerSprites.add(player1)

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
spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
bombspritesheet = Spritesheet(path.join(img_dir, BOMBSPRITESHEET))


def walking_collision_check(collisionList):
    for collision in collisionList:
        if collision is not None:
            return True
        else:
            continue
    return False


while carryOn:
    time = clock.tick(60)
    # Close the game if someone exits the screen.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carryOn = False

    level0.update_non_board_sprites()

    level1.update_non_board_sprites()

    level2.update_non_board_sprites()

    # check for collisions in all the four corners of the screen
    collission_1 = pygame.sprite.spritecollideany(wall_1, playerSprites)
    collission_2 = pygame.sprite.spritecollideany(wall_2, playerSprites)
    collission_3 = pygame.sprite.spritecollideany(wall_3, playerSprites)
    collission_4 = pygame.sprite.spritecollideany(wall_4, playerSprites)

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
        if bomb.animate(time):
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
        explosionDoneBool = explosion.update_explosion_list(time)
        # If the explosion isn't done, load the next set of sprites for it
        if explosionDoneBool:
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

    # If else statements for all the possible user inputs, for both movement and combat
    # The user can use WASD or the arrow keys in order to move their character
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if collission_2 is not None:
            player1.walk_left()
        else:
            player1.rect.x -= MOVEMENT_DISTANCE
            ableToWalk = player_collision_allowed_rocks(player1, unbreakableRocks, 'left')
            ableToWalk = player_collision_allowed_rocks(player1, breakableRocks, 'left')
            player1.walk_left()
        if keys[pygame.K_SPACE]:
            drop_bomb(player1, bombspritesheet, bombs, bomb_set)
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if collission_4 is not None:
            player1.walk_right()
        else:
            player1.rect.x += MOVEMENT_DISTANCE
            ableToWalk = player_collision_allowed_rocks(player1, unbreakableRocks, 'right')
            ableToWalk = player_collision_allowed_rocks(player1, breakableRocks, 'right')
            player1.walk_right()
        if keys[pygame.K_SPACE]:
            drop_bomb(player1, bombspritesheet, bombs, bomb_set)
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        if collission_1 is not None:
            player1.walk_forward()
        else:
            player1.rect.y -= MOVEMENT_DISTANCE
            ableToWalk = player_collision_allowed_rocks(player1, unbreakableRocks, 'up')
            ableToWalk = player_collision_allowed_rocks(player1, breakableRocks, 'up')
            player1.walk_forward()
        if keys[pygame.K_SPACE]:
            drop_bomb(player1, bombspritesheet, bombs, bomb_set)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if collission_3 is not None:
            player1.walk_backward()
        else: 
            player1.rect.y += MOVEMENT_DISTANCE
            ableToWalk = player_collision_allowed_rocks(player1, unbreakableRocks, 'down')
            ableToWalk = player_collision_allowed_rocks(player1, breakableRocks, 'down')
            player1.walk_backward()
        if keys[pygame.K_SPACE]:
            drop_bomb(player1, bombspritesheet, bombs, bomb_set)
    elif keys[pygame.K_SPACE]:
        drop_bomb(player1, bombspritesheet, bombs, bomb_set)
    else:
        player1.walking = False
        player1.placingBomb = False
        player1.animate_player()

    # These 4 statements will redraw the game, both the background and the sprites on top of the background
    unbreakableRocks.update()
    breakableRocks.update()
    bombs.update()
    explosions.update()
    playerSprites.update()
    pygame.display.flip()
    screen.fill(BLACK)
    clock.tick(60)

# Game has ended, we can close pygame
pygame.quit()
