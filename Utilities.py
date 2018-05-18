import pygame

from Sprites import Bomb


def drop_bomb(player, bombspritesheet, otherSprites, bomb_set):
    now = pygame.time.get_ticks()
    # Drop a bomb only if sufficient amount of time has passed since the last bomb was dropped
    if now - player.lastBombPlacementTime > 2000 and player.place_bomb():
        # Update the player's last bomb drop time
        player.lastBombPlacementTime = now
        # Create a new bomb object and add to the bomb set and sprites list
        bomb = Bomb(player, bombspritesheet)
        otherSprites.add(bomb)
        bomb_set.add(bomb)
        # Update the location of the bomb to the (x,y) of where the player dropped it
        bomb.rect.x = player.rect.x
        bomb.rect.y = player.rect.y + 20
