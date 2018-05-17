import pygame
from Settings import WIDTH, HEIGHT, TITLE, WHITE, BLACK
from Sprites import Player, Bomb

# Initialization function needed by Pygame
pygame.init()

# Size of the screen/window for the game
size = (WIDTH, HEIGHT)

# Pygame screen object which all the sprites and backgrounds will be drawn onto
screen = pygame.display.set_mode(size)

# Setting the title of the game which appears in the top bar of the application
pygame.display.set_caption(TITLE)

# Boolean value that keeps the game running until someone wins or the game is closed
carryOn = True

# Clock for the game, helps with timing of animations like bomb explosion
clock = pygame.time.Clock()

# Set of all active sprites, that will be drawn each frame
all_sprites = pygame.sprite.Group()

# Creation of the players in the game
player1 = Player()

# Adding player1 to the active list of all sprites
all_sprites.add(player1)

# Set of all active bombs
bomb_set = set()

# Set of bombs that have exploded at a certain frame and need to be removed from the bomb_set and the all_sprites list
bombs_to_remove = set()

while carryOn:
    time = clock.tick(100)

    # Close the game if someone exits the screen.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carryOn = False

    # Get the key that waas pressed by the user.
    keys = pygame.key.get_pressed()

    # Draw all of the sprites on the screen.
    all_sprites.draw(screen)

    # Check if any bombs on the screen have expired and are ready to explode.
    for bomb in bomb_set:
        if bomb.animate(time):
            bombs_to_remove.add(bomb)
            break

    # if bombs to remove isn't empty, remove them from the bomb_set, which is the set of all active bombs
    if bombs_to_remove:
        bomb_set -= bombs_to_remove

    # Remove all the bombs that exploded from the list of all the sprites that are drawn each frame
    for bomb in bombs_to_remove:
        all_sprites.remove(bomb)

    # If else statements for all the possible user inputs, for both movement and combat
    # The user can use WASD or the arrow keys in order to move their character
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player1.walk_left()
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player1.walk_right()
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        player1.walk_forward()
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player1.walk_backward()
    # Space button is used to drop bombs
    elif keys[pygame.K_SPACE]:
        now = pygame.time.get_ticks()
        # Drop a bomb only if sufficient amount of time has passed since the last bomb was dropped
        if now - player1.lastBombPlacementTime > 2000 and player1.place_bomb():
            # Update the player's last bomb drop time
            player1.lastBombPlacementTime = now
            # Create a new bomb object and add to the bomb set and sprites list
            bomb = Bomb()
            all_sprites.add(bomb)
            bomb_set.add(bomb)
            # Update the location of the bomb to the (x,y) of where the player dropped it
            bomb.rect.x = player1.rect.x
            bomb.rect.y = player1.rect.y + 20
            # Re-animate the player
            player1.animate_player()
    else:
        player1.walking = False
        player1.placingBomb = False
        player1.animate_player()

    # These 4 statements will redraw the game, both the background and the sprites on top of the background
    all_sprites.update()
    pygame.display.flip()
    screen.fill(BLACK)
    clock.tick(60)

# Game has ended, we can close pygame
pygame.quit()
